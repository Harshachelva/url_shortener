# 🔗 URL Shortener

A modern, production-ready URL shortener built with React, Flask, Redis, and SQLite. Features collision-free Base62 encoding, custom short codes, and a beautiful user interface.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)

## ✨ Features

- ⚡ **Lightning Fast** - Redis-backed atomic counters for instant URL generation
- 🎨 **Custom Short Codes** - Create personalized memorable links
- 🔒 **Collision-Free** - Base62 encoding with atomic operations
- 💎 **Beautiful UI** - Modern, responsive React interface with Tailwind CSS
- 🐳 **Docker Ready** - Full containerization with Docker Compose
- 🔄 **Auto-Retry** - Built-in retry logic for reliability
- 📊 **Health Monitoring** - Comprehensive health check endpoints
- 🌐 **CORS Enabled** - Ready for cross-origin requests

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌──────────────┐
│  React Frontend │─────▶│  Flask Backend   │─────▶│   SQLite DB  │
│   Port 3000     │      │    Port 5001     │      │              │
└─────────────────┘      └──────────────────┘      └──────────────┘
                                  │
                                  ▼
                         ┌──────────────┐
                         │ Redis Counter│
                         │  Port 6379   │
                         └──────────────┘
```

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🚀 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (20.10+) - [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (2.0+) - [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Make** (Optional but recommended) - Usually pre-installed on macOS/Linux
- **Git** - [Install Git](https://git-scm.com/downloads)

**Note for macOS users:** If port 5000 is in use by AirPlay Receiver:
- Disable it in: System Settings → General → AirDrop & Handoff → Turn off AirPlay Receiver
- Or the application uses port 5001 by default

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd url-shortener
```

### 2. Start the Application

**Using Make (Recommended):**
```bash
make build    # Build all containers
make up       # Start all services
make logs     # View logs (optional)
```

**Using Docker Compose:**
```bash
docker-compose build
docker-compose up -d
docker-compose logs -f
```

### 3. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5001
- **Health Check:** http://localhost:5001/health

### 4. Test It Out!

1. Open http://localhost:3000 in your browser
2. Enter a long URL (e.g., `https://www.example.com/very-long-url`)
3. Optionally add a custom short code
4. Click "Shorten URL"
5. Copy and share your shortened link!

## 📁 Project Structure

```
url-shortener/
├── backend/
│   ├── Dockerfile.api          # Backend Docker configuration
│   ├── app.py                  # Main Flask application
│   ├── init_db.py             # Database initialization script
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── Dockerfile.web         # Frontend Docker configuration
│   ├── package.json           # Node.js dependencies
│   ├── public/
│   │   └── index.html        # HTML template
│   └── src/
│       ├── App.js            # Main React component
│       └── index.js          # React entry point
├── docker-compose.yml         # Multi-container orchestration
├── Makefile                   # Convenient commands
├── README.md                  # This file
└── .gitignore                # Git ignore rules
```

## ⚙️ Configuration

### Environment Variables

**Backend (Flask):**
- `REDIS_HOST` - Redis server hostname (default: `redis`)
- `REDIS_PORT` - Redis port (default: `6379`)
- `DB_PATH` - SQLite database path (default: `/app/data/shortener.db`)
- `FLASK_ENV` - Flask environment (default: `development`)

**Frontend (React):**
- `REACT_APP_API_URL` - Backend API URL (default: `http://localhost:5001`)

### Port Configuration

If you need to change ports, update `docker-compose.yml`:

```yaml
services:
  api:
    ports:
      - "YOUR_PORT:5000"  # Change YOUR_PORT to desired port
  frontend:
    ports:
      - "YOUR_PORT:3000"  # Change YOUR_PORT to desired port
```

## 📚 API Documentation

### Base URL
```
http://localhost:5001
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "redis": "connected",
  "database": "connected"
}
```

---

#### 2. Root Endpoint
```http
GET /
```

**Response:**
```json
{
  "status": "running",
  "service": "URL Shortener API",
  "version": "1.0"
}
```

---

#### 3. Shorten URL
```http
POST /shorten
Content-Type: application/json
```

**Request Body:**
```json
{
  "url": "https://example.com/very-long-url",
  "custom_code": "my-link"  // Optional
}
```

**Response (201 Created):**
```json
{
  "shortened_url": "http://short.ly/my-link",
  "original_url": "https://example.com/very-long-url",
  "short_code": "my-link",
  "custom_code_used": true
}
```

**Error Responses:**
- `400 Bad Request` - Invalid URL format or missing URL
- `409 Conflict` - Custom code already exists

---

#### 4. Redirect to Original URL
```http
GET /{short_code}
```

**Response:**
- `302 Found` - Redirects to original URL
- `404 Not Found` - Short code doesn't exist

---

#### 5. Get URL Statistics
```http
GET /stats/{short_code}
```

**Response (200 OK):**
```json
{
  "short_code": "my-link",
  "original_url": "https://example.com/very-long-url",
  "shortened_url": "http://short.ly/my-link"
}
```

**Error Response:**
- `404 Not Found` - Short code doesn't exist

## 🛠️ Development

### Running Locally Without Docker

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

### Make Commands

```bash
make help          # Show all available commands
make build         # Build all Docker containers
make up            # Start all services
make down          # Stop all services
make restart       # Restart all services
make logs          # View logs from all services
make logs-api      # View backend logs only
make logs-frontend # View frontend logs only
make logs-redis    # View Redis logs only
make clean         # Remove all containers and volumes
make rebuild       # Clean and rebuild everything
make status        # Show service status
make health        # Run health checks
make test-api      # Test API endpoints
make shell-api     # Access backend container shell
make shell-redis   # Access Redis CLI
```

### Viewing Logs

```bash
# All services
make logs

# Specific service
make logs-api
make logs-frontend
make logs-redis

# Follow logs in real-time
docker-compose logs -f

# Last 50 lines
docker-compose logs --tail=50
```

## 🧪 Testing

### Test API with cURL

```bash
# Health check
curl http://localhost:5001/health

# Shorten a URL
curl -X POST http://localhost:5001/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com"}'

# With custom code
curl -X POST http://localhost:5001/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com", "custom_code": "test"}'

# Get stats
curl http://localhost:5001/stats/test

# Test redirect
curl -I http://localhost:5001/test
```

### Automated Testing

```bash
make test-api
```

### Load Testing (Optional)

Using Apache Bench:
```bash
ab -n 1000 -c 10 -p data.json -T application/json \
  http://localhost:5001/shorten
```

## 🚢 Production Deployment

### Recommended Changes for Production

1. **Use PostgreSQL instead of SQLite**
   - Better concurrency handling
   - Suitable for high traffic

2. **Enable Redis Persistence**
   ```yaml
   redis:
     command: redis-server --appendonly yes --requirepass YOUR_PASSWORD
   ```

3. **Add Environment-Specific Configs**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

4. **Use Production WSGI Server**
   - Replace Flask development server with Gunicorn
   ```dockerfile
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

5. **Set Up SSL/TLS**
   - Use nginx as reverse proxy
   - Enable HTTPS with Let's Encrypt

6. **Implement Rate Limiting**
   - Add Flask-Limiter
   - Protect against abuse

7. **Add Monitoring**
   - Prometheus + Grafana
   - Application logging
   - Error tracking (Sentry)

8. **Backup Strategy**
   - Regular database backups
   - Redis snapshots

### Docker Production Build

```dockerfile
# Use multi-stage builds
FROM python:3.11-slim as builder
# ... build steps

FROM python:3.11-slim
COPY --from=builder /app /app
CMD ["gunicorn", "app:app"]
```

## 🔧 Troubleshooting

### Port Already in Use

**Problem:** Port 5000 or 5001 is already in use

**Solution:**
```bash
# Find process using the port
lsof -i :5001
# Or on Linux
netstat -tulpn | grep :5001

# Kill the process
kill -9 <PID>

# Or change the port in docker-compose.yml
```

---

### Services Won't Start

**Problem:** Docker containers failing to start

**Solution:**
```bash
# Check logs
docker-compose logs

# Rebuild from scratch
make clean
make rebuild

# Check Docker daemon
docker info
```

---

### Redis Connection Error

**Problem:** Backend can't connect to Redis

**Solution:**
```bash
# Check Redis is running
docker-compose ps redis

# Test Redis connection
docker exec redis-server redis-cli ping

# Restart Redis
docker-compose restart redis
```

---

### Database Not Found

**Problem:** SQLite database doesn't exist

**Solution:**
```bash
# Reinitialize database
docker-compose run --rm api python /app/init_db.py

# Check database exists
docker exec flask-api ls -la /app/data/
```

---

### CORS Errors

**Problem:** Frontend can't connect to backend

**Solution:**
1. Verify backend is running: `curl http://localhost:5001/health`
2. Check CORS is enabled in `app.py`
3. Ensure API_URL in `App.js` matches backend port
4. Restart both services: `make restart`

---

### Frontend Build Errors

**Problem:** React app won't compile

**Solution:**
```bash
# Clear node_modules and rebuild
docker-compose down
docker-compose build --no-cache frontend
docker-compose up -d

# Check for file naming issues (App.js vs app.js)
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- **Python:** Follow PEP 8
- **JavaScript:** Use ESLint with Airbnb config
- **Commits:** Use conventional commits format

## 📝 How It Works

### Short Code Generation

**Auto-Generated:**
1. Redis atomic counter increments: `INCR url_id_counter`
2. Counter value (e.g., 12345) encoded to Base62: `"dnh"`
3. Guaranteed uniqueness, no collisions

**Custom Codes:**
1. User provides custom short code
2. Validated (3-20 chars, alphanumeric + hyphens)
3. Checked for uniqueness in database

### Base62 Encoding

Base62 uses: `0-9`, `a-z`, `A-Z` (62 characters)

**Benefits:**
- URL-safe characters only
- Compact representation
- Human-readable codes

**Examples:**
- `1` → `"1"`
- `62` → `"10"`
- `12345` → `"dnh"`
- `3844` → `"100"`

### Storage Flow

```
1. Request → Validate URL
2. Generate/Validate short code
3. Store in SQLite: (short_code → original_url)
4. Return shortened URL
```

### Retrieval Flow

```
1. User visits: short.ly/abc123
2. Backend looks up "abc123"
3. Retrieves original URL
4. HTTP 302 redirect
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [React](https://reactjs.org/) - Frontend library
- [Redis](https://redis.io/) - In-memory data store
- [Docker](https://www.docker.com/) - Containerization
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
- [Lucide Icons](https://lucide.dev/) - Icon library

## 📞 Support

For issues and questions:
- Open an [Issue](https://github.com/yourusername/url-shortener/issues)
- Email: your.email@example.com
- Documentation: [Wiki](https://github.com/yourusername/url-shortener/wiki)

## 🗺️ Roadmap

- [ ] Analytics dashboard
- [ ] QR code generation
- [ ] Link expiration
- [ ] User authentication
- [ ] API rate limiting
- [ ] Custom domains
- [ ] Click tracking
- [ ] Bulk URL shortening
- [ ] API key management
- [ ] Export/Import functionality

---

**Made with ❤️ by [Your Name]**

⭐ Star this repo if you find it helpful!