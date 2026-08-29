# Sweep Food

Sweep Food helps a single user manage household food inventory, track expiry dates by batch, and receive meal recommendations that prioritize ingredients expiring first.

## Technology

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.4-DC382D?logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

## Services

```text
src/
├── backend/                 # FastAPI backend service
│   ├── src/
│   │   ├── core/            # Environment settings and exceptions
│   │   ├── module/          # Feature modules
│   │   ├── model/           # Database models
│   │   └── service/         # Shared services
│   ├── docs/                # PRD, database schema, and decisions
│   ├── wiremock/            # Mock external HTTP APIs for local development
│   ├── main.py              # Backend entry point
│   ├── Dockerfile
│   └── docker-compose.yaml
└── frontend/                # Frontend service workspace
    └── README.md
```

Build with Cloudian 💙 Cloud
