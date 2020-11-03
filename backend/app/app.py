from fastapi import FastAPI

from app.db import init_db

from app.routers import api_router

app = FastAPI()
init_db(app)

app.include_router(api_router, prefix='/api')
