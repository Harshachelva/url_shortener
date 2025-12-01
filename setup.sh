#!/bin/bash

# URL Shortener - Automated Setup Script
# This script will guide you through setting up the URL shortener application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print colored messages
print_header() {
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║$1║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main setup function
main() {
    clear
    print_header "        URL Shortener - Automated Setup                 "
    echo ""

    # Step 1: Check prerequisites
    echo -e "${YELLOW}[1/6] Checking prerequisites...${NC}"
    echo ""

    # Check Docker
    if command_exists docker; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        print_success "Docker installed (version $DOCKER_VERSION)"
    else
        print_error "Docker is not installed"
        echo "Please install Docker from: https://docs.docker.com/get-docker/"
        exit 1
    fi

    # Check Docker Compose
    if command_exists docker-compose; then
        COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f4 | cut -d',' -f1)
        print_success "Docker Compose installed (version $COMPOSE_VERSION)"
    else
        print_error "Docker Compose is not installed"
        echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
        exit 1
    fi

    # Check if Docker daemon is running
    if docker info >/dev/null 2>&1; then
        print_success "Docker daemon is running"
    else
        print_error "Docker daemon is not running"
        echo "Please start Docker and try again"
        exit 1
    fi

    # Check Make (optional)
    if command_exists make; then
        print_success "Make is installed (optional but recommended)"
    else
        print_warning "Make is not installed (optional)"
    fi

    echo ""

    # Step 2: Check port availability
    echo -e "${YELLOW}[2/6] Checking port availability...${NC}"
    echo ""

    # Function to check if port is in use
    check_port() {
        if command_exists lsof; then
            lsof -i :$1 >/dev/null 2>&1
        elif command_exists netstat; then
            netstat -tuln | grep ":$1 " >/dev/null 2>&1
        else
            # Can't check, assume it's free
            return 1
        fi
    }

    PORTS_OK=true

    if check_port 5001; then
        print_warning "Port 5001 (Backend) is already in use"
        PORTS_OK=false
    else
        print_success "Port 5001 (Backend) is available"
    fi

    if check_port 3000; then
        print_warning "Port 3000 (Frontend) is already in use"
        PORTS_OK=false
    else
        print_success "Port 3000 (Frontend) is available"
    fi

    if check_port 6379; then
        print_warning "Port 6379 (Redis) is already in use"
        PORTS_OK=false
    else
        print_success "Port 6379 (Redis) is available"
    fi

    if [ "$PORTS_OK" = false ]; then
        echo ""
        print_warning "Some ports are in use. You may need to stop those services or change ports in docker-compose.yml"
        echo -n "Do you want to continue anyway? [y/N] "
        read -r response
        if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            echo "Setup cancelled"
            exit 0
        fi
    fi

    echo ""

    # Step 3: Verify project structure
    echo -e "${YELLOW}[3/6] Verifying project structure...${NC}"
    echo ""

    STRUCTURE_OK=true

    # Check required files
    if [ -f "docker-compose.yml" ]; then
        print_success "docker-compose.yml found"
    else
        print_error "docker-compose.yml not found"
        STRUCTURE_OK=false
    fi

    if [ -f "Makefile" ]; then
        print_success "Makefile found"
    else
        print_warning "Makefile not found (optional)"
    fi

    # Check backend files
    if [ -d "backend" ]; then
        print_success "backend/ directory found"
        
        if [ -f "backend/app.py" ]; then
            print_success "backend/app.py found"
        else
            print_error "backend/app.py not found"
            STRUCTURE_OK=false
        fi

        if [ -f "backend/init_db.py" ]; then
            print_success "backend/init_db.py found"
        else
            print_error "backend/init_db.py not found"
            STRUCTURE_OK=false
        fi

        if [ -f "backend/requirements.txt" ]; then
            print_success "backend/requirements.txt found"
        else
            print_error "backend/requirements.txt not found"
            STRUCTURE_OK=false
        fi

        if [ -f "backend/Dockerfile.api" ]; then
            print_success "backend/Dockerfile.api found"
        else
            print_error "backend/Dockerfile.api not found"
            STRUCTURE_OK=false
        fi
    else
        print_error "backend/ directory not found"
        STRUCTURE_OK=false
    fi

    # Check frontend files
    if [ -d "frontend" ]; then
        print_success "frontend/ directory found"
        
        if [ -f "frontend/package.json" ]; then
            print_success "frontend/package.json found"
        else
            print_error "frontend/package.json not found"
            STRUCTURE_OK=false
        fi

        if [ -f "frontend/Dockerfile.web" ]; then
            print_success "frontend/Dockerfile.web found"
        else
            print_error "frontend/Dockerfile.web not found"
            STRUCTURE_OK=false
        fi

        if [ -d "frontend/src" ]; then
            print_success "frontend/src/ directory found"
        else
            print_error "frontend/src/ directory not found"
            STRUCTURE_OK=false
        fi

        if [ -d "frontend/public" ]; then
            print_success "frontend/public/ directory found"
        else
            print_error "frontend/public/ directory not found"
            STRUCTURE_OK=false
        fi
    else
        print_error "frontend/ directory not found"
        STRUCTURE_OK=false
    fi

    if [ "$STRUCTURE_OK" = false ]; then
        echo ""
        print_error "Project structure is incomplete. Please ensure all required files are present."
        exit 1
    fi

    echo ""

    # Step 4: Build containers
    echo -e "${YELLOW}[4/6] Building Docker containers...${NC}"
    echo ""
    print_info "This may take a few minutes on first run..."
    echo ""

    if docker-compose build; then
        print_success "Docker containers built successfully"
    else
        print_error "Failed to build Docker containers"
        exit 1
    fi

    echo ""

    # Step 5: Start services
    echo -e "${YELLOW}[5/6] Starting services...${NC}"
    echo ""

    if docker-compose up -d; then
        print_success "Services started successfully"
    else
        print_error "Failed to start services"
        exit 1
    fi

    echo ""
    print_info "Waiting for services to be ready..."
    sleep 5

    echo ""

    # Step 6: Health checks
    echo -e "${YELLOW}[6/6] Running health checks...${NC}"
    echo ""

    # Check backend
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/health | grep -q "200"; then
        print_success "Backend API is healthy"
    else
        print_warning "Backend API is not responding yet (may need more time)"
    fi

    # Check frontend
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
        print_success "Frontend is healthy"
    else
        print_warning "Frontend is not responding yet (may need more time)"
    fi

    # Check Redis
    if docker exec redis-server redis-cli ping >/dev/null 2>&1; then
        print_success "Redis is healthy"
    else
        print_warning "Redis is not responding"
    fi

    echo ""
    echo ""

    # Success message
    print_header "              Setup Complete! 🎉                         "
    echo ""
    echo -e "${GREEN}Your URL Shortener is now running!${NC}"
    echo ""
    echo -e "${CYAN}Access URLs:${NC}"
    echo -e "  Frontend:  ${GREEN}http://localhost:3000${NC}"
    echo -e "  Backend:   ${GREEN}http://localhost:5001${NC}"
    echo -e "  Health:    ${GREEN}http://localhost:5001/health${NC}"
    echo ""
    echo -e "${CYAN}Useful Commands:${NC}"
    
    if command_exists make; then
        echo -e "  ${YELLOW}make logs${NC}      - View logs"
        echo -e "  ${YELLOW}make status${NC}    - Check service status"
        echo -e "  ${YELLOW}make health${NC}    - Run health checks"
        echo -e "  ${YELLOW}make down${NC}      - Stop services"
        echo -e "  ${YELLOW}make help${NC}      - Show all available commands"
    else
        echo -e "  ${YELLOW}docker-compose logs -f${NC}     - View logs"
        echo -e "  ${YELLOW}docker-compose ps${NC}          - Check service status"
        echo -e "  ${YELLOW}docker-compose down${NC}        - Stop services"
    fi
    
    echo ""
    echo -e "${CYAN}Documentation:${NC}"
    echo -e "  Read ${YELLOW}README.md${NC} for detailed documentation"
    echo ""
    
    # Ask to open browser
    echo -n "Would you like to open the application in your browser? [Y/n] "
    read -r response
    if [[ "$response" =~ ^([nN][oO]|[nN])$ ]]; then
        echo ""
        echo "You can manually visit: http://localhost:3000"
    else
        echo ""
        print_info "Opening browser..."
        if command_exists open; then
            open http://localhost:3000
        elif command_exists xdg-open; then
            xdg-open http://localhost:3000
        else
            echo "Please manually visit: http://localhost:3000"
        fi
    fi

    echo ""
    echo -e "${GREEN}Happy URL shortening! 🔗${NC}"
    echo ""
}

# Run main function
main