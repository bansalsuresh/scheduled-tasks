import time
import traceback
from pathlib import Path

from analyze_stock_info import AnalyzeStockInfo
from config import Config
from get_stock_info import GetStockInfo

from mailer import Email

config = Config.read_config()
to_email = config["TO_EMAIL"]
subject = config["EMAIL_SUBJECT"]


config = Config.read_config()
STOCKS_FILE = Path(config["STOCKS_FILE"])
MAX_STOCKS = 25
DELAY_SECONDS = 1

stock_names = [
    line.strip()
    for line in STOCKS_FILE.read_text(encoding="utf-8").splitlines()
    if line.strip()
][:MAX_STOCKS]

message_parts = []

for index, stock_name in enumerate(stock_names, start=1):
    stock_info = GetStockInfo(stock_name=stock_name, offline=False)

    try:
        df = stock_info.get_dataframe()
        analysis = AnalyzeStockInfo(df)
        metrics = analysis.calculate_key_metrics()
        recommendation = analysis.recommend_action(metrics)
        summary = analysis.format_analysis_summary(recommendation, metrics)

        message_parts.append(
            f"\n{'=' * 80}\n"
            f"Stock {index}: {stock_name}\n"
            f"{summary}"
        )
    except Exception as error:
        error_type = type(error).__name__
        error_args = getattr(error, "args", ())
        error_traceback = traceback.format_exc()
        message_parts.append(
            f"\n{'=' * 80}\n"
            f"Stock {index}: {stock_name}\n"
            f"Analysis failed\n"
            f"Error type: {error_type}\n"
            f"Error repr: {error!r}\n"
            f"Error args: {error_args}\n"
            f"Traceback:\n{error_traceback}"
        )

    if index < len(stock_names):
        time.sleep(DELAY_SECONDS)

msg_body = "".join(message_parts).lstrip()

mailer = Email()
mailer.send_mail(to_email, subject, msg_body)
