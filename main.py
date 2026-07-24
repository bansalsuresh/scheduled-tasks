import smtplib
import os

from check_stock_alerts import build_stock_alert_contents

# import os and use it to get the Github repository secrets
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")

contents = build_stock_alert_contents()
with smtplib.SMTP('smtp.gmail.com', 587) as connection:
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD)
    connection.sendmail(
        from_addr=f"Suresh Bansal <{MY_EMAIL}>",
        to_addrs=TO_EMAIL,
        msg=f"Subject:Stock Alerts\n\n{contents}"
    )
