import numpy as np
import pandas as pd
from scipy import stats
from config import BURST_PERCENTILE, BURST_MIN_DURATION_SEC


def compare_features(baseline_features, cramping_features):
    results = {}

    for feature in ['rms', 'mav', 'var', 'max_amp']:
        baseline_mean = baseline_features[feature].mean()
        cramping_mean = cramping_features[feature].mean()
        percent_increase = ((cramping_mean - baseline_mean) / baseline_mean) * 100
        t_stat, p_value = stats.ttest_ind(baseline_features[feature],
                                          cramping_features[feature])

        results[feature] = {
            'baseline_mean': baseline_mean,
            'cramping_mean': cramping_mean,
            'percent_increase': percent_increase,
            't_stat': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }

        print(f"\n{feature.upper()}:")
        print(f"  Baseline mean: {baseline_mean:.4f}")
        print(f"  Cramping mean: {cramping_mean:.4f}")
        print(f"  Increase: {percent_increase:.2f}%")
        print(f"  p-value: {p_value:.4f}")
        print(f"  Significant: {'YES' if p_value < 0.05 else 'NO'}")

    return results


def detect_bursts(baseline, cramping, fs):
    baseline_bursts, _ = _detect(baseline['rms'].values, fs)
    cramping_bursts, _ = _detect(cramping['rms'].values, fs)

    baseline_hours = len(baseline) / fs / 3600
    cramping_hours = len(cramping) / fs / 3600

    baseline_rate = len(baseline_bursts) / baseline_hours if baseline_hours > 0 else 0
    cramping_rate = len(cramping_bursts) / cramping_hours if cramping_hours > 0 else 0

    print(f"\nBaseline bursts: {len(baseline_bursts)} ({baseline_rate:.1f} events/hour)")
    print(f"Cramping bursts: {len(cramping_bursts)} ({cramping_rate:.1f} events/hour)")

    return baseline_bursts, cramping_bursts


def _detect(emg_rms, fs):
    baseline_portion = emg_rms[:int(len(emg_rms) * 0.2)]
    baseline_mean = np.mean(baseline_portion)
    baseline_std = np.std(baseline_portion)
    threshold = baseline_mean + (np.percentile(emg_rms, BURST_PERCENTILE) * baseline_std)

    above_threshold = emg_rms > threshold
    bursts = []
    in_burst = False
    burst_start = 0

    for i in range(len(above_threshold)):
        if above_threshold[i] and not in_burst:
            burst_start = i
            in_burst = True
        elif not above_threshold[i] and in_burst:
            duration = (i - burst_start) / fs
            if duration >= BURST_MIN_DURATION_SEC:
                bursts.append({
                    'start': burst_start,
                    'end': i,
                    'duration_sec': duration,
                    'peak_amplitude': np.max(emg_rms[burst_start:i])
                })
            in_burst = False

    return bursts, threshold