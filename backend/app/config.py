from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Auto Dialer"
    DATABASE_URL: str
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    ALLOWED_ORIGINS: list = ["http://localhost:3000"]
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()