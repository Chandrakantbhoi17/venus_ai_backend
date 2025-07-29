from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.endpoints.query import router as query_router
from app.api.v1.endpoints.auth import router as auth_router
def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)
    

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
app.include_router(query_router)
app.include_router(auth_router)