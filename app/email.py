from flask import current_app
from sendgrid.helpers.mail import Mail
import os
from pathlib import Path
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from app.constants import ADMINS


def init_sendgrid():
    sendgrid_env_path = Path(__file__).resolve().parent.parent / "sendgrid.env"
    load_dotenv(dotenv_path=sendgrid_env_path)
    sendgrid = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    return sendgrid


sendgrid = init_sendgrid()


def send_email(to, subject, text, html=None, sender=None):
    """Sends an email using SendGrid

    Args:
        to (str or list): Recipient email(s)
        subject (str): Subject of the email
        text (str): Plain-text content
        html (str, optional): HTML content (if any). Defaults to None.
    """

    # If `to` is a list, join into comma-separated string
    if isinstance(to, list):
        to = ','.join(to)

    if sender is None:
        sender = ADMINS[0]

    msg = Mail(
        from_email=sender,
        to_emails=to,
        subject=subject,
        html_content=html,
        plain_text_content=text,
    )

    try:
        response = sendgrid.send(msg)
        return response
    except Exception as e:
        current_app.logger.error(f'Failed to send email: {e}')
        raise
