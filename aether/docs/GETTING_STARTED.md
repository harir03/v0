# Getting Started with Aether Agents

Welcome to Aether Agents - the next-generation platform for creating, deploying, and managing AI agents!

## Quick Start

### Option 1: Docker Compose (Recommended)

The easiest way to get started is using Docker Compose, which will set up the entire stack including the database and cache.

1. **Clone and navigate to the project:**
```bash
cd aether
```

2. **Start all services:**
```bash
docker-compose up -d
```

3. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Option 2: Manual Setup

If you prefer to run components separately:

#### Prerequisites
- Node.js 18+ 
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

#### Backend Setup
```bash
cd aether/backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database and API keys

# Run database migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

#### Frontend Setup
```bash
cd aether/frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

## Features Overview

### 🧠 Instant Interface Builder
- Describe your agent's UI in plain English
- Real-time interface generation
- Interactive refinement and iteration

### 💻 Agentic Coding Capabilities
- Agents that can read, write, and debug code
- Repository interaction via GitHub integration
- Project scaffolding and automation

### 👥 Multi-Agent Collaboration
- Create agent societies with task delegation
- Workflow orchestration
- Cross-agent communication

### 🔒 Enterprise Security
- SOC 2 compliance options
- On-premise deployment
- Role-based access control

## Subscription Tiers

### Free (Hobbyist)
- 1 User Seat
- Up to 2 Active Agents
- 500 Tasks/Month
- Basic Integrations

### $49/month (Startup)
- Up to 3 User Seats
- Up to 10 Active Agents
- 5,000 Tasks/Month
- Agentic Coding Capabilities
- Premium Integrations

### $199/month (Scale-Up)
- Up to 10 User Seats
- Unlimited Agents
- 50,000 Tasks/Month
- Multi-Agent Collaboration
- Voice Capabilities

### Enterprise (Custom Pricing)
- Unlimited Users & Tasks
- SOC 2 & HIPAA Compliance
- On-Premise Deployment
- Custom AI Model Fine-tuning

## Example Use Cases

### Customer Support Agent
```
"Create an agent for customer support. It needs a dashboard to view incoming tickets from Gmail. When I click a ticket, it should show the email content on the right and have a text box below where the agent can draft a response using our knowledge base."
```

### Code Review Agent
```
"Build an agent that reviews pull requests, identifies potential bugs, and leaves constructive comments. It should integrate with GitHub and understand our coding standards."
```

### Lead Management Agent
```
"Design a lead management system that captures leads from our website, scores them based on our criteria, and automatically schedules follow-up tasks for our sales team."
```

## API Integration

### Creating an Agent
```javascript
const agent = await fetch('/api/v1/agents/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'My Customer Support Agent',
    type: 'customer_support',
    description: 'Handles customer inquiries and support tickets',
    configuration: {
      knowledge_base_id: 'kb_123',
      response_tone: 'friendly',
      escalation_threshold: 0.8
    }
  })
});
```

### Generating an Interface
```javascript
const interface = await fetch('/api/v1/interfaces/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'Create a dashboard for monitoring agent performance with charts and metrics'
  })
});
```

## Configuration

### Environment Variables

#### Backend (.env)
```bash
# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=aether_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=aether_agents

# AI Providers
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_AI_API_KEY=your_google_key

# Security
SECRET_KEY=your_secret_key
```

#### Frontend
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Development

### Running Tests
```bash
# Backend tests
cd aether/backend
pytest

# Frontend tests (if implemented)
cd aether/frontend
npm test
```

### Database Migrations
```bash
cd aether/backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Support

- 📚 [Full Documentation](./docs/)
- 🐛 [Report Issues](https://github.com/your-repo/issues)
- 💬 [Community Discord](https://discord.gg/aether-agents)
- 📧 [Email Support](mailto:support@aether-agents.com)

## License

MIT License - see LICENSE file for details.

---

**Ready to build your AI workforce? Start with our free tier and scale as you grow!**