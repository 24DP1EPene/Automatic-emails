from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender: str, receiver:str, password: str, subject: str, body: str) -> tuple[str, bool]:

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
            message = f'Failed to send email: {e}'
            status = False
        else:
            message = 'Successfully sent an email'
            status = True

        return (message, status)