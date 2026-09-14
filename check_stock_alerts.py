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
    """Return True when a cell value is exactly yes, ignoring case and spaces."""
    return str(value).strip().lower() == "yes"

def get_yesterday_close(symbol: str) -> tuple[float, float, float] | None:
    """Fetch the latest daily close, minimum close, and maximum close for a stock symbol."""
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

    close_prices = [float(day_data["4. close"]) for day_data in time_series.values()]
    latest_day = sorted(time_series.keys(), reverse=True)[0]
    yesterday_close = float(time_series[latest_day]["4. close"])
    return yesterday_close, min(close_prices), max(close_prices)


def is_alert_triggered(nav: float, condition: str, value: float) -> bool:
    """Compare NAV against an alert value using the requested condition."""
    compare = CONDITION_OPERATORS.get(str(condition).strip())
    if compare is None:
        raise ValueError(f"Unsupported condition: {condition!r}")
    return compare(nav, value)

def process_stocks(df: pd.DataFrame) -> pd.DataFrame:
    """Add latest NAV and alert status columns to the stock dataframe."""
    df = df.copy()
    nav_by_symbol: dict[str, tuple[float, float, float] | None] = {}

    yesterday_navs = []
    min_navs = []
    max_navs = []
    alerts_triggered = []

    for _, row in df.iterrows():
        symbol = row["Symbol"]
        nav = None
        min_nav = None
        max_nav = None

        if is_yes(row["Check"]):
            if symbol not in nav_by_symbol:
                # Call to API
                nav_by_symbol[symbol] = get_yesterday_close(symbol)
            nav_data = nav_by_symbol[symbol]
            if nav_data is not None:
                nav, min_nav, max_nav = nav_data

        triggered = False
        if (
            nav is not None
            and is_yes(row["Alert"])
            and pd.notna(row["Condition"])
            and pd.notna(row["Value"])
        ):
            triggered = is_alert_triggered(nav, row["Condition"], row["Value"])

        yesterday_navs.append(nav)
        min_navs.append(min_nav)
        max_navs.append(max_nav)
        alerts_triggered.append(triggered)

    # Add these columns to the dataframe
    df["Yesterday NAV"] = yesterday_navs
    df["Min NAV"] = min_navs
    df["Max NAV"] = max_navs
    df["Alert Triggered"] = alerts_triggered
    return df


def get_range_placement(nav: float, min_nav: float, max_nav: float) -> float:
    """Return NAV's percentage placement between minimum and maximum values."""
    if min_nav == max_nav:
        return 100.0
    return ((nav - min_nav) / (max_nav - min_nav)) * 100


def format_nav_range(row: pd.Series) -> str:
    """Format NAV with min, max, and percentage placement details."""
    placement = get_range_placement(row["Yesterday NAV"], row["Min NAV"], row["Max NAV"])
    return (
        f"NAV {row['Yesterday NAV']:.2f} "
        f"(Min: {row['Min NAV']:.2f}, Max: {row['Max NAV']:.2f}, Placement: {placement:.2f}%)"
    )


def build_summary_strings(df: pd.DataFrame) -> tuple[str, str]:
    """Build summaries for checked stocks and triggered alerts."""
    # Get all stocks for which we got NAV and then build a string from them
    checked = df[df["Yesterday NAV"].notna()]
    all_stocks_summary = "\n".join(
        f"{row['Name']} ({row['Symbol']}, {row['Cost']:.2f}): "
        f"{format_nav_range(row)}"
        for _, row in checked.iterrows()
    ) or "No stocks were checked."

    # Get all stocks for which alert was triggered and then build a string from them
    triggered = df[df["Alert Triggered"]]
    alerts_summary = "\n".join(
        f"{row['Name']} ({row['Symbol']}): {format_nav_range(row)} "
        f"{row['Condition']} {row['Value']} -> ALERT TRIGGERED"
        for _, row in triggered.iterrows()
    ) or "No alerts triggered."

    return all_stocks_summary, alerts_summary

def build_stock_alert_contents() -> str:
    """Read stock data and return the final alert report text."""
    df = pd.read_excel(EXCEL_PATH)
    df = process_stocks(df)
    all_stocks_summary, alerts_summary = build_summary_strings(df)

    return (
        "--- All Checked Stocks & NAV ---\n"
        f"{all_stocks_summary}\n\n"
        "--- Triggered Alerts ---\n"
        f"{alerts_summary}"
    )


def main() -> None:
    """Print the stock alert report."""
    print(build_stock_alert_contents())


if __name__ == "__main__":
    main()
