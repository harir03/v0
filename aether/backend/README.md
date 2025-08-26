# Aether Agents Backend

FastAPI backend for the Aether Agents platform providing AI agent management and interface generation capabilities.

## Features

- **REST API**: Comprehensive API for agent management
- **AI Integration**: Support for OpenAI, Anthropic, and Google AI models
- **Interface Generation**: AI-powered UI generation from natural language
- **Agent Execution**: Execute tasks using configured AI agents
- **Authentication**: JWT-based authentication system
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Real-time**: Redis for caching and real-time features

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Run the development server:**
```bash
uvicorn main:app --reload
```

4. **Visit API documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/logout` - User logout
- `GET /api/v1/auth/me` - Get current user

### Agents
- `GET /api/v1/agents/` - List all agents
- `POST /api/v1/agents/` - Create new agent
- `GET /api/v1/agents/{id}` - Get specific agent
- `PUT /api/v1/agents/{id}` - Update agent
- `DELETE /api/v1/agents/{id}` - Delete agent
- `POST /api/v1/agents/{id}/execute` - Execute agent task

### Interface Generation
- `POST /api/v1/interfaces/generate` - Generate interface from prompt
- `GET /api/v1/interfaces/{id}` - Get generated interface
- `PUT /api/v1/interfaces/{id}/refine` - Refine existing interface
- `POST /api/v1/interfaces/preview` - Quick preview generation

### Users
- `GET /api/v1/users/` - List users (admin)
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

## Project Structure

```
app/
├── api/v1/              # API version 1
│   ├── endpoints/       # API route handlers
│   └── api.py          # API router configuration
├── core/               # Core functionality
│   ├── config.py       # Application configuration
│   └── database.py     # Database connection
├── models/             # SQLAlchemy models
├── schemas/            # Pydantic schemas
│   └── agent.py        # Agent data models
└── services/           # Business logic
    ├── agent_service.py # Agent management
    └── interface_generator.py # UI generation
```

## Configuration

Key environment variables:

- `POSTGRES_*`: Database connection settings
- `REDIS_URL`: Redis connection string
- `OPENAI_API_KEY`: OpenAI API key for GPT models
- `ANTHROPIC_API_KEY`: Anthropic API key for Claude
- `GOOGLE_AI_API_KEY`: Google AI API key for Gemini
- `SECRET_KEY`: JWT signing secret
- `BACKEND_CORS_ORIGINS`: Allowed CORS origins

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
alembic upgrade head
```

### Code Formatting
```bash
black .
isort .
```

## Deployment

The backend is designed to be deployed on cloud platforms like AWS, Google Cloud, or Azure. Key considerations:

- Use environment variables for configuration
- Set up PostgreSQL database
- Configure Redis for caching
- Set proper CORS origins for production
- Use HTTPS in production
- Monitor with logging and metrics

## API Documentation

When running the server, visit:
- http://localhost:8000/docs for interactive Swagger documentation
- http://localhost:8000/redoc for ReDoc documentation

## License

MIT License - see LICENSE file for details.