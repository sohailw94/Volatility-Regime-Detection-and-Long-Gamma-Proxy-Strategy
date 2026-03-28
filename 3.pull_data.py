import pandas as pd
import yfinance as yf

from src.config import RAW_DIR


def pull_price_data(
    ticker: str = "QQQ",
    start: str = "2015-01-01",
    end: str | None = None,
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Pull OHLCV data from Yahoo Finance and save to parquet.
    """
    df = yf.download(
        tickers=ticker,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=False,
        progress=False,
    )

    if df.empty:
        raise ValueError(f"No data returned for {ticker}")

    # Flatten columns if needed
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.rename(columns=str.lower)
    df.index.name = "date"

    expected_cols = ["open", "high", "low", "close", "adj close", "volume"]
    existing_cols = [c for c in expected_cols if c in df.columns]
    df = df[existing_cols].copy()

    output_path = RAW_DIR / f"{ticker.lower()}_{interval}.parquet"
    df.to_parquet(output_path)

    return df


if __name__ == "__main__":
    data = pull_price_data("QQQ", start="2015-01-01")
    print(data.tail())
