# FastAPI ML Deployment Architecture

## Why I Built This

I know serving an ML model with Flask takes about 30 lines of code. I know a Jupyter notebook works perfectly fine for most use cases. 

But I wanted to understand what all the discussion is about with "enterprise architecture" and "production-ready" systems. So I built this intentionally over-engineered version to learn the patterns and tools that larger companies use - even though the complexity is probably unnecessary for most real ML deployments.

This is my exploration of what happens when you choose the more complex approach on purpose.

## Technology Stack

- **FastAPI 0.115.6** - Modern Python web framework with automatic documentation
- **scikit-learn 1.6.0** - Simple linear regression for ML functionality
- **PostgreSQL 15** - Production-grade database with proper integration
- **Docker** - Containerization for consistent environments
- **SQLAlchemy 2.0** - Industry-standard Python ORM
- **Alembic** - Database migration management
- **Pydantic Settings** - Type-safe configuration management

## Project Structure

Follows hexagonal architecture principles with clear separation of concerns:

```
app/
├── api/v1/endpoints/     # HTTP request handlers and routing
├── core/                 # Application configuration and settings
├── db/                   # Database connection and session management
├── models/               # SQLAlchemy entity definitions
├── schemas/              # Pydantic data transfer objects
├── services/             # Business logic and domain operations
├── ml/                   # Machine learning model lifecycle management
└── main.py              # Application factory and ASGI entry point
```

## Getting This Thing Running

### 1. Environment Setup
```bash
# Copy environment template
copy .env.example .env

# Edit .env with your actual values
```

### 2. Local Development (with venv)
```bash
# Create virtual environment
py -3.13.9 -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run application
uvicorn app.main:app --reload
```

### 3. Docker Development
```bash
# Build and run with docker-compose
docker-compose up --build

# Access application at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

## API Functionality

The application provides two main feature sets:

**Resource Management**:
- `POST /api/v1/items` - Create new items
- `GET /api/v1/items` - Retrieve item collection
- `GET /api/v1/items/{id}` - Get specific item
- `PUT /api/v1/items/{id}` - Update existing item
- `DELETE /api/v1/items/{id}` - Remove item

**Machine Learning Operations**:
- `GET /api/v1/ml/sample-data` - Generate synthetic training data
- `POST /api/v1/ml/train` - Train linear regression model
- `POST /api/v1/ml/predict` - Execute model predictions
- `GET /api/v1/ml/model-info` - Retrieve model status and metrics

## Testing It Out

FastAPI provides interactive documentation at `http://localhost:8000/docs` for easy testing.

Alternatively, using curl:

```bash
# Get some sample data first
curl http://localhost:8000/api/v1/ml/sample-data

# Train the model with that data
curl -X POST http://localhost:8000/api/v1/ml/train \
  -H "Content-Type: application/json" \
  -d '{"X": [[1,2,3], [4,5,6]], "y": [10, 20]}'

# Make a prediction
curl -X POST http://localhost:8000/api/v1/ml/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0]}'

# Test the basic CRUD stuff
curl -X POST http://localhost:8000/api/v1/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "Just testing"}'
```

## Key Insights 🤔

**FastAPI Benefits**: Automatic API documentation eliminates manual documentation work. Built-in type validation catches errors early. Async support handles concurrent requests efficiently.

**Database Architecture**: SQLAlchemy provides essential features for production applications - migrations, connection pooling, and team collaboration. The ORM abstraction becomes valuable as complexity grows.

**Containerization Value**: Docker solves environment consistency issues. Multi-service orchestration with Docker Compose simplifies development workflows when managing databases and APIs together.

**Architectural Patterns**: Separating concerns into distinct layers (schemas, services, models) enables independent modification of different system components. The structure supports long-term maintainability.

**Complexity Justification**: Enterprise patterns exist because simple solutions face limitations with multiple developers, deployment requirements, and extended maintenance cycles.

## What I Wanted to Figure Out

I had questions about why everyone talks about FastAPI, Docker, and complex architectures when Flask works fine:

- Is FastAPI actually better or just trendy?
- Why do people separate everything into services, schemas, and models?
- What's the real benefit of Docker for simple applications?
- When does this complexity actually pay off?
- Are most production systems really this complicated?

Turns out, a lot of this complexity exists for problems I don't have yet - multiple developers, high availability requirements, regulatory compliance, or managing dozens of models. But learning these patterns helped me understand when and why to add complexity instead of just cargo-culting "best practices."

Most ML deployments are probably simpler than this. But now I know what the complex version looks like and when it might be worth the overhead.

---

*This is intentionally over-engineered for learning purposes. If you just need to serve a model, Flask + pickle is probably fine.*