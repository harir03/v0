# Aether Agents Backend

FastAPI backend for the Aether Agents platform providing AI agent management and interface generation capabilities.

## Features

- **Agent Management**: Create, update, delete, and execute AI agents
- **User Authentication**: JWT-based authentication with secure password hashing
- **Database Persistence**: PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **Subscription Management**: Multi-tier subscription system with usage tracking
- **RESTful API**: Comprehensive API with automatic OpenAPI documentation
- **Security**: Production-ready security features including CORS, authentication, and authorization

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Set up Database**
   ```bash
   # Make sure PostgreSQL is running
   alembic upgrade head
   ```

4. **Run Server**
   ```bash
   python run_server.py
   ```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout
- `GET /api/v1/auth/me` - Get current user

### Agents
- `GET /api/v1/agents/` - List all agents
- `POST /api/v1/agents/` - Create new agent
- `GET /api/v1/agents/{id}` - Get specific agent
- `PUT /api/v1/agents/{id}` - Update agent
- `DELETE /api/v1/agents/{id}` - Delete agent
- `POST /api/v1/agents/{id}/execute` - Execute agent task

## Project Structure

```
app/
├── api/v1/              # API version 1
│   ├── endpoints/       # API route handlers
│   └── api.py          # API router configuration
├── core/               # Core functionality
│   ├── config.py       # Application configuration
│   ├── database.py     # Database connection
│   └── security.py     # Authentication utilities
├── models/             # SQLAlchemy models
├── schemas/            # Pydantic schemas
│   ├── agent.py        # Agent data models
│   └── user.py         # User data models
└── services/           # Business logic
    ├── agent_service.py # Agent management
    └── user_service.py  # User management
```

## Configuration

Key environment variables:

- `POSTGRES_*` - Database configuration
- `SECRET_KEY` - JWT signing key
- `REDIS_URL` - Redis connection for caching/tasks
- `OPENAI_API_KEY` - OpenAI API key
- `STRIPE_*` - Stripe payment configuration

## Development

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Downgrade
alembic downgrade -1
```

### Testing

```bash
pytest
```

## Deployment

The application is designed for production deployment with:

- Docker containerization
- Kubernetes orchestration
- Environment-based configuration
- Database migrations
- Health check endpoints

## API Documentation

When running the server, visit:
- http://localhost:8000/docs for interactive Swagger documentation
- http://localhost:8000/redoc for ReDoc documentation

## License

MIT License - see LICENSE file for details.