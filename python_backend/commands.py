from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from python_backend.utils import log_action

def send_email(sender: str, receiver:str, password: str, subject: str, body: str) -> None:
    """
    funkcija <>
    pieņem <> tipa vērtību <>
    un atgriež <> tipa vērtību <>
    """
    # Create the email
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Connect to SMTP server
    try:
        with SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
    except Exception as e:
        log_action(f'Failed to send the email from {sender} to {receiver} | Error: {e}')
    else:
        log_action(f'Successfully sent the email from {sender} to {receiver}')