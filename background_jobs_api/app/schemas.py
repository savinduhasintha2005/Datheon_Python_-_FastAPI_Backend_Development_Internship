from pydantic import BaseModel, EmailStr, HttpUrl, Field


class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1, max_length=5000)


class WebhookRequest(BaseModel):
    webhook_url: HttpUrl
    payload: dict = Field(
        description="JSON data to send to the webhook"
    )
