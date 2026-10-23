import os


class Settings:
    APP_NAME = "Background Jobs API"
    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM = os.getenv("EMAIL_FROM", "")
    WEBHOOK_TIMEOUT = float(os.getenv("WEBHOOK_TIMEOUT", "10"))


settings = Settings()
