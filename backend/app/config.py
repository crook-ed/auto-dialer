from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Auto Dialer API"
    DATABASE_URL: str
    SECRET_KEY: str
    ALLOWED_ORIGINS: list = ["http://localhost:3000"]
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str

    class Config:
        env_file = ".env"

settings = Settings()