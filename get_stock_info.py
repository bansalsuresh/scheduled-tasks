from io import StringIO
import os
from pathlib import Path

import pandas as pd
import requests

from config import Config


class GetStockInfo:
    def __init__(
        self,
        stock_name: str,
        offline: bool = True,
    ) -> None:
        config = Config.read_config()
        self.stock_name = stock_name
        self.stock_endpoint = config["STOCK_ENDPOINT"]
        self.stock_api_key = os.environ.get("STOCK_API_KEY")
        self.offline = offline

    def _build_cache_file(self, configured_cache_dir: str) -> Path:
        cache_directory = Path(configured_cache_dir)
        cache_directory.mkdir(exist_ok=True)
        cache_name = f"time_series_daily__{self.stock_name}.csv"

        return cache_directory / cache_name

    def build_stock_params(self) -> dict[str, str | None]:
        return {
            "function": "TIME_SERIES_DAILY",
            "symbol": self.stock_name,
            "apikey": self.stock_api_key,
            "datatype": "csv",
        }

    def get_csv_text(self) -> str:

        response = requests.get(self.stock_endpoint, params=self.build_stock_params())
        response.raise_for_status()
        csv_text = response.text
        return csv_text

    def get_dataframe(self) -> pd.DataFrame:
        csv_buffer = StringIO(self.get_csv_text())
        return pd.read_csv(csv_buffer)
