import numpy as np
import pandas as pd
from config import FEATURE_WINDOW_SEC


def extract_features(baseline, cramping, fs):
    baseline_features = _extract(baseline['emg_voltage'].values, fs)
    cramping_features = _extract(cramping['emg_voltage'].values, fs)
    return baseline_features, cramping_features


def _extract(emg_signal, fs):
    window_samples = int(FEATURE_WINDOW_SEC * fs)
    n_windows = len(emg_signal) // window_samples

    features = {
        'rms': [],
        'mav': [],
        'var': [],
        'max_amp': []
    }

    for i in range(n_windows):
        window = emg_signal[i * window_samples:(i + 1) * window_samples]
        features['rms'].append(np.sqrt(np.mean(window**2)))
        features['mav'].append(np.mean(np.abs(window)))
        features['var'].append(np.var(window))
        features['max_amp'].append(np.max(np.abs(window)))

    return pd.DataFrame(features)