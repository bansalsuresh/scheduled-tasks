import random
import smtplib
import os

# import os and use it to get the Github repository secrets
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")

def read_quotes():
    with open("quotes.txt", "r") as quotes_file:
        quotes = quotes_file.readlines()
        quote = random.choice(quotes)
        return quote

contents = read_quotes()
with smtplib.SMTP('smtp.gmail.com', 587) as connection:
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD)
    connection.sendmail(
        from_addr=f"Suresh Bansal <{MY_EMAIL}>",
        to_addrs=TO_EMAIL,
        msg=f"Subject:Happy Birthday!\n\n{contents}"
    )
