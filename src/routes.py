from fastapi import APIRouter
from src.auth.controllers.auth_controller import router as auth_router

def get_apps_router(**kwargs):
    router = APIRouter()
    
    for router_name, router_instance in kwargs.items():
        router.include_router(router_instance)
    
    return router

app_routes = get_apps_router(
    auth_router = auth_router,
)