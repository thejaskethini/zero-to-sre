#!/usr/bin/env python3
"""
=============================================================================
⚡ Predictive Scaling — Time-Series Forecasting for Auto-Scaling
=============================================================================
Description:
    Demonstrates time-series forecasting for proactive infrastructure scaling.
    Uses multiple methods:
    1. Holt-Winters Exponential Smoothing
    2. Simple Moving Average with trend
    3. ARIMA-style differencing

Usage:
    pip install numpy pandas matplotlib
    python predictive_scaler.py

Author: Zero to SRE
License: MIT
=============================================================================
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Tuple, Dict

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


# =============================================================================
# DATA GENERATION — Synthetic traffic with daily/weekly seasonality
# =============================================================================

def generate_traffic_data(days: int = 14, interval_minutes: int = 15) -> pd.DataFrame:
    """Generate realistic traffic data with daily and weekly seasonality."""
    np.random.seed(42)
    n_points = days * 24 * (60 // interval_minutes)

    start = datetime(2025, 1, 6, 0, 0)  # Monday
    timestamps = [start + timedelta(minutes=i * interval_minutes) for i in range(n_points)]

    # Base load
    base = 100

    # Daily seasonality (peak at 2 PM, low at 4 AM)
    hours = np.array([t.hour + t.minute / 60 for t in timestamps])
    daily = 50 * np.sin(2 * np.pi * (hours - 6) / 24)

    # Weekly seasonality (lower on weekends)
    weekday = np.array([t.weekday() for t in timestamps])
    weekly = np.where(weekday < 5, 20, -30)  # Weekday boost, weekend dip

    # Growth trend
    trend = np.linspace(0, 30, n_points)

    # Random noise
    noise = np.random.normal(0, 10, n_points)

    # Combine
    rps = np.maximum(base + daily + weekly + trend + noise, 10)

    return pd.DataFrame({
        'timestamp': timestamps,
        'requests_per_second': rps.round(1),
        'hour': hours,
        'weekday': weekday,
    })


# =============================================================================
# METHOD 1: Holt-Winters Triple Exponential Smoothing
# =============================================================================

def holt_winters_forecast(
    data: np.ndarray,
    season_length: int = 96,  # 24h at 15-min intervals
    horizon: int = 96,
    alpha: float = 0.3,
    beta: float = 0.1,
    gamma: float = 0.3
) -> np.ndarray:
    """
    Triple exponential smoothing for seasonal time series.

    Args:
        data: Historical values
        season_length: Points in one season (96 = 24h at 15-min)
        horizon: How far ahead to forecast
        alpha: Level smoothing (0-1)
        beta: Trend smoothing (0-1)
        gamma: Seasonal smoothing (0-1)
    """
    n = len(data)

    # Initialize
    level = np.mean(data[:season_length])
    trend = (np.mean(data[season_length:2*season_length]) - np.mean(data[:season_length])) / season_length
    seasonal = np.array([data[i] - level for i in range(season_length)])

    levels = np.zeros(n + horizon)
    trends = np.zeros(n + horizon)
    seasons = np.zeros(n + horizon)
    forecast = np.zeros(n + horizon)

    # Fit
    for i in range(n):
        if i < season_length:
            forecast[i] = data[i]
            levels[i] = level
            trends[i] = trend
            seasons[i] = seasonal[i]
            continue

        prev_level = levels[i-1]
        prev_trend = trends[i-1]
        prev_season = seasons[i - season_length]

        levels[i] = alpha * (data[i] - prev_season) + (1 - alpha) * (prev_level + prev_trend)
        trends[i] = beta * (levels[i] - prev_level) + (1 - beta) * prev_trend
        seasons[i] = gamma * (data[i] - levels[i]) + (1 - gamma) * prev_season
        forecast[i] = levels[i] + trends[i] + seasons[i - season_length]

    # Forecast future
    for i in range(n, n + horizon):
        h = i - n + 1
        forecast[i] = levels[n-1] + h * trends[n-1] + seasons[n - season_length + (h % season_length)]

    return forecast[n:]


# =============================================================================
# METHOD 2: Moving Average with Seasonal Decomposition
# =============================================================================

def seasonal_moving_average_forecast(
    data: np.ndarray,
    season_length: int = 96,
    horizon: int = 96
) -> np.ndarray:
    """Forecast using seasonal average of recent cycles."""
    n_seasons = len(data) // season_length
    if n_seasons < 2:
        return np.full(horizon, np.mean(data))

    # Average of last 3 seasonal cycles (or fewer if not enough data)
    n_avg = min(n_seasons, 3)
    seasonal_avg = np.zeros(season_length)

    for i in range(n_avg):
        start = len(data) - (i + 1) * season_length
        end = start + season_length
        seasonal_avg += data[start:end]

    seasonal_avg /= n_avg

    # Add trend
    recent_mean = np.mean(data[-season_length:])
    older_mean = np.mean(data[-2*season_length:-season_length])
    trend_per_step = (recent_mean - older_mean) / season_length

    forecast = np.zeros(horizon)
    for i in range(horizon):
        forecast[i] = seasonal_avg[i % season_length] + trend_per_step * i

    return forecast


# =============================================================================
# SCALING DECISION ENGINE
# =============================================================================

def calculate_scaling_decision(
    forecast: np.ndarray,
    capacity_per_instance: float = 50.0,
    target_utilization: float = 0.7,
    min_instances: int = 2,
    max_instances: int = 50,
    buffer_pct: float = 0.2
) -> Dict:
    """
    Convert traffic forecast into scaling decisions.

    Args:
        forecast: Predicted RPS values
        capacity_per_instance: RPS each instance can handle
        target_utilization: Target utilization (0.7 = 70%)
        min_instances: Minimum instance count
        max_instances: Maximum instance count
        buffer_pct: Additional buffer above forecast
    """
    # Add safety buffer to forecast
    buffered = forecast * (1 + buffer_pct)

    # Calculate required instances
    required = np.ceil(buffered / (capacity_per_instance * target_utilization))
    required = np.clip(required, min_instances, max_instances).astype(int)

    peak_rps = np.max(forecast)
    peak_instances = int(np.max(required))
    min_rps = np.min(forecast)
    min_required = int(np.min(required))

    return {
        'peak_rps': round(peak_rps, 1),
        'min_rps': round(min_rps, 1),
        'peak_instances': peak_instances,
        'min_instances_needed': min_required,
        'instance_schedule': required,
        'estimated_cost_per_hour': peak_instances * 0.05,  # ~$0.05/instance/hour
    }


# =============================================================================
# VISUALIZATION
# =============================================================================

def visualize_forecast(
    df: pd.DataFrame,
    forecast_hw: np.ndarray,
    forecast_sma: np.ndarray,
    scaling: Dict,
    output_file: str = "predictive_scaling_forecast.png"
):
    """Create visualization of forecast and scaling decisions."""
    if not HAS_MATPLOTLIB:
        print("⏭️  Skipping visualization (matplotlib not installed)")
        return

    fig, axes = plt.subplots(3, 1, figsize=(16, 14), sharex=False)
    fig.suptitle('⚡ Predictive Scaling — Traffic Forecast & Capacity Planning',
                 fontsize=16, fontweight='bold', color='white')
    fig.patch.set_facecolor('#0d1117')

    actual_ts = df['timestamp'].values
    actual_rps = df['requests_per_second'].values

    # Forecast timestamps
    last_ts = df['timestamp'].iloc[-1]
    interval = timedelta(minutes=15)
    forecast_ts = [last_ts + interval * (i+1) for i in range(len(forecast_hw))]

    # Plot 1: Historical + Forecast
    ax1 = axes[0]
    ax1.plot(actual_ts, actual_rps, color='#4fc3f7', linewidth=0.8, alpha=0.7, label='Actual Traffic')
    ax1.plot(forecast_ts, forecast_hw, color='#f4c542', linewidth=2, label='Holt-Winters Forecast')
    ax1.plot(forecast_ts, forecast_sma, color='#43a047', linewidth=2, linestyle='--', label='Seasonal MA Forecast')
    ax1.axvline(x=actual_ts[-1], color='#ef5350', linestyle=':', alpha=0.7, label='Forecast Start')
    ax1.set_ylabel('Requests/sec', color='white')
    ax1.set_title('Traffic Forecast (Next 24 Hours)', fontweight='bold', color='white')
    ax1.legend(loc='upper left', facecolor='#1a1a2e', edgecolor='#333')
    ax1.grid(True, alpha=0.2)
    ax1.set_facecolor('#1a1a2e')
    ax1.tick_params(colors='white')

    # Plot 2: Instance Count
    ax2 = axes[1]
    schedule = scaling['instance_schedule']
    ax2.fill_between(forecast_ts, schedule, alpha=0.3, color='#7c4dff')
    ax2.step(forecast_ts, schedule, color='#7c4dff', linewidth=2, where='mid', label='Required Instances')
    ax2.axhline(y=scaling['peak_instances'], color='#ef5350', linestyle='--', alpha=0.7,
                label=f'Peak: {scaling["peak_instances"]} instances')
    ax2.set_ylabel('Instances', color='white')
    ax2.set_title('Pre-Scaling Schedule', fontweight='bold', color='white')
    ax2.legend(loc='upper left', facecolor='#1a1a2e', edgecolor='#333')
    ax2.grid(True, alpha=0.2)
    ax2.set_facecolor('#1a1a2e')
    ax2.tick_params(colors='white')

    # Plot 3: Daily pattern (last 7 days average)
    ax3 = axes[2]
    df_recent = df.tail(7 * 96)  # Last 7 days
    hourly_avg = df_recent.groupby(df_recent['timestamp'].dt.hour)['requests_per_second'].mean()
    ax3.bar(hourly_avg.index, hourly_avg.values, color='#4fc3f7', alpha=0.7, edgecolor='#2196f3')
    ax3.set_xlabel('Hour of Day', color='white')
    ax3.set_ylabel('Avg RPS', color='white')
    ax3.set_title('Daily Traffic Pattern (7-Day Average)', fontweight='bold', color='white')
    ax3.set_xticks(range(0, 24, 2))
    ax3.grid(True, alpha=0.2, axis='y')
    ax3.set_facecolor('#1a1a2e')
    ax3.tick_params(colors='white')

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='#0d1117')
    print(f"📊 Visualization saved to: {output_file}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("⚡ Predictive Scaling — Traffic Forecasting")
    print("=" * 60)

    # Step 1: Generate data
    print("\n📊 Step 1: Generating 14 days of traffic data...")
    df = generate_traffic_data(days=14, interval_minutes=15)
    print(f"  Generated {len(df)} data points ({df['timestamp'].min()} to {df['timestamp'].max()})")

    values = df['requests_per_second'].values
    season_length = 96  # 24 hours at 15-min intervals
    horizon = 96        # Forecast 24 hours ahead

    # Step 2: Forecast
    print("\n🔮 Step 2: Running forecasting models...")

    # Method 1: Holt-Winters
    forecast_hw = holt_winters_forecast(values, season_length, horizon)
    print(f"  Holt-Winters: Peak forecast = {np.max(forecast_hw):.1f} RPS")

    # Method 2: Seasonal Moving Average
    forecast_sma = seasonal_moving_average_forecast(values, season_length, horizon)
    print(f"  Seasonal MA:  Peak forecast = {np.max(forecast_sma):.1f} RPS")

    # Use ensemble (average of both methods)
    forecast_ensemble = (forecast_hw + forecast_sma) / 2
    print(f"  Ensemble:     Peak forecast = {np.max(forecast_ensemble):.1f} RPS")

    # Step 3: Scaling Decision
    print("\n🚀 Step 3: Calculating scaling decisions...")
    scaling = calculate_scaling_decision(forecast_ensemble)

    print(f"\n  📈 Forecast Summary (next 24h):")
    print(f"     Peak Traffic:     {scaling['peak_rps']} RPS")
    print(f"     Min Traffic:      {scaling['min_rps']} RPS")
    print(f"     Peak Instances:   {scaling['peak_instances']}")
    print(f"     Min Instances:    {scaling['min_instances_needed']}")
    print(f"     Est. Peak Cost:   ${scaling['estimated_cost_per_hour']:.2f}/hour")

    # Step 4: Generate scaling schedule
    print("\n📋 Step 4: Pre-Scaling Schedule:")
    schedule = scaling['instance_schedule']
    for i in range(0, horizon, 4):  # Every hour
        ts = df['timestamp'].iloc[-1] + timedelta(minutes=15 * (i + 1))
        rps = forecast_ensemble[i]
        instances = schedule[i]
        bar = "█" * instances
        print(f"  {ts.strftime('%H:%M')} | {rps:6.1f} RPS | {instances:2d} instances | {bar}")

    # Step 5: Visualize
    print("\n📊 Step 5: Generating visualization...")
    visualize_forecast(df, forecast_hw, forecast_sma, scaling)

    print("\n✅ Done! Use this forecast to pre-scale your infrastructure.")
    print("💡 Tip: Schedule this script as a cron job to run every 6 hours.")


if __name__ == "__main__":
    main()
