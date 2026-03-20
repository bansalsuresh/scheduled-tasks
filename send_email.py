import os
import smtplib

class EmailFunctions:
    def send_email(self, email_adr, body):
        MY_PASSWORD = os.environ.get("MY_PASSWORD")
        MY_EMAIL = os.environ.get("MY_EMAIL")
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=email_adr,
                msg=f"Subject: Daily Weather Update\n\n{body}")