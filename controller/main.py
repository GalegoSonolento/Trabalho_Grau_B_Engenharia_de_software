from fastapi import FastAPI
from logs.logging_config import setup_logging
from view.users import router as users_router
from view.tasks import router as tasks_router
from controller.auth_utils import (
    create_access_token,
    get_current_user,
    invalidated_tokens,
    oauth2_scheme
)

setup_logging()

app = FastAPI()

app.include_router(users_router)
app.include_router(tasks_router)