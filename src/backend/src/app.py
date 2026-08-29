from dotenv import load_dotenv
from fastapi import FastAPI

from src.core.exceptions import register_exception_handlers
from src.core.setting import get_env_var
from src.module.health.health_router import health_router

APP_NAME = "Sweep Food API"
APP_VERSION = "0.1.0"
API_PREFIX = "/api"

def create_app() -> FastAPI:
    load_dotenv()
    application = FastAPI(
        title=APP_NAME,
        version=APP_VERSION,
        description="Sweep Food backend API.",
    )
    application.state.environment = get_env_var("ENV", "dev")
    register_exception_handlers(application)
    application.include_router(health_router, prefix=API_PREFIX)
    return application


app = create_app()
