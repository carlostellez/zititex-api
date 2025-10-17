# Quick Start Guide

Get up and running with Zititex API in minutes!

## 🚀 Fast Setup (Recommended)

### Option 1: Automated Setup

Run the setup script:

```bash
./setup.sh
```

This will:
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Set up pre-commit hooks
- ✅ Create .env file
- ✅ Check for PostgreSQL and Redis

### Option 2: Docker (Fastest)

```bash
# Start all services with Docker Compose
docker-compose up --build

# API will be available at http://localhost:8000
# Docs at http://localhost:8000/v1/docs
```

Done! Your API is running. 🎉

### Option 3: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements-dev.txt

# 3. Set up environment
cp .env.example .env  # Edit with your settings

# 4. Install pre-commit hooks
pre-commit install

# 5. Start dependencies (or use Docker)
# Start PostgreSQL and Redis

# 6. Create database
createdb zititex_db

# 7. Run the API
uvicorn src.main:app --reload
```

## 📋 Prerequisites

Choose your setup method:

### For Docker Setup
- Docker
- Docker Compose

### For Local Setup
- Python 3.12+
- PostgreSQL 15+
- Redis 7+

## 🔍 Verify Installation

### Check API is Running

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "v1"
}
```

### Access API Documentation

Open your browser:
- **Swagger UI**: http://localhost:8000/v1/docs
- **ReDoc**: http://localhost:8000/v1/redoc

### Run Tests

```bash
pytest -v
```

All tests should pass! ✅

## 🛠️ Common Commands

```bash
# Start API
make run

# Run tests
make test

# Format code
make format

# Run linters
make lint

# Start with Docker
make docker-up

# Stop Docker
make docker-down
```

## 📚 Next Steps

1. **Read the Documentation**
   - [README.md](README.md) - Full documentation
   - [run.md](run.md) - Detailed instructions
   - [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guide

2. **Explore the API**
   - Visit http://localhost:8000/v1/docs
   - Try the health check endpoints
   - Review the code structure

3. **Start Developing**
   - Create a new feature branch
   - Follow Clean Architecture
   - Write tests (>99% coverage)
   - Submit a pull request

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Kill process on port 8000
lsof -i :8000
kill -9 <PID>
```

### Database Connection Error

```bash
# Check PostgreSQL is running
pg_isready

# Start PostgreSQL
brew services start postgresql@15  # macOS
sudo systemctl start postgresql    # Linux
```

### Redis Connection Error

```bash
# Check Redis is running
redis-cli ping

# Start Redis
brew services start redis           # macOS
sudo systemctl start redis          # Linux
```

### Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements-dev.txt
```

## 💡 Tips

- Use **Docker** for quickest setup
- Use **Makefile** for common commands
- Enable **pre-commit hooks** for quality
- Run **tests** before committing
- Read **prompts.md** for patterns

## 🆘 Need Help?

- **Documentation**: Check [run.md](run.md) for detailed instructions
- **Issues**: Open an issue on GitHub
- **Questions**: Use GitHub Discussions

---

**Ready to build something amazing!** 🚀

For detailed information, see [README.md](README.md) and [run.md](run.md).

