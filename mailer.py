import os
import smtplib

from config import Config


class Email:
    def __init__(self):
        config = Config.read_config()
        self.from_email = config["FROM_EMAIL"]
        self.email_password = os.environ.get("EMAIL_PASSWORD")
        self.smtp_address = config["SMTP_ADDRESS"]

    def send_mail(self, to_address, subject, email_body):
        with smtplib.SMTP(self.smtp_address) as connection:
            connection.starttls()
            connection.login(self.from_email, self.email_password)
            connection.sendmail(
                from_addr=self.from_email,
                to_addrs=to_address,
                msg=f"Subject:{subject}\n\n{email_body}",
            )
