from fastapi import FastAPI
from app.api.router import router

fastapi_app = FastAPI(title="LP Command Center", docs_url=None, redoc_url=None)
fastapi_app.include_router(router)
