# Volatility Regime Detection and Long Gamma Proxy Strategy

## Overview

This project explores whether volatility expansion can be predicted using only price-based features. The initial hypothesis—low volatility (compression) leads to future expansion—was tested and rejected through empirical analysis.

The research then pivoted to regime detection using a Hidden Markov Model (HMM). While directional strategies underperformed, the model consistently identified periods of elevated realized volatility and large absolute price moves.

This led to the development of a **non-directional long gamma proxy strategy**, where returns are driven by the magnitude of price movements rather than direction.

---

## Key Insight

> The signal predicts **when large moves are likely**, but not **which direction they will take**.

This makes it more suitable for **volatility-based strategies** than directional trading.

---

## Research Journey

### 1. Compression Hypothesis (Rejected)

* Built features based on:

  * short vs long realized volatility ratios
  * rolling volatility percentiles
  * price range compression
  * Bollinger Band width
* Tested whether low-volatility regimes predict expansion

**Result:**
Compression does not predict expansion. Low-volatility regimes tend to persist.

---

### 2. Regime Detection with HMM

* Built an HMM using normalized price-based features
* Identified latent volatility regimes:

  * low-vol
  * normal
  * high-vol

**Result:**
The model successfully separates volatility regimes.

---

### 3. Directional Strategies (Rejected)

* Tested breakout + trend continuation strategies in high-vol regimes
* Applied filters:

  * trend alignment
  * return sign confirmation
  * volatility continuation

**Result:**
Directional strategies underperformed despite strong signal activity.

---

### 4. Long Gamma Proxy Strategy (Final)

Reframed the signal into a **non-directional strategy**:

* Enter when high-volatility regime is detected

* Hold for short horizons (1–4 days)

* Profit from absolute returns:

  ```
  PnL = |return| - cost
  ```

* Cost approximates:

  * option premium
  * decay
  * execution friction

---

## Strategy Logic

**Signal triggers when:**

* HMM indicates high-volatility regime
* breakout / impulse confirms movement
* short-term volatility is elevated

**Execution:**

* No directional bet
* Returns depend on magnitude of price movement

---

## Results Summary

| Asset | Hold | Cost | Trades | Avg PnL | Win Rate | Sharpe | Max DD |
| ----- | ---- | ---- | ------ | ------- | -------- | ------ | ------ |
| SPY   | 2D   | 1%   | 20     | 0.71%   | 55%      | 4.7    | -2.0%  |
| SPY   | 4D   | 1%   | 20     | 1.52%   | 65%      | 8.2    | -1.4%  |
| QQQ   | 4D   | 1%   | 29     | 2.03%   | 75.9%    | 8.7    | -1.6%  |

**Observations:**

* Performance improves with longer holding periods
* Signal is stronger in higher-beta assets (QQQ vs SPY)
* Volatility expansion appears persistent and clustered

---

## Data

* Daily OHLCV data
* Source: `yfinance`
* No options data required (v1)
* No simulated Greeks

---

## Feature Set

* Realized volatility: `rv_5`, `rv_20`, `rv_60`
* Term structure: `rv_ratio_5_20`, `rv_ratio_20_60`
* Volatility percentile
* Price range compression
* Bollinger Band width
* Absolute returns

---

## Project Structure

```
src/
  data/           # data ingestion
  features/       # feature engineering
  signals/        # HMM + signal logic
  backtest/       # strategy evaluation
  visualization/  # plots and charts

data/
  raw/
  processed/

outputs/
  figures/
```

---

## How to Run

```bash
python -m src.data.pull_data
python -m src.features.build_features
python -m src.signals.hmm_short_term_continuation
python -m src.backtest.run_long_gamma_backtest
python -m src.visualization.plot_gamma_results
```

For QQQ:

```bash
python -m src.signals.hmm_short_term_continuation_qqq
python -m src.backtest.run_long_gamma_backtest_qqq
```

---

## Limitations

* Small sample size (20–30 trades per asset)
* Proxy payoff (not actual options execution)
* Results sensitive to transaction cost assumptions

---

## Key Takeaways

* Volatility is easier to predict than direction
* High-volatility regimes are persistent and clustered
* Non-directional strategies better capture this behavior
* Aligning strategy with signal type is critical

---


## Disclaimer

This project is for research and educational purposes only. It is not investment advice and is not intended for production trading use.

  visualization/
