# app/core/config.py

from pydantic import BaseSettings, AnyHttpUrl, PostgresDsn, validator
from typing import List, Optional, Union
import os

class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v

    # --- DB settings ---
    DB_TYPE: str

    # For SQLite
    SQLITE_PATH: str 

    # For PostgreSQL
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_PORT: Optional[int] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    DATABASE_URI: Optional[str] = None

    @validator("DATABASE_URI", pre=True, always=True)
    def assemble_db_uri(cls, v: Optional[str], values: dict) -> str:
        if values["DB_TYPE"] == "sqlite":
            path = values["SQLITE_PATH"]
            abs_path = os.path.abspath(path)
            return f"sqlite:///{abs_path}"
        elif values["DB_TYPE"] == "postgres":
            return PostgresDsn.build(
                scheme="postgresql",
                user=values["POSTGRES_USER"],
                password=values["POSTGRES_PASSWORD"],
                host=values["POSTGRES_SERVER"],
                port=str(values["POSTGRES_PORT"]),
                path=f"/{values['POSTGRES_DB']}",
            )
        raise ValueError("Invalid DB_TYPE. Use 'sqlite' or 'postgres'.")

    # --- Security ---
    SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS:int=30

    AWS_ACCESS_KEY_ID:str
    AWS_SECRET_ACCESS_KEY:str
    AWS_S3_REGION:str
    AWS_S3_BUCKET:str
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
