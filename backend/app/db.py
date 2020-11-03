import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI):
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.rates"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
