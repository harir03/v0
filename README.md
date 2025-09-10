# Aether Agents - Production-Ready AI Agents Platform

A production-ready, enterprise-grade AI agents platform that competes with Lindy AI. Built with modern technologies for scalability, security, and enterprise deployment.

## 🚀 Overview

Aether Agents transforms businesses with intelligent automation through:

- **🤖 AI Agent Management**: Create, deploy, and monitor AI agents
- **⚡ Scalable Execution**: Async task processing with Celery + Redis
- **🔒 Enterprise Security**: Production-ready security and compliance
- **📊 Advanced Monitoring**: Prometheus metrics and structured logging
- **🎨 Modern UI**: React frontend with smooth animations
- **🐳 Container Ready**: Docker deployment with orchestration support

## 🏗️ Architecture

### Technology Stack

**Backend:**
- FastAPI with async support
- SQLAlchemy ORM + PostgreSQL
- Celery task queue with Redis
- JWT authentication
- Prometheus monitoring
- Structured logging

**Frontend:**
- React 18 with TypeScript
- Tailwind CSS + Framer Motion
- React Query for state management
- JWT-based authentication
- Responsive design

**Infrastructure:**
- Docker containerization
- Docker Compose for development
- Health checks for orchestration
- Prometheus metrics
- Structured logging

### Service Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React App     │    │   FastAPI       │    │   PostgreSQL    │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
                               ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Celery        │◄──►│     Redis       │
                       │   (Workers)     │    │   (Queue/Cache) │
                       └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)

### Development Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/harir03/v0.git
   cd v0
   ```

2. **Backend Setup**
   ```bash
   cd aether/backend
   
   # Copy environment file
   cp .env.example .env
   
   # Start services with Docker Compose
   docker-compose up -d
   
   # Run migrations
   docker-compose exec backend alembic upgrade head
   ```

3. **Frontend Setup**
   ```bash
   cd aether/frontend
   
   # Install dependencies
   npm install
   
   # Start development server
   npm start
   ```

4. **Access Applications**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Celery Flower: http://localhost:5555

## 🎯 Features

### Core Platform Features

- **Agent Management**: Full CRUD operations for AI agents
- **Async Execution**: Scalable task processing with Celery
- **Real-time Dashboard**: Monitor agent performance and executions
- **User Authentication**: JWT-based auth with protected routes
- **Subscription Tiers**: Free, Startup, Scale-Up, Enterprise plans

### Production Features

- **Monitoring**: Prometheus metrics and structured logging
- **Security**: Rate limiting, security headers, error handling
- **Health Checks**: Kubernetes-ready health and readiness checks
- **Container Support**: Docker deployment with compose
- **AI Integration**: OpenAI and Anthropic API support

### Enterprise Features

- **Multi-tenant**: User isolation and resource management
- **Audit Logging**: Comprehensive activity tracking
- **Security**: Production-ready security middleware
- **Scalability**: Horizontal scaling with container orchestration
- **Compliance**: GDPR/SOC2 ready architecture

## 📊 Pricing Tiers

| Feature | Hobbyist | Startup | Scale-Up | Enterprise |
|---------|----------|---------|----------|------------|
| **Price** | Free | $49/month | $199/month | Custom |
| **User Seats** | 1 | 3 | 10 | Unlimited |
| **Active Agents** | 2 | 10 | Unlimited | Unlimited |
| **Tasks/Month** | 500 | 5,000 | 50,000 | Custom |
| **Integrations** | Basic | Premium | Advanced | Custom |
| **Support** | Community | Priority | Dedicated | 24/7 Premium |

## 🔧 API Documentation

### Authentication Endpoints

```bash
POST /api/v1/auth/register     # User registration
POST /api/v1/auth/login        # User login
GET  /api/v1/auth/me          # Current user info
POST /api/v1/auth/logout      # User logout
```

### Agent Management

```bash
GET    /api/v1/agents/                 # List agents
POST   /api/v1/agents/                 # Create agent
GET    /api/v1/agents/{id}             # Get agent
PUT    /api/v1/agents/{id}             # Update agent
DELETE /api/v1/agents/{id}             # Delete agent
POST   /api/v1/agents/{id}/execute     # Execute agent
```

### Health & Monitoring

```bash
GET /api/v1/health              # Basic health check
GET /api/v1/health/detailed     # Detailed service health
GET /api/v1/health/ready        # Kubernetes readiness
GET /api/v1/health/live         # Kubernetes liveness
GET /api/v1/metrics             # Prometheus metrics
```

## 🐳 Deployment

### Docker Compose (Development)

```bash
cd aether/backend
docker-compose up -d
```

### Production Deployment

1. **Configure Environment**
   ```bash
   # Update .env with production values
   SECRET_KEY=your-secure-secret-key
   POSTGRES_PASSWORD=secure-password
   OPENAI_API_KEY=your-api-key
   ```

2. **Deploy with Docker**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Run Migrations**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

### Kubernetes Deployment

```yaml
# Example Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aether-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: aether-backend
  template:
    metadata:
      labels:
        app: aether-backend
    spec:
      containers:
      - name: backend
        image: aether/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: POSTGRES_SERVER
          value: "postgres-service"
        livenessProbe:
          httpGet:
            path: /api/v1/health/live
            port: 8000
        readinessProbe:
          httpGet:
            path: /api/v1/health/ready
            port: 8000
```

## 📈 Monitoring

### Prometheus Metrics

- HTTP request metrics (duration, count, status codes)
- Agent execution metrics (count, duration, success rate)
- System health metrics (database, Redis, Celery)
- User activity metrics

### Structured Logging

```json
{
  "timestamp": "2024-08-26T22:00:00Z",
  "level": "info",
  "event": "agent_execution",
  "agent_id": "uuid",
  "agent_type": "customer_support",
  "status": "completed",
  "duration": 1.23,
  "user_id": "uuid"
}
```

### Health Checks

- `/health` - Basic API health
- `/health/detailed` - All service dependencies
- `/health/ready` - Kubernetes readiness probe
- `/health/live` - Kubernetes liveness probe

## 🔒 Security

### Authentication & Authorization

- JWT token-based authentication
- Secure password hashing with bcrypt
- Protected API routes
- User session management

### Security Middleware

- Rate limiting (100 requests/minute per client)
- Security headers (XSS, CSRF protection)
- CORS configuration
- Request/response monitoring

### Data Protection

- Encrypted database connections
- Secure environment variable handling
- Input validation and sanitization
- Audit logging for compliance

## 🚀 Development

### Backend Development

```bash
cd aether/backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start development server
python run_server.py

# Start Celery worker
celery -A app.core.celery_app worker --loglevel=info
```

### Frontend Development

```bash
cd aether/frontend

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

### Testing

```bash
# Backend tests
cd aether/backend
pytest

# Frontend tests
cd aether/frontend
npm test
```

## 📝 Environment Variables

### Backend Configuration

```bash
# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=aether_user
POSTGRES_PASSWORD=aether_password
POSTGRES_DB=aether_agents

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=11520

# AI Providers
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Frontend Configuration

```bash
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## 🎭 Demo & Screenshots

### Landing Page
Professional marketing site with interactive demo, pricing tiers, and smooth animations.

### Dashboard
Real-time agent management with execution monitoring, statistics, and intuitive controls.

### Agent Creation
Simple form-based agent creation with type selection and configuration options.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with modern technologies for enterprise deployment
- Inspired by Lindy AI and other AI automation platforms
- Designed for scalability and production readiness

---

**Ready to transform your business with AI agents?** [Get Started](http://localhost:3000) today!