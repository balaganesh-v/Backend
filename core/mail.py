# core/mail.py
import smtplib
from email.message import EmailMessage
from config import settings
import io
import qrcode
import pyotp


def send_email_smtp(
    to_email: str, subject: str, html_content: str, qr_code_bytes: bytes = None
):
    """
    Send an email using SMTP with optional QR code attachment (inline for HTML).
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_EMAIL
    msg["To"] = to_email
    msg.set_content("This email requires an HTML-capable email client.")
    msg.add_alternative(html_content, subtype="html")

    # Attach QR code if provided
    if qr_code_bytes:
        msg.get_payload()[1].add_related(
            qr_code_bytes, "image", "png", cid="totp_qr_code"
        )

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
            server.send_message(msg)
            print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")


def send_welcome_email(to_email: str, user_name: str, password: str, user_role: str):
    """
    Send a standard welcome email for students or teachers.
    """
    subject = f"Welcome to the School Management System, {user_role}!"
    html_content = f"""
    <h1>Welcome, {user_name}!</h1>
    <p>Your account has been created with the role of <b>{user_role}</b>.</p>
    <p>You can now login using:</p>
    <p><b>Email:</b> {to_email}</p>
    <p><b>Password:</b> {password}</p>
    <p>Thank you for joining!</p>
    """
    send_email_smtp(to_email, subject, html_content)


def send_principal_welcome_email(
    to_email: str, user_name: str, password: str, user_role: str, totp_secret: str
):
    """
    Send a welcome email to a principal with TOTP QR code.
    """
    subject = f"Welcome to the School Management System, {user_role}!"

    # Generate QR code from TOTP secret
    totp_uri = pyotp.TOTP(totp_secret).provisioning_uri(
        name=to_email, issuer_name="School Management System"
    )
    qr = qrcode.make(totp_uri)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    qr_code_bytes = buf.getvalue()

    html_content = f"""
    <h1>Welcome, {user_name}!</h1>
    <p>Your account has been created with the role of <b>{user_role}</b>.</p>
    <p>You can now login using:</p>
    <p><b>Email:</b> {to_email}</p>
    <p><b>Password:</b> {password}</p>
    <p>Scan this QR code in your Authenticator app to enable 2FA:</p>
    <img src="cid:totp_qr_code">
    <p>Thank you for joining!</p>
    """

    send_email_smtp(to_email, subject, html_content, qr_code_bytes)


def send_reset_password_email(
    to_email: str, reset_token: str, otp_code: str | None = None
):
    """
    Send a password reset email. Supports either:
        - a reset link (token), or
        - a one-time OTP code
    """
    subject = "Password Reset Instructions"

    # Option 1: Reset link
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

    # If OTP mode is used instead of link
    otp_section = ""
    if otp_code:
        otp_section = f"""
            <h3>Your OTP Code</h3>
            <p style="font-size: 20px; font-weight: bold;">{otp_code}</p>
            <p>This code expires in 5 minutes.</p>
        """

    html_content = f"""
    <h2>Password Reset Request</h2>
    <p>You requested to reset your password.</p>

    <h3>Reset Link</h3>
    <p>Click the link below to reset your password:</p>
    <p>
        <a href="{reset_link}"
            style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px;">
            Reset Password
        </a>
    </p>

    {otp_section}

    <p>If you did not request this change, you can safely ignore this email.</p>
    """

    send_email_smtp(to_email, subject, html_content)
