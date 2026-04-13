import pandas as pd


class AnalyzeStockInfo:
    DEFAULT_RULES = {
        "sma_window": 20, # SMA Window of Last 20 Trading Sessions
        "rsi_window": 14, # SMA Window of Last 14 Trading Sessions
        "volatility_window": 20, # of Trading Sessions
        "volume_window": 20,  # Number of Trading Sessions
        "rsi_buy_max": 45.0,  # Buy signal below RSI of 45
        "rsi_sell_min": 70.0, # Sell signal above RSI of 70
        "volatility_buy_max": 0.03,  # Buy if volatility < 3%
        "volatility_sell_min": 0.05, # Sell if volatility > 5%
        "volume_ratio_buy_min": 1.0, # Buy if volume ratio is > 1
        "volume_ratio_sell_min": 1.5,# Sell if volume ratio is > 1.5
    }

    def __init__(self, dataframe: pd.DataFrame, rules: dict | None = None) -> None:
        self.dataframe = dataframe.copy()
        self.rules = {**self.DEFAULT_RULES, **(rules or {})}

    """
    {
        'close': 1350.15, 
        'sma': 1372.18, 
        'trend': 'downtrend', 
        'rsi': 40.41, 
        'momentum': 'oversold', 
        'volatility': 0.0183, 
        'volume': 501416, 
        'average_volume': 1353435.35, 
        'volume_ratio': 0.37}
    {'action': 'HOLD', 'reason': 'signals are mixed'}
    timestamp,open,high,low,close,volume
    """

    def calculate_key_metrics(self) -> dict[str, float | int | str]:
        df = self.dataframe.copy()

        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values("timestamp").reset_index(drop=True)

        numeric_columns = ["open", "high", "low", "close", "volume"]
        for column in numeric_columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

        max_window = max(
            self.rules["sma_window"],
            self.rules["rsi_window"],
            self.rules["volatility_window"],
            self.rules["volume_window"],
        )
        if len(df) < max_window:
            raise ValueError(f"At least {max_window} rows are required to calculate metrics.")

        df["sma"] = df["close"].rolling(self.rules["sma_window"]).mean()

        delta = df["close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        average_gain = gain.rolling(self.rules["rsi_window"]).mean()
        average_loss = loss.rolling(self.rules["rsi_window"]).mean()
        relative_strength = average_gain / average_loss.replace(0, pd.NA)
        df["rsi"] = 100 - (100 / (1 + relative_strength))
        df["rsi"] = df["rsi"].fillna(100)

        df["daily_return"] = df["close"].pct_change()
        df["volatility"] = df["daily_return"].rolling(self.rules["volatility_window"]).std()
        df["average_volume"] = df["volume"].rolling(self.rules["volume_window"]).mean()
        df["volume_ratio"] = df["volume"] / df["average_volume"]

        latest = df.iloc[-1]
        trend = "uptrend" if latest["close"] > latest["sma"] else "downtrend"
        momentum = "overbought" if latest["rsi"] >= self.rules["rsi_sell_min"] else "oversold" if latest["rsi"] <= self.rules["rsi_buy_max"] else "neutral"

        return {
            "close": round(float(latest["close"]), 2),
            "sma": round(float(latest["sma"]), 2),
            "trend": trend,
            "rsi": round(float(latest["rsi"]), 2),
            "momentum": momentum,
            "volatility": round(float(latest["volatility"]), 4),
            "volume": int(latest["volume"]),
            "average_volume": round(float(latest["average_volume"]), 2),
            "volume_ratio": round(float(latest["volume_ratio"]), 2),
        }

    def recommend_action(self, metrics: dict | None = None) -> dict[str, str | list[str]]:
        metrics = metrics or self.calculate_key_metrics()

        buy_reasons = []
        sell_reasons = []

        if metrics["trend"] == "uptrend":
            sell_reasons.append("Price is above the moving average")
        else:
            buy_reasons.append("price is below the moving average")

        if metrics["rsi"] <= self.rules["rsi_buy_max"]:
            buy_reasons.append("RSI is in a favorable entry zone")
        elif metrics["rsi"] >= self.rules["rsi_sell_min"]:
            sell_reasons.append("RSI shows overbought conditions")

        if metrics["volatility"] <= self.rules["volatility_buy_max"]:
            buy_reasons.append("volatility is contained")
        elif metrics["volatility"] >= self.rules["volatility_sell_min"]:
            sell_reasons.append("volatility is elevated")

        if metrics["volume_ratio"] >= self.rules["volume_ratio_buy_min"]:
            buy_reasons.append("volume supports the move")
        if metrics["volume_ratio"] >= self.rules["volume_ratio_sell_min"]:
            sell_reasons.append("volume is unusually high and may confirm distribution")

        if len(sell_reasons) >= 2:
            action = "SELL"
            reason = "; ".join(sell_reasons)
        elif len(buy_reasons) >= 3 and not sell_reasons:
            action = "BUY"
            reason = "; ".join(buy_reasons)
        else:
            action = "HOLD"
            reason = "signals are mixed"

        return {
            "action": action,
            "reason": reason,
            "buy_reasons": buy_reasons,
            "sell_reasons": sell_reasons,
        }

    def format_analysis_summary(self, recommendation: dict[str, str | list[str]], metrics: dict | None = None) -> str:
        metrics = metrics or self.calculate_key_metrics()

        trend_interpretation = (
            "Less Than Last Close - Bullish Trend"
            if metrics["trend"] == "uptrend"
            else "More Than Last Close - Bearish Trend"
        )

        low = self.rules["rsi_sell_min"]
        high = self.rules["rsi_buy_max"]
        if metrics["momentum"] == "oversold":
            momentum_interpretation = f"Buy - Less Than {high}"
        elif metrics["momentum"] == "overbought":
            momentum_interpretation = f"Sell - More Than {low}"
        else:
            momentum_interpretation = f"Neutral - Between {low} & {high}"

        # "volatility_buy_max": 0.03,  # Buy if volatility < 3%
        max_volatility = self.rules["volatility_buy_max"]
        volatility_interpretation = (
            f"Buy - Volatility < {max_volatility * 100}"
            if metrics["volatility"] <= max_volatility
            else f"High Volatility > {max_volatility * 100}"
        )

        # "volume_ratio_buy_min": 1.0, # Buy if volume ratio is > 1
        min_vol = self.rules["volume_ratio_buy_min"]
        volume_interpretation = (
            "High Volume > Average"
            if metrics["volume_ratio"] >= min_vol
            else "Low Volume < Average"
        )

        buy_reasons = recommendation.get("buy_reasons", [])
        sell_reasons = recommendation.get("sell_reasons", [])

        lines = [
            f"Action: {recommendation['action']}",
            f"Close: {metrics['close']:,.2f}",
            f"Simple Moving Average: {metrics['sma']:,.2f} -> {trend_interpretation}",
            f"Relative Strength Index: {metrics['rsi']} -> {momentum_interpretation}",
            f"Volatility: {metrics['volatility'] * 100}% -> {volatility_interpretation}",
            f"Volume: {metrics['volume']:,} | Average Volume: {metrics['average_volume']:,.2f} | Volume Ratio: {metrics['volume_ratio']} -> {volume_interpretation}",
            "",
        ]

        return "\n".join(lines)
