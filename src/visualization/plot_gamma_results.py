from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.config import PROCESSED_DIR, PROJECT_ROOT


FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def load_gamma_trades(ticker: str = "spy") -> pd.DataFrame:
    path = PROCESSED_DIR / f"{ticker.lower()}_gamma_trades.parquet"
    df = pd.read_parquet(path).copy()

    if not isinstance(df.index, pd.DatetimeIndex):
        try:
            df.index = pd.to_datetime(df.index)
        except Exception:
            pass

    return df


def plot_equity_curve(trades: pd.DataFrame, ticker: str) -> Path:
    plt.figure(figsize=(10, 5))
    plt.plot(trades.index, trades["equity_curve"])
    plt.title(f"{ticker.upper()} Long Gamma Proxy - Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Equity Curve")
    plt.tight_layout()

    output_path = FIGURES_DIR / f"{ticker.lower()}_equity_curve.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return output_path


def plot_drawdown(trades: pd.DataFrame, ticker: str) -> Path:
    plt.figure(figsize=(10, 5))
    plt.plot(trades.index, trades["drawdown"])
    plt.title(f"{ticker.upper()} Long Gamma Proxy - Drawdown")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.tight_layout()

    output_path = FIGURES_DIR / f"{ticker.lower()}_drawdown.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return output_path


def plot_return_distribution(trades: pd.DataFrame, ticker: str) -> Path:
    plt.figure(figsize=(10, 5))
    plt.hist(trades["net_pnl"].dropna(), bins=20)
    plt.title(f"{ticker.upper()} Long Gamma Proxy - Trade PnL Distribution")
    plt.xlabel("Net PnL")
    plt.ylabel("Frequency")
    plt.tight_layout()

    output_path = FIGURES_DIR / f"{ticker.lower()}_pnl_distribution.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return output_path


def plot_signal_timeline(trades: pd.DataFrame, ticker: str) -> Path:
    plt.figure(figsize=(10, 5))
    plt.scatter(trades.index, trades["net_pnl"])
    plt.axhline(0, linewidth=1)
    plt.title(f"{ticker.upper()} Long Gamma Proxy - Trade Outcomes Over Time")
    plt.xlabel("Date")
    plt.ylabel("Net PnL")
    plt.tight_layout()

    output_path = FIGURES_DIR / f"{ticker.lower()}_trade_timeline.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return output_path


def summarize_gamma_trades(trades: pd.DataFrame) -> pd.Series:
    if trades.empty:
        return pd.Series(
            {
                "trade_count": 0,
                "win_rate": None,
                "avg_pnl": None,
                "median_pnl": None,
                "std_pnl": None,
                "cumulative_return": None,
                "max_drawdown": None,
            }
        )

    return pd.Series(
        {
            "trade_count": len(trades),
            "win_rate": trades["win_flag"].mean(),
            "avg_pnl": trades["net_pnl"].mean(),
            "median_pnl": trades["net_pnl"].median(),
            "std_pnl": trades["net_pnl"].std(),
            "cumulative_return": trades["equity_curve"].iloc[-1] - 1,
            "max_drawdown": trades["drawdown"].min(),
        }
    )


def run_all_plots(ticker: str = "spy") -> None:
    trades = load_gamma_trades(ticker)

    if trades.empty:
        print(f"No trades found for {ticker}.")
        return

    summary = summarize_gamma_trades(trades)
    print(f"\n===== {ticker.upper()} GAMMA TRADE SUMMARY =====")
    print(summary.round(4))

    eq_path = plot_equity_curve(trades, ticker)
    dd_path = plot_drawdown(trades, ticker)
    hist_path = plot_return_distribution(trades, ticker)
    time_path = plot_signal_timeline(trades, ticker)

    print("\nSaved figures:")
    print(eq_path)
    print(dd_path)
    print(hist_path)
    print(time_path)


if __name__ == "__main__":
    run_all_plots("qqq")
