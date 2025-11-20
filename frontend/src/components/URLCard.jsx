import { useState } from "react";
function URLCard({ originalUrl, shortUrl }) {
    const [longUrl, setLongUrl] = useState("");

    const generateShortUrl = (e) => {
        e.preventDefault()
        alert(`Generating short URL for: ${longUrl}`);
    }

    return (
        <div className="url-card">
            <form onSubmit={generateShortUrl} className="URL-form">
                <div className="url - field">
                    <p>Enter your Long URL here:</p>
                    <input
                        type="text"
                        placeholder="https://www.example.com/very/long/url"
                        value={longUrl} 
                        onChange={(e) => setLongUrl(e.target.value)}/>
                </div>

                <div className="short-url-input-field">
                    <p>If you have a preference for a short URL(6 alphabet characters only), put it here:</p>
                    <input type="text" placeholder="youralias(optional)" maxLength={6}/>
                </div>

                <button type="submit" className="submit-button">Shorten URL</button>
            </form>
        </div>
    )
}

export default URLCard