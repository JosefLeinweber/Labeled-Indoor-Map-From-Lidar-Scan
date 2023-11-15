import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


from src.config.settings.setup import settings
from src.utility.events.event_handlers import (
    execute_backend_server_event_handler,
    terminate_backend_server_event_handler,
)
from src.api.endpoints import router


def initialize_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI(**settings.set_backend_app_attributes)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    app.add_event_handler(
        "startup",
        execute_backend_server_event_handler(app=app),
    )

    app.add_event_handler(
        "shutdown",
        terminate_backend_server_event_handler(app=app),
    )

    app.router.include_router(router)

    return app


app: fastapi.FastAPI = initialize_application()

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
