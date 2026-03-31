import os

# ========================================
# PATHS
# ========================================
BASELINE_PATH = os.path.join('data', 'myoware_data', 'baseline_samiya_myoware_03_16_1833.csv')
CRAMPING_PATH = os.path.join('data', 'myoware_data', 'cramps_samiya_03_19_1537.csv')
RESULTS_DIR = 'results'
PLOT_PATH = os.path.join(RESULTS_DIR, 'emg_cramp_analysis.png')
RESULTS_CSV = os.path.join(RESULTS_DIR, 'emg_analysis_results.csv')

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