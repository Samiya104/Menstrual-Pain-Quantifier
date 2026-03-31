import pandas as pd
import numpy as np
from config import BASELINE_PATH, CRAMPING_PATH, RESULTS_DIR, RESULTS_CSV
from src.preprocess import load_data, smooth_emg
from src.features import extract_features
from src.analysis import compare_features, detect_bursts
from src.visualize import plot_all
from src.mlflow_logging import log_run
import os

# ========================================
# SETUP
# ========================================
os.makedirs(RESULTS_DIR, exist_ok=True)

# ========================================
# LOAD & PREPROCESS
# ========================================
baseline, cramping, fs = load_data(BASELINE_PATH, CRAMPING_PATH)
baseline, cramping = smooth_emg(baseline, cramping, fs)

# ========================================
# FEATURES & ANALYSIS
# ========================================
baseline_features, cramping_features = extract_features(baseline, cramping, fs)
stats = compare_features(baseline_features, cramping_features)
baseline_bursts, cramping_bursts = detect_bursts(baseline, cramping, fs)

# ========================================
# VISUALIZE
# ========================================
plot_all(baseline, cramping, baseline_features, cramping_features, baseline_bursts, cramping_bursts)

# ========================================
# SAVE RESULTS
# ========================================
results_df = pd.DataFrame({
    'metric': ['baseline_mean_rms', 'cramping_mean_rms', 'percent_increase',
               'baseline_bursts', 'cramping_bursts'],
    'value': [
        baseline['rms'].mean(),
        cramping['rms'].mean(),
        ((cramping['rms'].mean() - baseline['rms'].mean()) / baseline['rms'].mean()) * 100,
        len(baseline_bursts),
        len(cramping_bursts)
    ]
})
results_df.to_csv(RESULTS_CSV, index=False)

# ========================================
# MLFLOW
# ========================================
log_run(fs, stats, baseline_bursts, cramping_bursts, baseline, cramping)