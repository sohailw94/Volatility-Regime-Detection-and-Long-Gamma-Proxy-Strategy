import numpy as np
import pandas as pd

from src.config import PROCESSED_DIR


def load_signals(ticker: str = "spy") -> pd.DataFrame:
    path = PROCESSED_DIR / f"{ticker.lower()}_hmm_short_term_signals.parquet"
    return pd.read_parquet(path).copy()


def add_forward_returns(df: pd.DataFrame, hold_period: int = 2) -> pd.DataFrame:
    df = df.copy()

    price_col = "adj close" if "adj close" in df.columns else "close"

    df[f"fwd_return_{hold_period}d"] = (
        df[price_col].shift(-hold_period) / df[price_col] - 1
    )

    df[f"abs_fwd_return_{hold_period}d"] = df[f"fwd_return_{hold_period}d"].abs()

    return df


def build_gamma_trades(
    df: pd.DataFrame,
    hold_period: int = 2,
    cost: float = 0.01
) -> pd.DataFrame:
    df = df.copy()
    df = add_forward_returns(df, hold_period)

    trades = df[df["entry_signal"] != 0].copy()

    if trades.empty:
        return pd.DataFrame()

    trades["gross_pnl"] = trades[f"abs_fwd_return_{hold_period}d"]

    trades["net_pnl"] = trades["gross_pnl"] - cost

    trades["win_flag"] = (trades["net_pnl"] > 0).astype(int)

    equity = (1 + trades["net_pnl"].fillna(0)).cumprod()
    trades["equity_curve"] = equity
    trades["running_max"] = equity.cummax()
    trades["drawdown"] = trades["equity_curve"] / trades["running_max"] - 1

    return trades


def summarize_gamma(trades: pd.DataFrame) -> pd.Series:
    if trades.empty:
        return pd.Series({
            "trade_count": 0,
            "win_rate": np.nan,
            "avg_pnl": np.nan,
            "median_pnl": np.nan,
            "std_pnl": np.nan,
            "sharpe_like": np.nan,
            "cumulative_return": np.nan,
            "max_drawdown": np.nan,
        })

    avg = trades["net_pnl"].mean()
    std = trades["net_pnl"].std()

    sharpe = np.nan
    if std and not pd.isna(std) and std > 0:
        sharpe = avg / std * np.sqrt(252 / 2)

    return pd.Series({
        "trade_count": len(trades),
        "win_rate": trades["win_flag"].mean(),
        "avg_pnl": avg,
        "median_pnl": trades["net_pnl"].median(),
        "std_pnl": std,
        "sharpe_like": sharpe,
        "cumulative_return": trades["equity_curve"].iloc[-1] - 1,
        "max_drawdown": trades["drawdown"].min(),
    })


def run_long_gamma_backtest(
    ticker: str = "spy",
    hold_period: int = 3,
    cost: float = 0.01
):
    df = load_signals(ticker)

    trades = build_gamma_trades(
        df,
        hold_period=hold_period,
        cost=cost
    )

    summary = summarize_gamma(trades)

    output_path = PROCESSED_DIR / f"{ticker.lower()}_gamma_trades.parquet"
    trades.to_parquet(output_path)

    print("\n===== LONG GAMMA BACKTEST =====")
    print(f"Hold period: {hold_period} days")
    print(f"Cost assumption: {cost:.2%}")
    print(summary.round(4))

    print(f"\nSaved gamma trades to: {output_path}")

    return trades, summary


if __name__ == "__main__":
    run_long_gamma_backtest(
        ticker="spy",
        hold_period=4,
        cost=0.01
    )