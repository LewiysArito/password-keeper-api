from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import app_routes
from src.config.project_config import settings_project

#Костыль, который к сожалению нужен!!!
import migrations.base

def get_application() -> FastAPI:
    application = FastAPI(
        title=settings_project.NAME,
        debug=settings_project.DEBUG,
        version=settings_project.VERSION,
    )
    application.include_router(app_routes)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings_project.CORS_ALLOWED_ORIGINS.split(" "),
        allow_credentials=True,
        allow_methods=["*"],
    )
    return application


app = get_application()
