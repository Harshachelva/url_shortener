import hashlib
import sqlite3
import redis
import random
import string
from flask import Flask, request, jsonify, redirect
from tenacity import retry, stop_after_attempt, wait_fixed, wait_exponential
from functools import wraps
from retry import retry_decorator
import logging
import os
app = Flask(__name__)


# Database initialization
DB_PATH = os.environ.get('DB_PATH', 'shortener.db')
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()



# Initialize Redis client
r = redis.Redis(decode_responses=True)
REDIS_KEY = 'url_id_counter'

# Define the Base62 character set
BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(BASE62)

def encode_base62(num):
    """Encodes an integer (the ID) into a Base62 string."""
    if num == 0:
        return BASE62[0]
    
    encoded = []
    while num > 0:
        encoded.append(BASE62[num % BASE])
        num //= BASE
    
    # Base62 strings are read right-to-left, so we reverse the result
    return "".join(encoded[::-1])

# NOTE: A decoder is usually not needed for lookup, as you can store the 
# short code directly in the database, but it's good practice:
def decode_base62(s):
    """Decodes a Base62 string back to an integer."""
    num = 0
    for char in s:
        num = num * BASE + BASE62.index(char)
    return num

# ----------------# Helper functions#-----------------#
# Generates a short code for a given URL
def generate_short_code(url):
   hash_object = hashlib.md5(url.encode())
   return hash_object.hexdigest()[:6]

def is_valid_url(url):
   return url.startswith("http://") or url.startswith("https://")


# Inserts a URL into the database
@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=4)) 
def store_url(original_url, custom_code=None):
    
    if custom_code:
        # Case 1: Custom code provided.
        short_code = custom_code
    else:
        # Case 2: Generated short code needed.
        # 1. ATOMIC COUNTER INCREMENT (No collisions possible here)
        unique_id = r.incr(REDIS_KEY) 
        
        # 2. ENCODE ID TO SHORT CODE
        short_code = encode_base62(unique_id)
    try:
        cursor.execute(
           "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
           (original_url, short_code),
        )
        conn.commit()
        return short_code
        
    except sqlite3.IntegrityError:
        # This error now only happens if:
        # 1. A custom_code was used and already exists.
        # 2. (EXTREMELY RARE) The Redis counter was reset, causing a re-use of an old ID.
        
        if custom_code:
            # If the custom code is taken, raise a unique error
            raise ValueError("Custom short code is already in use.Please retry with a different code or we can generate one for you.")
        else:
            logging.getLogger(__name__).critical(
               "CRITICAL COLLISION: Generated code '%s' already exists. Skipping ID %s.",
               short_code,
               unique_id,
            )
            raise Exception("Generated code collision detected.")


@retry(stop=stop_after_attempt(3), wait=wait_exponential(2))
# Retrieves the original URL from the database
def get_original_url(short_code):
   cursor.execute("SELECT original_url FROM urls WHERE short_code = ?", (short_code,))
   result = cursor.fetchone()
   if result:
       return result[0]
   return None




#-----------------# Flask API endpoints#-----------------#
@app.route("/shorten", methods=["POST"])
def shorten_url():
   data = request.get_json()

   if "url" not in data:
       return jsonify({"error": "URL is required"}), 400

   original_url = data["url"]
   custom_code = data.get("custom_code") 

   if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL format. Must start with http:// or https://"}), 400

   try:
       short_code = store_url(original_url, custom_code=custom_code)
   except ValueError as e:
       return jsonify({"error": str(e)}), 409 # 409 Conflict

   return jsonify({
       "shortened_url": f"http://short.ly/{short_code}",
       "original_url": original_url,
       "custom_code_used": bool(custom_code)
       })




@app.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
   original_url = get_original_url(short_code)
   if original_url:
       return redirect(original_url, code=302)
   return (
       jsonify({"error": "Short URL not found"}),
       404,
    )


if __name__ == "__main__":
   app.run(debug=True)
