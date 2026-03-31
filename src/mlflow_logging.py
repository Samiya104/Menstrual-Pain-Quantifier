import mlflow
import pandas as pd
from config import EXPERIMENT_NAME, PLOT_PATH, RESULTS_CSV, BURST_PERCENTILE, BURST_MIN_DURATION_SEC, FEATURE_WINDOW_SEC, SMOOTHING_WINDOW_MS


def log_run(fs, stats, baseline_bursts, cramping_bursts, baseline, cramping):
    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run():

        # Parameters
        mlflow.log_param("sampling_rate_hz", fs)
        mlflow.log_param("smoothing_window_ms", SMOOTHING_WINDOW_MS)
        mlflow.log_param("burst_percentile_threshold", BURST_PERCENTILE)
        mlflow.log_param("burst_min_duration_sec", BURST_MIN_DURATION_SEC)
        mlflow.log_param("feature_window_sec", FEATURE_WINDOW_SEC)

        # Feature metrics
        for feature, values in stats.items():
            mlflow.log_metric(f"baseline_{feature}", values['baseline_mean'])
            mlflow.log_metric(f"cramping_{feature}", values['cramping_mean'])
            mlflow.log_metric(f"pct_increase_{feature}", values['percent_increase'])
            mlflow.log_metric(f"pvalue_{feature}", values['p_value'])
            mlflow.log_metric(f"tstat_{feature}", values['t_stat'])

        # Burst metrics
        baseline_hours = len(baseline) / fs / 3600
        cramping_hours = len(cramping) / fs / 3600

        baseline_rate = len(baseline_bursts) / baseline_hours if baseline_hours > 0 else 0
        cramping_rate = len(cramping_bursts) / cramping_hours if cramping_hours > 0 else 0

        mlflow.log_metric("baseline_burst_count", len(baseline_bursts))
        mlflow.log_metric("cramping_burst_count", len(cramping_bursts))
        mlflow.log_metric("baseline_burst_rate_per_hr", baseline_rate)
        mlflow.log_metric("cramping_burst_rate_per_hr", cramping_rate)

        # Signal variability
        baseline_cv = baseline['emg_voltage'].std() / baseline['emg_voltage'].mean()
        cramping_cv = cramping['emg_voltage'].std() / cramping['emg_voltage'].mean()
        mlflow.log_metric("baseline_cv", baseline_cv)
        mlflow.log_metric("cramping_cv", cramping_cv)

        # Artifacts
        mlflow.log_artifact(PLOT_PATH)
        mlflow.log_artifact(RESULTS_CSV)

        print("MLflow run logged successfully.")