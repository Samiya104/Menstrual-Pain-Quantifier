import os

# ========================================
# PATHS
# ========================================
BASELINE_PATH = os.path.join('data', 'myoware_data', 'baseline.csv')
CRAMPING_PATH = os.path.join('data', 'myoware_data', 'cramps.csv')
RESULTS_DIR = 'results'
PLOT_PATH = os.path.join(RESULTS_DIR, 'cramp_analysis.png')
RESULTS_CSV = os.path.join(RESULTS_DIR, 'cramp_analysis_results.csv')

# ========================================
# SIGNAL PARAMETERS
# ========================================
ADC_MAX = 1023.0
VOLTAGE_MAX = 5.0

# ========================================
# PREPROCESSING
# ========================================
SMOOTHING_WINDOW_MS = 500

# ========================================
# FEATURE EXTRACTION
# ========================================
FEATURE_WINDOW_SEC = 5

# ========================================
# BURST DETECTION
# ========================================
BURST_PERCENTILE = 75
BURST_MIN_DURATION_SEC = 0.5

# ========================================
# MLFLOW
# ========================================
EXPERIMENT_NAME = 'cramp_emg_analysis'