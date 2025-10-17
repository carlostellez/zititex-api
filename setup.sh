#!/bin/bash

# Zititex API Setup Script
# This script automates the initial setup of the development environment

set -e  # Exit on error

echo "🚀 Starting Zititex API Setup..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION detected"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip --quiet
print_success "pip upgraded"

# Install dependencies
echo ""
echo "Installing dependencies..."
if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt --quiet
    print_success "Development dependencies installed"
else
    print_error "requirements-dev.txt not found"
    exit 1
fi

# Create .env file if it doesn't exist
echo ""
echo "Setting up environment variables..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success ".env file created from .env.example"
        print_info "Please update .env with your configuration"
    else
        # Create basic .env file
        cat > .env << 'EOF'
APP_NAME=Zititex API
APP_ENV=development
DEBUG=True
API_VERSION=v1
SECRET_KEY=change-me-in-production

HOST=0.0.0.0
PORT=8000
WORKERS=4

DATABASE_URL=postgresql://zititex:zititex@localhost:5432/zititex_db
DB_ECHO=False

REDIS_URL=redis://localhost:6379/0
REDIS_TTL=3600

JWT_SECRET_KEY=change-me-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_METHODS=["*"]
CORS_ALLOW_HEADERS=["*"]

LOG_LEVEL=INFO
LOG_FORMAT=json
EOF
        print_success ".env file created"
        print_info "Please update .env with your configuration"
    fi
else
    print_info ".env file already exists"
fi

# Install pre-commit hooks
echo ""
echo "Installing pre-commit hooks..."
pre-commit install --quiet
print_success "Pre-commit hooks installed"

# Check if PostgreSQL is available
echo ""
echo "Checking PostgreSQL..."
if command -v psql &> /dev/null; then
    print_success "PostgreSQL is installed"
    
    # Try to connect
    if pg_isready &> /dev/null; then
        print_success "PostgreSQL is running"
    else
        print_info "PostgreSQL is not running. Start it with: brew services start postgresql@15"
    fi
else
    print_info "PostgreSQL not found. Install with: brew install postgresql@15"
fi

# Check if Redis is available
echo ""
echo "Checking Redis..."
if command -v redis-cli &> /dev/null; then
    print_success "Redis is installed"
    
    # Try to ping
    if redis-cli ping &> /dev/null; then
        print_success "Redis is running"
    else
        print_info "Redis is not running. Start it with: brew services start redis"
    fi
else
    print_info "Redis not found. Install with: brew install redis"
fi

# Summary
echo ""
echo "================================================"
echo "Setup complete! 🎉"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Update .env with your configuration"
echo "2. Start PostgreSQL: brew services start postgresql@15"
echo "3. Start Redis: brew services start redis"
echo "4. Create database: createdb zititex_db"
echo "5. Run migrations: make migrate"
echo "6. Start the API: make run"
echo ""
echo "Available commands (see Makefile):"
echo "  make install-dev   - Install dependencies"
echo "  make run           - Run the application"
echo "  make test          - Run tests"
echo "  make format        - Format code"
echo "  make lint          - Run linters"
echo "  make docker-up     - Start with Docker"
echo ""
echo "Documentation:"
echo "  README.md          - Project overview"
echo "  run.md             - Detailed run instructions"
echo "  prompts.md         - Development guidelines"
echo "  CONTRIBUTING.md    - Contribution guidelines"
echo ""
print_success "Happy coding! 🚀"

