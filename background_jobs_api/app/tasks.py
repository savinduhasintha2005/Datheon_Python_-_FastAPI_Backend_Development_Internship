import logging
import smtplib
from email.message import EmailMessage
import httpx
from background_jobs_api.app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_email(to_email: str, subject: str, message: str) -> None:
    """Send an email in a background task."""
    if not all([
        settings.SMTP_HOST,
        settings.SMTP_USERNAME,
        settings.SMTP_PASSWORD,
        settings.EMAIL_FROM,
    ]):
        logger.info(
            "DEV EMAIL | To: %s | Subject: %s | Message: %s",
            to_email,
            subject,
            message,
        )
        return

    email = EmailMessage()
    email["From"] = settings.EMAIL_FROM
    email["To"] = to_email
    email["Subject"] = subject
    email.set_content(message)

    try:
        with smtplib.SMTP(
            settings.SMTP_HOST, settings.SMTP_PORT, timeout=10
        ) as server:
            server.starttls()
            server.login(
                settings.SMTP_USERNAME,
                settings.SMTP_PASSWORD,
            )
            server.send_message(email)

        logger.info("Email sent to %s", to_email)

    except Exception:
        logger.exception("Failed to send email to %s", to_email)


def dispatch_webhook(webhook_url: str, payload: dict) -> None:
    """Dispatch a JSON payload to a webhook."""
    try:
        with httpx.Client(
            timeout=settings.WEBHOOK_TIMEOUT,
            follow_redirects=False,
        ) as client:
            response = client.post(webhook_url, json=payload)
            response.raise_for_status()

        logger.info(
            "Webhook dispatched successfully: %s (status %s)",
            webhook_url,
            response.status_code,
        )

    except Exception:
        logger.exception("Webhook dispatch failed: %s", webhook_url)
