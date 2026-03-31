import pandas as pd
import numpy as np
from config import ADC_MAX, VOLTAGE_MAX, SMOOTHING_WINDOW_MS


def find_header(filepath):
    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            if 'timestamp,emg' in line:
                return i
    return 0


def load_data(baseline_path, cramping_path):
    skip_baseline = find_header(baseline_path)
    skip_cramping = find_header(cramping_path)

    baseline = pd.read_csv(baseline_path, skiprows=skip_baseline)
    cramping = pd.read_csv(cramping_path, skiprows=skip_cramping)

    baseline.columns = baseline.columns.str.strip()
    cramping.columns = cramping.columns.str.strip()

    baseline['emg_voltage'] = (baseline['emg'] / ADC_MAX) * VOLTAGE_MAX
    cramping['emg_voltage'] = (cramping['emg'] / ADC_MAX) * VOLTAGE_MAX

    fs = int(1000 / baseline['timestamp'].diff().median())

    print(f"Baseline: {len(baseline)} points at {fs} Hz")
    print(f"Cramping: {len(cramping)} points at {fs} Hz")

    return baseline, cramping, fs


def smooth_emg(baseline, cramping, fs):
    def _smooth(emg_signal, fs, window_ms):
        window_size = max(1, int((window_ms / 1000) * fs))
        return np.convolve(emg_signal, np.ones(window_size) / window_size, mode='same')

    baseline['rms'] = _smooth(baseline['emg_voltage'].values, fs, SMOOTHING_WINDOW_MS)
    cramping['rms'] = _smooth(cramping['emg_voltage'].values, fs, SMOOTHING_WINDOW_MS)

    return baseline, cramping