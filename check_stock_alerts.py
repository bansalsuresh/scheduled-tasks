import operator
import os
import time

import pandas as pd
import requests

EXCEL_PATH = "stocks.xlsx"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")

CONDITION_OPERATORS = {
    ">": operator.gt,
    "<": operator.lt,
    "=": operator.eq,
    "!=": operator.ne,
    "<=": operator.le,
    ">=": operator.ge,
}

def is_yes(value) -> bool:
    return str(value).strip().lower() == "yes"


def get_yesterday_close(symbol: str) -> float | None:
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": STOCK_API_KEY,
    }
    response = requests.get(STOCK_ENDPOINT, params=params)
    time.sleep(1)
    data = response.json()

    time_series = data.get("Time Series (Daily)")
    if not time_series:
        print(f"Could not fetch NAV for {symbol}: {data}")
        return None

    latest_day = sorted(time_series.keys(), reverse=True)[0]
    return float(time_series[latest_day]["4. close"])


def is_alert_triggered(nav: float, condition: str, value: float) -> bool:
    compare = CONDITION_OPERATORS.get(str(condition).strip())
    if compare is None:
        raise ValueError(f"Unsupported condition: {condition!r}")
    return compare(nav, value)


def process_stocks(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    nav_by_symbol: dict[str, float | None] = {}

    yesterday_navs = []
    alerts_triggered = []

    for _, row in df.iterrows():
        symbol = row["Symbol"]
        nav = None

        if is_yes(row["Check"]):
            if symbol not in nav_by_symbol:
                nav_by_symbol[symbol] = get_yesterday_close(symbol)
            nav = nav_by_symbol[symbol]

        triggered = False
        if (
            nav is not None
            and is_yes(row["Alert"])
            and pd.notna(row["Condition"])
            and pd.notna(row["Value"])
        ):
            triggered = is_alert_triggered(nav, row["Condition"], row["Value"])

        yesterday_navs.append(nav)
        alerts_triggered.append(triggered)

    df["Yesterday NAV"] = yesterday_navs
    df["Alert Triggered"] = alerts_triggered
    return df


def build_summary_strings(df: pd.DataFrame) -> tuple[str, str]:
    checked = df[df["Yesterday NAV"].notna()]
    all_stocks_summary = "\n".join(
        f"{row['Name']} ({row['Symbol']}): {row['Yesterday NAV']:.2f}"
        for _, row in checked.iterrows()
    ) or "No stocks were checked."

    triggered = df[df["Alert Triggered"]]
    alerts_summary = "\n".join(
        f"{row['Name']} ({row['Symbol']}): NAV {row['Yesterday NAV']:.2f} "
        f"{row['Condition']} {row['Value']} -> ALERT TRIGGERED"
        for _, row in triggered.iterrows()
    ) or "No alerts triggered."

    return all_stocks_summary, alerts_summary


def main() -> None:
    df = pd.read_excel(EXCEL_PATH)
    df = process_stocks(df)
    all_stocks_summary, alerts_summary = build_summary_strings(df)

    # print(df.to_string())
    print("\n--- All Checked Stocks & NAV ---")
    print(all_stocks_summary)
    print("\n--- Triggered Alerts ---")
    print(alerts_summary)


if __name__ == "__main__":
    main()
