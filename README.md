# Sweep Food

Sweep Food is a household food-management application for tracking batch inventory and expiry dates. It is designed to recommend recipes that prioritize ingredients nearing their expiry date.

## Technology

![Flutter](https://img.shields.io/badge/Flutter-Dart-02569B?logo=flutter&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.4-DC382D?logo=redis&logoColor=white)

| Component | Main technologies |
| --- | --- |
| Frontend | Flutter/Dart, `flutter_bloc`, `get_it`, `go_router`, `dio` |
| Backend | Python, FastAPI, PostgreSQL (Neon), Redis |
| Frontend support | `flutter_secure_storage`, `shared_preferences`, image picker/cropper, and charts |

## Project structure

### BE Folder Structure

```text
src/backend/
├── src/
│   ├── core/                      # Configuration and shared exceptions
│   ├── middleware/                # HTTP middleware
│   ├── model/                     # Database models
│   ├── module/                    # Feature modules (for example, health)
│   └── service/                   # Shared application services
├── docs/                          # PRD, database documentation, and ADRs
├── main.py                        # Application entry point
├── Dockerfile
└── README.md
```

### FE Folder Structure

```text
src/frontend/
├── lib/
│   ├── app/
│   │   └── routes/                # GoRouter configuration
│   ├── core/                      # API client, interceptors, constants, errors, and utilities
│   ├── features/                  # Feature modules
│   │   └── <feature>/
│   │       ├── data/              # Data sources, models, and repository implementations
│   │       ├── domain/            # Entities, repository contracts, and use cases
│   │       └── presentation/      # Controllers, views, and widgets
│   ├── shared/widgets/            # Reusable widgets
│   ├── injection_container.dart   # GetIt registrations
│   └── main.dart                  # Application bootstrap
├── assets/                        # Icons and images
├── test/
├── pubspec.yaml
└── README.md
```

Each frontend feature is divided into `data`, `domain`, and `presentation` layers so the UI does not access the API or storage mechanisms directly.

## Documentation

- [Product requirements](docs/requirement.md)
- [Frontend guide](src/frontend/README.md)
- [Backend guide](src/backend/README.md)

Build with Cloudian 💙 Cloud
