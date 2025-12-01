# 📦 Installation Guide

Complete step-by-step installation guide for the URL Shortener.

## 📋 Pre-Installation Checklist

- [ ] Docker installed (20.10+)
- [ ] Docker Compose installed (2.0+)
- [ ] Git installed
- [ ] 8GB RAM available
- [ ] 2GB free disk space
- [ ] Ports 3000, 5001, 6379 are available

## 🔧 Step-by-Step Installation

### Step 1: Install Docker

**macOS:**
```bash
# Download from Docker website
open https://docs.docker.com/desktop/mac/install/

# Or use Homebrew
brew install --cask docker
```

**Linux (Ubuntu/Debian):**
```bash
# Update packages
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in for changes to take effect
```

**Windows:**
```bash
# Download from Docker website
# https://docs.docker.com/desktop/windows/install/
```

**Verify Docker:**
```bash
docker --version
docker-compose --version
```

### Step 2: Check Port Availability

**macOS/Linux:**
```bash
# Check if ports are free
lsof -i :3000
lsof -i :5001
lsof -i :6379

# If port 5000 is used by AirPlay (macOS):
# System Settings → General → AirDrop & Handoff
# Turn off "AirPlay Receiver"
```

**Windows:**
```powershell
netstat -ano | findstr :3000
netstat -ano | findstr :5001
netstat -ano | findstr :6379
```

### Step 3: Clone the Repository

```bash
# Clone the repo
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener

# Verify files
ls -la
```

### Step 4: Project Structure Setup

Ensure you have this structure:

```
url-shortener/
├── backend/
│   ├── app.py
│   ├── init_db.py
│   ├── requirements.txt
│   └── Dockerfile.api
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── index.js
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── Dockerfile.web
├── docker-compose.yml
├── Makefile
├── setup.sh
└── README.md
```

### Step 5: Configure Environment (Optional)

Create `.env` file if you want custom configuration:

```bash
cat > .env << EOF
# Backend
REDIS_HOST=redis
REDIS_PORT=6379
DB_PATH=/app/data/shortener.db
FLASK_ENV=development

# Frontend
REACT_APP_API_URL=http://localhost:5001
EOF
```

### Step 6: Run Setup

**Option A: Automated Setup (Recommended)**
```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

**Option B: Manual Setup**
```bash
# Using Make
make build
make up

# Using Docker Compose
docker-compose build
docker-compose up -d
```

### Step 7: Wait for Services

```bash
# Wait 30 seconds for all services to start
sleep 30

# Check status
make status

# Or
docker-compose ps
```

### Step 8: Verify Installation

```bash
# Run health checks
make health

# Or manual checks
curl http://localhost:5001/health
curl http://localhost:3000
docker exec redis-server redis-cli ping
```

### Step 9: Test the Application

**Web UI Test:**
1. Open http://localhost:3000
2. Enter a URL
3. Click "Shorten URL"
4. Verify you get a shortened link

**API Test:**
```bash
curl -X POST http://localhost:5001/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

Expected response:
```json
{
  "shortened_url": "http://short.ly/1",
  "original_url": "https://www.google.com",
  "short_code": "1",
  "custom_code_used": false
}
```

## ✅ Post-Installation Checklist

- [ ] All containers running (`docker-compose ps`)
- [ ] Backend health check passes
- [ ] Frontend loads in browser
- [ ] Redis responding to ping
- [ ] Database file created
- [ ] Can shorten URLs via web UI
- [ ] Can shorten URLs via API

## 🔧 Troubleshooting Installation

### Issue: Docker daemon not running

**Solution:**
```bash
# macOS
open -a Docker

# Linux
sudo systemctl start docker

# Verify
docker info
```

### Issue: Permission denied

**Solution:**
```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER
newgrp docker

# Or run with sudo
sudo docker-compose up -d
```

### Issue: Port already in use

**Solution:**
```bash
# Find process using port
lsof -i :5001  # macOS/Linux
netstat -ano | findstr :5001  # Windows

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Issue: Build fails

**Solution:**
```bash
# Clean and rebuild
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up -d
```

### Issue: Services won't start

**Solution:**
```bash
# Check logs
docker-compose logs

# Restart specific service
docker-compose restart api

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

### Issue: Frontend shows CORS error

**Solution:**
1. Verify backend is running: `curl http://localhost:5001/health`
2. Check `app.py` has CORS enabled
3. Verify API_URL in `App.js` matches backend port
4. Restart services: `make restart`

### Issue: Database not found

**Solution:**
```bash
# Initialize database
docker-compose run --rm api python /app/init_db.py

# Verify
docker exec flask-api ls -la /app/data/
```

## 🔄 Updating the Application

### Pull Latest Changes

```bash
# Pull from git
git pull origin main

# Rebuild containers
make rebuild

# Or
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Update Dependencies

**Backend:**
```bash
# Edit backend/requirements.txt
# Then rebuild
docker-compose build api
docker-compose up -d api
```

**Frontend:**
```bash
# Edit frontend/package.json
# Then rebuild
docker-compose build frontend
docker-compose up -d frontend
```

## 🗑️ Uninstallation

### Remove Everything

```bash
# Stop and remove containers
docker-compose down -v

# Remove images
docker rmi url-shortener_api url-shortener_frontend

# Remove project directory
cd ..
rm -rf url-shortener

# Clean Docker system
docker system prune -a
```

### Keep Data, Remove Containers

```bash
# Just stop containers
docker-compose down

# Restart later
docker-compose up -d
```

## 🚀 Next Steps

After successful installation:

1. **Read Documentation:** Check `README.md` for features
2. **Learn Commands:** Run `make help` for available commands
3. **Customize:** Edit configuration files as needed
4. **Test API:** Use Postman to test endpoints
5. **Monitor:** Use `make logs` to watch application behavior

## 📞 Support

If you encounter issues:

1. Check logs: `make logs`
2. Run health checks: `make health`
3. Review troubleshooting section
4. Open an issue on GitHub
5. Check existing issues for solutions

## 📚 Additional Resources

- **Docker Documentation:** https://docs.docker.com
- **Flask Documentation:** https://flask.palletsprojects.com
- **React Documentation:** https://reactjs.org
- **Redis Documentation:** https://redis.io/documentation

---

**Installation complete!** 🎉

Your URL Shortener is ready to use at http://localhost:3000