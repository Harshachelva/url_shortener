# 🚀 Quick Start Guide

Get your URL Shortener up and running in 5 minutes!

## 📋 Prerequisites

- **Docker** (20.10+) - [Install](https://docs.docker.com/get-docker/)
- **Docker Compose** (2.0+) - [Install](https://docs.docker.com/compose/install/)
- **8GB RAM** minimum
- **2GB** free disk space

## ⚡ Option 1: Automated Setup (Recommended)

### 1. Run the Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

The script will:
- ✓ Check all prerequisites
- ✓ Verify port availability
- ✓ Build Docker containers
- ✓ Start all services
- ✓ Run health checks

**Done!** Open http://localhost:3000

---

## 🛠️ Option 2: Manual Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd url-shortener
```

### 2. Build and Start

**Using Make:**
```bash
make build
make up
```

**Using Docker Compose:**
```bash
docker-compose build
docker-compose up -d
```

### 3. Verify Services

```bash
# Check status
make status

# Or
docker-compose ps
```

### 4. Open the Application

- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:5001/health

---

## 📱 Usage

### Shorten a URL

1. Open http://localhost:3000
2. Enter your long URL
3. (Optional) Add a custom short code
4. Click **"Shorten URL"**
5. Copy and share!

### API Usage

```bash
# Shorten URL
curl -X POST http://localhost:5001/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/long-url"}'

# With custom code
curl -X POST http://localhost:5001/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "custom_code": "my-link"}'

# Check health
curl http://localhost:5001/health
```

---

## 🔧 Common Commands

### Using Make

```bash
make help          # Show all commands
make logs          # View logs
make status        # Check service status
make health        # Run health checks
make restart       # Restart services
make down          # Stop services
make clean         # Remove everything
```

### Using Docker Compose

```bash
docker-compose logs -f              # View logs
docker-compose ps                   # Check status
docker-compose restart              # Restart
docker-compose down                 # Stop
docker-compose down -v              # Stop and remove volumes
```

---

## 🐛 Troubleshooting

### Port Already in Use

**macOS - AirPlay on Port 5000:**
1. System Settings → General → AirDrop & Handoff
2. Turn off **AirPlay Receiver**
3. Restart: `make restart`

**Change Port:**
Edit `docker-compose.yml`:
```yaml
api:
  ports:
    - "5001:5000"  # Already using 5001 by default
```

### Services Not Starting

```bash
# Check logs
make logs

# Rebuild from scratch
make rebuild

# Or
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Connection Refused

```bash
# Wait for services to start (30 seconds)
sleep 30

# Check if services are up
make status

# Test backend directly
curl http://localhost:5001/health
```

### Database Issues

```bash
# Reset database
make db-reset

# Or reinitialize
docker-compose run --rm api python /app/init_db.py
```

---

## 📊 Verify Installation

Run comprehensive health checks:

```bash
make health
```

Expected output:
```
✓ Container Status: Running
✓ Redis: PONG
✓ Backend API: healthy
✓ Database: exists
✓ Frontend: 200 OK
```

---

## 🎯 Next Steps

1. **Read the docs:** Check `README.md` for detailed documentation
2. **Customize:** Edit `docker-compose.yml` for custom configuration
3. **Test API:** Use Postman or curl to test endpoints
4. **Monitor:** Use `make logs` to watch real-time logs
5. **Deploy:** See production deployment guide in README.md

---

## 🆘 Get Help

- **Documentation:** See `README.md`
- **Commands:** Run `make help`
- **Logs:** Run `make logs`
- **Issues:** Open an issue on GitHub

---

## 📝 File Structure

```
url-shortener/
├── setup.sh              ← Run this first!
├── Makefile              ← Convenient commands
├── docker-compose.yml    ← Container configuration
├── backend/
│   ├── app.py           ← Flask application
│   ├── init_db.py       ← Database setup
│   └── Dockerfile.api   ← Backend container
└── frontend/
    ├── src/App.js       ← React UI
    └── Dockerfile.web   ← Frontend container
```

---

## ✅ Quick Test

Test your installation:

```bash
# Test API
curl -X POST http://localhost:5001/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'

# Expected response:
# {
#   "shortened_url": "http://short.ly/1",
#   "original_url": "https://google.com",
#   "short_code": "1",
#   "custom_code_used": false
# }
```

---

## 🎉 Success!

Your URL Shortener is ready to use!

**Access Points:**
- 🌐 Web UI: http://localhost:3000
- 🔌 API: http://localhost:5001
- ❤️ Health: http://localhost:5001/health

Happy shortening! 🔗