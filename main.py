import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import app_routes
from src.config.project_config import project_settings

def get_application() -> FastAPI:
    application = FastAPI(
        title=project_settings.NAME,
        debug=project_settings.DEBUG,
        version=project_settings.VERSION
    )
    application.include_router(app_routes)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=project_settings.CORS_ALLOWED_ORIGINS.split(" "),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application

app = get_application()

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", reload=True)