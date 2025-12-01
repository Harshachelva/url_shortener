import hashlib
import sqlite3
import redis
import logging
import os
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from tenacity import retry, stop_after_attempt, wait_exponential
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simple CORS - Allow all origins (for development)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuration
DB_PATH = os.environ.get('DB_PATH', 'data/shortener.db')
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

# Initialize Redis client
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    r.ping()
    logger.info("Successfully connected to Redis")
except redis.ConnectionError:
    logger.error("Failed to connect to Redis")
    raise

REDIS_KEY = 'url_id_counter'

# Define the Base62 character set
BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(BASE62)

# Database connection pool
@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()

def encode_base62(num):
    """Encodes an integer (the ID) into a Base62 string."""
    if num == 0:
        return BASE62[0]
    
    encoded = []
    while num > 0:
        encoded.append(BASE62[num % BASE])
        num //= BASE
    
    return "".join(encoded[::-1])

def decode_base62(s):
    """Decodes a Base62 string back to an integer."""
    num = 0
    for char in s:
        num = num * BASE + BASE62.index(char)
    return num

def is_valid_url(url):
    """Validates URL format"""
    return url.startswith("http://") or url.startswith("https://")

def is_valid_custom_code(code):
    """Validates custom code format"""
    if not code:
        return True
    # Only alphanumeric and hyphens, 3-20 characters
    if len(code) < 3 or len(code) > 20:
        return False
    return all(c.isalnum() or c == '-' for c in code)

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=4))
def store_url(original_url, custom_code=None):
    """Stores a URL in the database with collision handling"""
    
    if custom_code:
        if not is_valid_custom_code(custom_code):
            raise ValueError("Custom code must be 3-20 characters and contain only letters, numbers, and hyphens")
        short_code = custom_code
    else:
        # Atomic counter increment
        unique_id = r.incr(REDIS_KEY)
        short_code = encode_base62(unique_id)
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
                (original_url, short_code),
            )
            conn.commit()
        
        logger.info(f"Stored URL: {short_code} -> {original_url}")
        return short_code
        
    except sqlite3.IntegrityError:
        if custom_code:
            raise ValueError("Custom short code is already in use. Please try a different code.")
        else:
            logger.critical(
                f"CRITICAL COLLISION: Generated code '{short_code}' already exists. ID: {unique_id}"
            )
            raise Exception("Generated code collision detected.")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2))
def get_original_url(short_code):
    """Retrieves the original URL from the database"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT original_url FROM urls WHERE short_code = ?", (short_code,))
            result = cursor.fetchone()
            if result:
                logger.info(f"Retrieved URL for code: {short_code}")
                return result[0]
        return None
    except Exception as e:
        logger.error(f"Error retrieving URL for {short_code}: {e}")
        return None

# -------------------- Flask API Endpoints --------------------

@app.route("/", methods=["GET"])
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "service": "URL Shortener API",
        "version": "1.0"
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check with service status"""
    try:
        r.ping()
        redis_status = "connected"
    except:
        redis_status = "disconnected"
    
    return jsonify({
        "status": "healthy",
        "redis": redis_status,
        "database": "connected" if os.path.exists(DB_PATH) else "not found"
    })

@app.route("/shorten", methods=["POST"])
def shorten_url():
    """Shorten a URL"""
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "URL is required"}), 400

    original_url = data["url"]
    custom_code = data.get("custom_code", "").strip() or None

    if not is_valid_url(original_url):
        return jsonify({
            "error": "Invalid URL format. Must start with http:// or https://"
        }), 400

    try:
        short_code = store_url(original_url, custom_code=custom_code)
        
        return jsonify({
            "shortened_url": f"http://short.ly/{short_code}",
            "original_url": original_url,
            "short_code": short_code,
            "custom_code_used": bool(custom_code)
        }), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        logger.error(f"Error shortening URL: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    """Redirect to original URL"""
    original_url = get_original_url(short_code)
    
    if original_url:
        return redirect(original_url, code=302)
    
    return jsonify({"error": "Short URL not found"}), 404

@app.route("/stats/<short_code>", methods=["GET"])
def get_stats(short_code):
    """Get stats for a short code"""
    original_url = get_original_url(short_code)
    
    if not original_url:
        return jsonify({"error": "Short URL not found"}), 404
    
    return jsonify({
        "short_code": short_code,
        "original_url": original_url,
        "shortened_url": f"http://short.ly/{short_code}"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH) if os.path.dirname(DB_PATH) else 'data', exist_ok=True)
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)