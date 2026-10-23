from fastapi import FastAPI, BackgroundTasks, Request
from slowapi.errors import RateLimitExceeded
from slowapi.extension import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from background_jobs_api.app.config import settings
from background_jobs_api.app.limiter import limiter
from background_jobs_api.app.schemas import EmailRequest, WebhookRequest
from background_jobs_api.app.tasks import send_email, dispatch_webhook

app = FastAPI(
    title=settings.APP_NAME,
    description="Background email and webhook processing API",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)
app.add_middleware(SlowAPIMiddleware)


@app.get("/")
def home():
    return {
        "message": "Background Jobs API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/send-email", status_code=202)
@limiter.limit("5/minute")
def send_email_endpoint(
    request: Request,
    data: EmailRequest,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        send_email,
        data.to_email,
        data.subject,
        data.message,
    )

    return {
        "message": "Email job accepted",
        "status": "queued",
        "recipient": data.to_email,
    }


@app.post("/send-webhook", status_code=202)
@limiter.limit("10/minute")
def send_webhook_endpoint(
    request: Request,
    data: WebhookRequest,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        dispatch_webhook,
        str(data.webhook_url),
        data.payload,
    )

    return {
        "message": "Webhook job accepted",
        "status": "queued",
    }
