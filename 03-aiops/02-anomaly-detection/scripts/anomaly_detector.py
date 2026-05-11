#!/usr/bin/env python3
"""
=============================================================================
📉 Anomaly Detection for Metrics — Multi-Method Detector
=============================================================================
Description:
    A production-inspired anomaly detection script that demonstrates three
    different approaches to detecting anomalies in time-series metrics:
    
    1. Z-Score (Statistical)     — Fast, interpretable, assumes normality
    2. Isolation Forest (ML)     — Handles non-linear patterns
    3. Rolling Statistics        — Moving average with dynamic thresholds

Usage:
    pip install numpy pandas scikit-learn matplotlib
    python anomaly_detector.py

Output:
    - Console: Detection results with precision/recall for each method
    - File: anomaly_detection_results.png (visualization)

Author: Zero to SRE
License: MIT
=============================================================================
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Tuple, List, Dict

# Optional: sklearn for Isolation Forest
try:
    from sklearn.ensemble import IsolationForest
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("⚠️  scikit-learn not installed. Isolation Forest will be skipped.")
    print("   Install with: pip install scikit-learn")

# Optional: matplotlib for visualization
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️  matplotlib not installed. Visualization will be skipped.")
    print("   Install with: pip install matplotlib")


# =============================================================================
# DATA GENERATION — Synthetic metrics with injected anomalies
# =============================================================================

def generate_synthetic_metrics(
    n_points: int = 1440,
    interval_minutes: int = 1,
    anomaly_ratio: float = 0.01,
    seed: int = 42
) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Generate synthetic time-series metrics that mimic real application behavior.
    
    Creates data with:
    - Daily seasonality (higher during business hours)
    - Random noise
    - Injected anomalies (spikes and dips)
    
    Args:
        n_points: Number of data points (default: 1440 = 1 day at 1-min intervals)
        interval_minutes: Time between data points
        anomaly_ratio: Fraction of points that are anomalies
        seed: Random seed for reproducibility
    
    Returns:
        Tuple of (DataFrame with timestamps and values, boolean array of true anomaly positions)
    """
    np.random.seed(seed)
    
    # Create timestamps
    start_time = datetime(2025, 1, 15, 0, 0, 0)
    timestamps = [start_time + timedelta(minutes=i * interval_minutes) for i in range(n_points)]
    
    # --- Base signal: Daily seasonality ---
    # Simulates higher load during business hours (9 AM - 6 PM)
    hours = np.array([t.hour + t.minute / 60 for t in timestamps])
    seasonality = 50 + 30 * np.sin(2 * np.pi * (hours - 6) / 24)  # Peak around noon
    
    # --- Add random noise ---
    noise = np.random.normal(0, 5, n_points)
    
    # --- Combine into base metric ---
    values = seasonality + noise
    
    # --- Inject anomalies ---
    n_anomalies = max(int(n_points * anomaly_ratio), 5)
    anomaly_indices = np.random.choice(n_points, n_anomalies, replace=False)
    true_anomalies = np.zeros(n_points, dtype=bool)
    
    for idx in anomaly_indices:
        # Randomly choose between spike (high) and dip (low) anomalies
        if np.random.random() > 0.3:
            # Spike anomaly: 3-5x the normal noise
            values[idx] += np.random.uniform(25, 50)
        else:
            # Dip anomaly: sudden drop
            values[idx] -= np.random.uniform(25, 40)
        true_anomalies[idx] = True
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'value': values,
        'is_anomaly': true_anomalies
    })
    
    print(f"📊 Generated {n_points} data points with {n_anomalies} injected anomalies")
    return df, true_anomalies


# =============================================================================
# METHOD 1: Z-Score Anomaly Detection
# =============================================================================

def detect_zscore(
    values: np.ndarray,
    threshold: float = 3.0
) -> np.ndarray:
    """
    Detect anomalies using Z-Score (standard deviations from mean).
    
    How it works:
    - Calculate mean and standard deviation of the data
    - Any point > threshold standard deviations from mean is an anomaly
    
    Pros: Simple, fast, interpretable
    Cons: Assumes normal distribution, no seasonality awareness
    
    Args:
        values: Array of metric values
        threshold: Number of standard deviations (default: 3.0)
    
    Returns:
        Boolean array where True = anomaly
    """
    mean = np.mean(values)
    std = np.std(values)
    
    # Avoid division by zero
    if std == 0:
        return np.zeros(len(values), dtype=bool)
    
    z_scores = np.abs((values - mean) / std)
    anomalies = z_scores > threshold
    
    return anomalies


# =============================================================================
# METHOD 2: Isolation Forest (Machine Learning)
# =============================================================================

def detect_isolation_forest(
    values: np.ndarray,
    contamination: float = 0.02
) -> np.ndarray:
    """
    Detect anomalies using Isolation Forest algorithm.
    
    How it works:
    - Randomly selects a feature and split value
    - Anomalies are isolated in fewer splits (shorter path length)
    - Normal points require more splits to isolate
    
    Pros: Handles non-linear patterns, no distribution assumptions
    Cons: Requires tuning contamination parameter
    
    Args:
        values: Array of metric values
        contamination: Expected proportion of anomalies (default: 0.02)
    
    Returns:
        Boolean array where True = anomaly
    """
    if not HAS_SKLEARN:
        print("  ⏭️  Skipping Isolation Forest (scikit-learn not installed)")
        return np.zeros(len(values), dtype=bool)
    
    # Reshape for sklearn (requires 2D input)
    X = values.reshape(-1, 1)
    
    # Add rate of change as a second feature (makes detection better)
    rate_of_change = np.diff(values, prepend=values[0])
    X = np.column_stack([values, rate_of_change])
    
    # Train Isolation Forest
    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100,  # Number of trees
        max_samples='auto'
    )
    
    # Predict: -1 = anomaly, 1 = normal
    predictions = model.fit_predict(X)
    anomalies = predictions == -1
    
    return anomalies


# =============================================================================
# METHOD 3: Rolling Statistics (Moving Average + Dynamic Threshold)
# =============================================================================

def detect_rolling_stats(
    values: np.ndarray,
    window: int = 60,
    n_sigmas: float = 3.0
) -> np.ndarray:
    """
    Detect anomalies using rolling mean and standard deviation.
    
    How it works:
    - Calculate rolling mean and std over a sliding window
    - A point is anomalous if it's outside mean ± n_sigmas * std
    - Adapts to local trends and seasonality
    
    Pros: Handles trends and seasonality, simple to understand
    Cons: Window size requires tuning, lagging detection
    
    Args:
        values: Array of metric values
        window: Size of rolling window (default: 60 = 1 hour at 1-min intervals)
        n_sigmas: Number of standard deviations for threshold
    
    Returns:
        Boolean array where True = anomaly
    """
    series = pd.Series(values)
    
    # Calculate rolling statistics
    rolling_mean = series.rolling(window=window, center=True, min_periods=1).mean()
    rolling_std = series.rolling(window=window, center=True, min_periods=1).std()
    
    # Fill NaN std with global std (for edges of the series)
    rolling_std = rolling_std.fillna(series.std())
    
    # Detect anomalies: points outside the dynamic band
    upper_band = rolling_mean + n_sigmas * rolling_std
    lower_band = rolling_mean - n_sigmas * rolling_std
    
    anomalies = (series > upper_band) | (series < lower_band)
    
    return anomalies.values


# =============================================================================
# EVALUATION — Compare detection methods
# =============================================================================

def evaluate_method(
    detected: np.ndarray,
    actual: np.ndarray,
    method_name: str
) -> Dict[str, float]:
    """
    Evaluate anomaly detection performance.
    
    Args:
        detected: Boolean array of detected anomalies
        actual: Boolean array of true anomalies
        method_name: Name of the method for display
    
    Returns:
        Dictionary with precision, recall, and F1 score
    """
    true_positives = np.sum(detected & actual)
    false_positives = np.sum(detected & ~actual)
    false_negatives = np.sum(~detected & actual)
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    n_detected = np.sum(detected)
    
    print(f"\n  Method: {method_name}")
    print(f"    Detected: {n_detected} anomalies")
    print(f"    True Positives: {true_positives} | False Positives: {false_positives} | Missed: {false_negatives}")
    print(f"    Precision: {precision:.1%} | Recall: {recall:.1%} | F1: {f1:.1%}")
    
    return {
        'method': method_name,
        'detected': n_detected,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }


# =============================================================================
# VISUALIZATION
# =============================================================================

def visualize_results(
    df: pd.DataFrame,
    results: Dict[str, np.ndarray],
    output_file: str = "anomaly_detection_results.png"
) -> None:
    """
    Create a visualization comparing all detection methods.
    """
    if not HAS_MATPLOTLIB:
        print("\n⏭️  Skipping visualization (matplotlib not installed)")
        return
    
    n_methods = len(results)
    fig, axes = plt.subplots(n_methods + 1, 1, figsize=(16, 4 * (n_methods + 1)), sharex=True)
    fig.suptitle('📉 Anomaly Detection — Method Comparison', fontsize=16, fontweight='bold')
    
    timestamps = df['timestamp'].values
    values = df['value'].values
    true_anomalies = df['is_anomaly'].values
    
    # Plot 1: Raw data with true anomalies
    ax = axes[0]
    ax.plot(timestamps, values, color='#4fc3f7', linewidth=0.8, alpha=0.8, label='Metric')
    ax.scatter(
        timestamps[true_anomalies], values[true_anomalies],
        color='#ef5350', s=50, zorder=5, label='True Anomalies', marker='x'
    )
    ax.set_ylabel('Value')
    ax.set_title('Raw Data with True Anomalies', fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#1a1a2e')
    
    # Plot each method
    colors = ['#f4c542', '#43a047', '#7c4dff']
    for i, (method_name, detected) in enumerate(results.items()):
        ax = axes[i + 1]
        ax.plot(timestamps, values, color='#4fc3f7', linewidth=0.8, alpha=0.5)
        
        # True anomalies
        ax.scatter(
            timestamps[true_anomalies], values[true_anomalies],
            color='#ef5350', s=40, zorder=5, label='True', marker='x'
        )
        
        # Detected anomalies
        ax.scatter(
            timestamps[detected], values[detected],
            color=colors[i % len(colors)], s=30, zorder=4,
            label='Detected', marker='o', facecolors='none', linewidths=2
        )
        
        ax.set_ylabel('Value')
        ax.set_title(f'{method_name}', fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#1a1a2e')
    
    axes[-1].set_xlabel('Time')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='#0d1117')
    print(f"\n📊 Visualization saved to: {output_file}")


# =============================================================================
# MAIN — Run all methods and compare
# =============================================================================

def main():
    """Main execution function."""
    print("=" * 60)
    print("📉 Anomaly Detection for Metrics")
    print("=" * 60)
    
    # Step 1: Generate data
    print("\n🔧 Step 1: Generating synthetic metrics data...")
    df, true_anomalies = generate_synthetic_metrics(
        n_points=1440,      # 24 hours at 1-min intervals
        anomaly_ratio=0.01  # 1% anomalies (~14 points)
    )
    
    values = df['value'].values
    
    # Step 2: Run detection methods
    print("\n🔍 Step 2: Running anomaly detection methods...")
    
    results = {}
    evaluations = []
    
    # Method 1: Z-Score
    print("\n" + "-" * 40)
    print("📊 Method 1: Z-Score")
    zscore_detected = detect_zscore(values, threshold=3.0)
    results['Z-Score (σ=3)'] = zscore_detected
    evaluations.append(evaluate_method(zscore_detected, true_anomalies, 'Z-Score'))
    
    # Method 2: Isolation Forest
    if HAS_SKLEARN:
        print("\n" + "-" * 40)
        print("🌲 Method 2: Isolation Forest")
        iforest_detected = detect_isolation_forest(values, contamination=0.02)
        results['Isolation Forest'] = iforest_detected
        evaluations.append(evaluate_method(iforest_detected, true_anomalies, 'Isolation Forest'))
    
    # Method 3: Rolling Statistics
    print("\n" + "-" * 40)
    print("📈 Method 3: Rolling Statistics")
    rolling_detected = detect_rolling_stats(values, window=60, n_sigmas=3.0)
    results['Rolling Stats (w=60)'] = rolling_detected
    evaluations.append(evaluate_method(rolling_detected, true_anomalies, 'Rolling Statistics'))
    
    # Step 3: Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    summary_df = pd.DataFrame(evaluations)
    print(summary_df.to_string(index=False))
    
    # Step 4: Recommendation
    best = max(evaluations, key=lambda x: x['f1'])
    print(f"\n🏆 Best method by F1 Score: {best['method']} (F1: {best['f1']:.1%})")
    
    print("\n💡 Recommendations:")
    print("  • Start with Rolling Statistics for most use cases")
    print("  • Use Z-Score for quick, simple detection")
    print("  • Use Isolation Forest when patterns are complex")
    print("  • In production, combine methods (ensemble) for best results")
    
    # Step 5: Visualize
    print("\n📊 Step 3: Generating visualization...")
    visualize_results(df, results)
    
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
