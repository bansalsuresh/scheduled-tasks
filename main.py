from mailer import Email
from config import Config

config = Config.read_config()
to_email = config["TO_EMAIL"]
subject = config["EMAIL_SUBJECT"]

mailer = Email()
mailer.send_mail(to_email, subject, "Best Wishes")

