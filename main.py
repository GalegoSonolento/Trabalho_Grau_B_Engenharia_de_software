from fastapi import FastAPI
from src.adapters.api.user_controller import router as user_router
from src.infrastructure.logging import setup_logging
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Task Management API",
    description="A RESTful API for managing collaborative tasks, built with FastAPI and MongoDB.",
    version="1.0.0",
    openapi_tags=[
        {"name": "users", "description": "Operations related to user management"},
    ]
)

setup_logging()

# Register routers
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)