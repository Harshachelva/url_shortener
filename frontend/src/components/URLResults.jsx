function URLResults({ originalUrl, shortUrl }) {
  return (
    <div className="url-results">
      <h3>Original URL:</h3>
      <p>{originalUrl}</p>

      <h3>Shortened URL:</h3>
      <p>{shortUrl}</p>
    </div>
  );
}

export default URLResults;