"""Notification microservice - entry point.

Run:  uvicorn app.main:app --reload --port 8084
  or: python -m app.main
"""
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import notification

PORT = int(os.getenv("PORT", "8084"))
EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka")
INSTANCE_HOST = os.getenv("EUREKA_INSTANCE_HOST", "localhost")
INSTANCE_IP = os.getenv("EUREKA_INSTANCE_IP", "127.0.0.1")
logger = logging.getLogger(__name__)


def report_eureka_error(error_type: str, error: Exception) -> None:
    logger.error("Eureka client error (%s): %s", error_type, error)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from py_eureka_client import eureka_client

    await eureka_client.init_async(
        eureka_server=EUREKA_SERVER,
        app_name="notification",
        instance_id=f"notification:{PORT}",
        instance_host=INSTANCE_HOST,
        instance_ip=INSTANCE_IP,
        instance_port=PORT,
        home_page_url=f"http://{INSTANCE_HOST}:{PORT}/swagger-ui",
        status_page_url=f"http://{INSTANCE_HOST}:{PORT}/api/notifications/hello",
        health_check_url=f"http://{INSTANCE_HOST}:{PORT}/api/notifications/hello",
        on_error=report_eureka_error,
    )
    logger.info("Notification registered with Eureka at %s", EUREKA_SERVER)
    try:
        yield
    finally:
        await eureka_client.stop_async()

app = FastAPI(
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; the notification logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    # Same URLs as the other microservices of the project
    docs_url="/swagger-ui",       # Swagger UI
    openapi_url="/v3/api-docs",   # OpenAPI JSON
    redoc_url="/redoc",           # alternative documentation
    lifespan=lifespan,
)

app.include_router(notification.router)

# TODO (students): if you add other routers, include them here.


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)