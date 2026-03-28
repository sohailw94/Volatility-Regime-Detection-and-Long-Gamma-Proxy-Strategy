# Volatility Regime Detection and Long Gamma Proxy Strategy

## Overview

This project investigates whether volatility expansion can be predicted using only real price data. The original hypothesis was that compressed volatility regimes would lead to future expansion. After testing that idea through feature design, decile analysis, and threshold sweeps, the evidence showed that compression alone did not predict expansion in SPY daily data.

The project then pivoted toward regime-based volatility detection using a Hidden Markov Model (HMM). While directional continuation strategies underperformed, the signal consistently identified periods of elevated realized volatility and large absolute price moves. This led to a non-directional long gamma proxy strategy that monetizes magnitude rather than direction.

## Core Research Journey

### Phase 1: Compression Hypothesis
- Built realized-volatility term structure features
- Defined compression using:
  - short vs long realized vol ratios
  - rolling volatility percentile
  - range compression
  - band-width compression
- Tested whether compression predicted future volatility expansion

### Result
Compression did **not** predict expansion. In fact, low-volatility regimes tended to remain low-volatility.

### Phase 2: Regime Detection with HMM
- Built an HMM using price-derived regime features
- Inferred hidden volatility states
- Identified high-volatility regimes using state-level realized-vol statistics

### Result
The HMM successfully separated low-, medium-, and high-volatility environments.

### Phase 3: Directional Strategies
- Tested breakout continuation strategies in high-volatility regimes
- Applied trend filters and return-sign confirmation

### Result
Directional strategies underperformed. The signal captured magnitude, but not direction.

### Phase 4: Long Gamma Proxy
- Reframed the signal as a non-directional volatility strategy
- Backtested a long gamma proxy using:
  - absolute forward returns
  - fixed cost assumption for option premium / decay / execution friction

### Result
The signal showed positive expectancy and strong risk-adjusted performance on SPY and QQQ under reasonable cost assumptions.

---

## Key Insight

The main finding is:

> The signal predicts **when** large moves are likely, but not **which direction** they will take.

This makes it better suited for volatility-based strategies than directional trading.

---

## Data

- Daily OHLCV price data
- Primary source: Yahoo Finance via `yfinance`
- No simulated Greeks in the core model
- No option chain dependency for v1

---

## Feature Design

Main features include:

- `rv_5`, `rv_20`, `rv_60`
- `rv_ratio_5_20`
- `rv_ratio_20_60`
- `rv_20_pct_252`
- `range_ratio`
- `bb_width_20`
- `abs_ret_1d`

These features are used to characterize volatility state and feed the HMM.

---

## HMM Regime Logic

The HMM is fit on normalized price-derived regime features and infers hidden states such as:

- low-volatility regime
- medium/normal regime
- high-volatility regime

The high-volatility state is identified using the state with the highest average `rv_20`.

---

## Strategy Logic

### Signal
Enter when:
- the HMM assigns high probability to the high-volatility regime
- breakout / impulse filters confirm meaningful movement
- price-based filters indicate active volatility expansion

### Directional backtests
Directional long/short continuation strategies were tested and rejected.

### Final strategy
The final strategy uses a **long gamma proxy**:

- Enter on signal
- Hold for 1–4 days
- Approximate payoff using absolute forward returns
- Subtract a fixed cost assumption to simulate option premium / decay

---

## Example Results

### SPY
- Positive expectancy under 1-day, 2-day, and 4-day holding periods
- Strong Sharpe-like performance under a 1% cost assumption

### QQQ
- Stronger performance than SPY
- Higher win rate and larger average trade PnL
- Suggests the signal is more powerful in higher-beta assets

---

## Repo Structure

```text
src/
  data/
  features/
  signals/
  backtest/
  visualization/ 
