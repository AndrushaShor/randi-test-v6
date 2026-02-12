from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://agent:agent_dev@postgres:5432/appdb"
    
    # API
    API_VERSION: str = "v1"
    API_TITLE: str = "Construction Project Management API"
    API_DESCRIPTION: str = "REST API for managing construction projects and their locations"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
