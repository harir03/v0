# LinkedIn Bot v1 + Aether Agents Platform

**ALWAYS follow these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Repository Overview

This repository contains two main components:
1. **LinkedIn Bot v1** - Python automation platform for multi-account LinkedIn engagement
2. **Aether Agents Platform** - Full-stack AI agent management system with FastAPI backend and Next.js frontend

## Working Effectively

### Initial Setup (Required for both components)
```bash
# Ensure Python 3.12+ and Node.js 20+ are available
python3 --version  # Should be 3.12+
node --version     # Should be v20+
```

### LinkedIn Bot v1 Setup
```bash
# Install LinkedIn bot dependencies - takes ~10 seconds
pip3 install -r requirements.txt

# Verify installation
python3 -c "import selenium, schedule, psutil, requests; print('LinkedIn bot dependencies OK')"
```

### Aether Platform Setup
```bash
# Backend setup - takes ~45 seconds. NEVER CANCEL.
cd aether/backend
pip3 install -r requirements.txt

# Fix CORS configuration (CRITICAL)
cp .env.example .env
# Edit .env and ensure CORS line looks like:
# BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001","https://aether-agents.com"]

# Verify backend imports
python3 -c "import main; print('Backend imports successful')"

# Frontend setup - takes ~13 seconds
cd ../frontend
npm install

# Build frontend - takes ~30 seconds. NEVER CANCEL.
npm run build
```

### Docker Compose Setup (Full Stack)
```bash
cd aether

# Build all services - takes 5-15 minutes. NEVER CANCEL. Set timeout to 30+ minutes.
docker compose build

# Start all services
docker compose up -d

# Access points:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Documentation: http://localhost:8000/docs
```

## Running and Testing

### LinkedIn Bot Operations
```bash
# Run v0 (simple single-account bot)
python3 v0.py
# Prompts for search query, runs interactively

# Run v1 (advanced multi-account scheduler)
python3 v1.py
# Shows menu interface with options 1-7

# Configuration
# - Edit accounts_config.json to add/modify LinkedIn accounts
# - Each account needs separate browser profile
# - Requires Chrome browser at /usr/bin/google-chrome
```

### Aether Backend Testing
```bash
cd aether/backend

# Run tests - takes ~3.5 seconds. NEVER CANCEL.
python3 -m pytest tests/ -v

# Expected results: 10 pass, 6 fail (test setup issues, not functionality)
# Start backend server (requires PostgreSQL and Redis)
uvicorn main:app --reload
```

### Aether Frontend Testing
```bash
cd aether/frontend

# Lint (requires configuration first)
npm run lint
# First run will prompt for ESLint config - choose "Strict (recommended)"

# Development server
npm run dev
# Access at http://localhost:3000

# Production build
npm run build
```

## Critical Timing and Timeouts

- **LinkedIn bot dependencies**: 10 seconds - use 60 second timeout
- **Backend dependencies**: 45 seconds - use 120 second timeout
- **Frontend dependencies**: 13 seconds - use 60 second timeout  
- **Frontend build**: 30 seconds - use 120 second timeout
- **Backend tests**: 3.5 seconds - use 30 second timeout
- **Docker Compose build**: 5-15 minutes - use 30+ minute timeout. **NEVER CANCEL DOCKER BUILDS**

## Validation Scenarios

### LinkedIn Bot Validation
```bash
# Test v1 menu interface
python3 v1.py
# Should show menu with options 1-7
# Use Ctrl+C to exit

# Verify configuration
cat accounts_config.json
# Should show valid JSON with accounts array
```

### Aether Backend Validation
```bash
cd aether/backend

# Test imports and configuration
python3 -c "import main; print('Backend configuration valid')"

# Test API endpoints (with running server)
curl http://localhost:8000/
curl http://localhost:8000/docs
```

### Aether Frontend Validation
```bash
cd aether/frontend

# Test build pipeline
npm run build
# Should complete without errors (warnings OK)

# Test development server startup
timeout 10 npm run dev
# Should start without import errors
```

### Full Stack Docker Validation
```bash
cd aether

# Test service health
docker compose ps
# All services should show "healthy" or "running"

# Test connectivity
curl http://localhost:3000
curl http://localhost:8000/docs
```

## Known Issues and Workarounds

### Backend Configuration
- **CORS Error**: Edit `.env` file, ensure `BACKEND_CORS_ORIGINS` uses JSON array format with double quotes
- **Database Required**: Backend needs PostgreSQL and Redis for full functionality
- **Import Warnings**: Security.py has regex escape sequence warnings (non-blocking)

### Frontend Setup
- **ESLint Config**: First `npm run lint` will prompt for configuration
- **Build Warnings**: Next.js metadata warnings are non-blocking
- **Dependency Audit**: npm may show vulnerability warnings (typical)

### LinkedIn Bot Limitations
- **Browser Required**: Needs Chrome at `/usr/bin/google-chrome`
- **Profile Setup**: Each account needs separate browser profile directory
- **Headless Mode**: May fall back to visible mode on failures

### Docker Issues
- **Version Warning**: `version` field in docker-compose.yml is obsolete (ignore)
- **Build Time**: Initial build downloads large images (5-15 minutes normal)

## File Structure Reference

```
/
├── v0.py                     # Simple LinkedIn bot
├── v1.py                     # Advanced LinkedIn bot  
├── accounts_config.json      # LinkedIn account configuration
├── requirements.txt          # LinkedIn bot dependencies
├── logs/                     # Bot execution logs
├── screenshots/              # Bot screenshots
├── account_histories/        # Per-account history
└── aether/                   # Full-stack platform
    ├── docker-compose.yml    # Stack orchestration
    ├── backend/              # FastAPI backend
    │   ├── main.py          # API entry point
    │   ├── requirements.txt # Backend dependencies
    │   ├── .env.example     # Configuration template
    │   ├── tests/           # Backend tests
    │   └── app/             # Application code
    └── frontend/            # Next.js frontend
        ├── package.json     # Frontend dependencies
        ├── src/             # React components
        └── Dockerfile       # Frontend container
```

## Pre-commit Validation

Always run these commands before committing changes:

```bash
# For LinkedIn bot changes
python3 -c "import v0, v1; print('Python syntax OK')"

# For backend changes
cd aether/backend
python3 -c "import main; print('Backend imports OK')"
python3 -m pytest tests/ --tb=short

# For frontend changes  
cd aether/frontend
npm run build
npm run lint

# For full stack changes
cd aether
docker compose build --no-cache
```

## Common Commands Reference

```bash
# Repository status
git status && ls -la

# Component health check
python3 --version && node --version && docker --version

# Quick dependency install
pip3 install -r requirements.txt && cd aether/backend && pip3 install -r requirements.txt && cd ../frontend && npm install && cd ../..

# Quick build validation
cd aether/frontend && npm run build && cd ../backend && python3 -c "import main" && cd ../..

# Full stack startup
cd aether && docker compose up -d && cd ..
```