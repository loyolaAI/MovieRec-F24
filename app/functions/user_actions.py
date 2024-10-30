from werkzeug.security import generate_password_hash
from app.db_models.user import User
from app.db_models.password_reset_token import PasswordResetToken as Pass
from app import db
from sendgrid import SendGridAPIClient, SendGridException

import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("SENDGRID_API_KEY"):
    raise ValueError("SENDGRID_API_KEY is not set.")

from typing import Callable
from cuid2 import cuid_wrapper  # type: ignore

cuid_generator: Callable[[], str] = cuid_wrapper()

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def create_user(email: str, username: str, password: str, letterboxd: str) -> User:
    return User(
        id=cuid_generator(),
        email=email,
        username=username,
        letterboxd_username=letterboxd,
        password=generate_password_hash(password),
        ratings=[],
        reset_token=None,
        profile_image_id=None,
        profile_image_url=None,
    )


def update_user(user: User, username: str, email: str, letterboxd: str, *imgData: dict) -> None:
    user.email = email
    user.username = username
    user.letterboxd_username = letterboxd

    if imgData:
        user.profile_image_url = imgData["url"]
        user.profile_image_id = imgData["id"]

    db.session.commit()


def update_password(user: User, new_password: str) -> None:
    user.password = generate_password_hash(new_password)
    db.session.commit()


def send_password_reset_email(user: User, token: Pass) -> None:
    message = Mail(
        from_email="no-reply@dacs-digital.design",
        to_emails=user.email,
        subject="LAIC MovieRec Password Reset",
        html_content=construct_reset_password_email(token),
    )
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"Email sent with status code {response.status_code}")
    except SendGridException as e:
        print(f"Error sending email: {e}")


def construct_reset_password_email(token):
    username = token.user.username
    reset_token = token.token
    return f"""
    <!doctype html>
    <html lang='en'>
      <head>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
        <title>Password Reset</title>
      </head>
      <body style='font-family: Helvetica, sans-serif; background-color: #f4f5f6; color: black; margin: 0; padding: 0;'>
        <table role='presentation' width='100%' bgcolor='#ffffff' style='width: 100%; background-color: #ffffff; padding: 0; margin: 0;'>
          <tr>
            <td>&nbsp;</td>
            <td style='max-width: 600px; width: 100%; margin: 32px; padding: 24px; background-color: #ffffff; border-radius: 16px;'>
              <div style='max-width: 600px; margin: 0 auto;'>
                <p style='font-size: 16px; margin: 0 0 16px; color: black;'>Dear {username},</p>
                <p style='font-size: 16px; margin: 0 0 16px; color: black;'>You requested a password reset for your account. You can reset your password by clicking the button below or by entering the 6-digit code manually.</p>
                <table role='presentation' width='100%' style='margin: 16px 0;'>
                  <tr>
                    <td align='center'>
                      <a href='http://localhost:5000/reset-password?reset-token={reset_token}' target='_blank' style='display: inline-block; padding: 12px 24px; font-size: 16px; line-height: 16px; color: #ffffff; background-color: #0867ec; text-decoration: none; border-radius: 4px;'>Reset Password</a>
                    </td>
                  </tr>
                </table>
                <p style='font-size: 16px; margin: 0 0 16px; color: black;'>If you prefer, you can also use the following 6-digit code to reset your password:</p>
                <p style='font-size: 16px; font-weight: bold; color: black; margin: 0 0 16px;'>{reset_token}</p>
                <p style='font-size: 16px; margin: 0 0 16px; color: black;'>This code is valid for the next 15 minutes.</p>
                <p style='font-size: 16px; margin: 0; color: black;'>Good luck! We hope this helps you get back into your account.</p>
              </div>
            </td>
            <td>&nbsp;</td>
          </tr>
        </table>
      </body>
    </html>
    """
