import numpy as np
import matplotlib.pyplot as plt
from config import PLOT_PATH


def plot_all(baseline, cramping, baseline_features, cramping_features, baseline_bursts, cramping_bursts):
    fig, axes = plt.subplots(4, 1, figsize=(14, 12))

    baseline_time = baseline['timestamp'].values / 1000
    cramping_time = cramping['timestamp'].values / 1000

    _, baseline_threshold = _get_threshold(baseline['rms'].values)
    _, cramping_threshold = _get_threshold(cramping['rms'].values)

    # Plot 1: Raw signal
    axes[0].plot(baseline_time, baseline['emg_voltage'], label='Baseline', alpha=0.7, linewidth=0.8)
    axes[0].plot(cramping_time, cramping['emg_voltage'], label='Cramping', alpha=0.7, linewidth=0.8)
    axes[0].set_ylabel('EMG Voltage (V)')
    axes[0].set_xlabel('Time (seconds)')
    axes[0].set_title('Raw MyoWare Signal Comparison')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot 2: RMS envelope with bursts
    axes[1].plot(baseline_time, baseline['rms'], label='Baseline RMS', alpha=0.7)
    axes[1].plot(cramping_time, cramping['rms'], label='Cramping RMS', alpha=0.7)
    axes[1].axhline(y=baseline_threshold, color='blue', linestyle='--',
                    label=f'Baseline threshold ({baseline_threshold:.2f}V)', alpha=0.5)
    axes[1].axhline(y=cramping_threshold, color='red', linestyle='--',
                    label=f'Cramping threshold ({cramping_threshold:.2f}V)', alpha=0.5)
    for burst in cramping_bursts[:10]:
        axes[1].axvspan(cramping_time[burst['start']], cramping_time[burst['end']],
                        alpha=0.2, color='red')
    axes[1].set_ylabel('RMS Voltage (V)')
    axes[1].set_xlabel('Time (seconds)')
    axes[1].set_title('RMS Envelope with Detected Bursts (red shaded = cramping bursts)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # Plot 3: Amplitude distribution
    axes[2].hist(baseline['emg_voltage'], bins=50, alpha=0.5, label='Baseline', density=True, color='blue')
    axes[2].hist(cramping['emg_voltage'], bins=50, alpha=0.5, label='Cramping', density=True, color='red')
    axes[2].axvline(baseline['emg_voltage'].mean(), color='blue', linestyle='--', linewidth=2,
                    label=f'Baseline mean ({baseline["emg_voltage"].mean():.2f}V)')
    axes[2].axvline(cramping['emg_voltage'].mean(), color='red', linestyle='--', linewidth=2,
                    label=f'Cramping mean ({cramping["emg_voltage"].mean():.2f}V)')
    axes[2].set_xlabel('EMG Voltage (V)')
    axes[2].set_ylabel('Probability Density')
    axes[2].set_title('EMG Amplitude Distribution')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    # Plot 4: Feature boxplot
    feature_data = []
    labels = []
    for feature in ['rms', 'mav', 'var', 'max_amp']:
        feature_data.append(baseline_features[feature])
        labels.append(f'Baseline\n{feature}')
        feature_data.append(cramping_features[feature])
        labels.append(f'Cramping\n{feature}')

    bp = axes[3].boxplot(feature_data, labels=labels, patch_artist=True)
    for i, patch in enumerate(bp['boxes']):
        patch.set_facecolor('lightblue' if i % 2 == 0 else 'lightcoral')
    axes[3].set_ylabel('Feature Value')
    axes[3].set_title('Feature Distribution Comparison')
    axes[3].grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to {PLOT_PATH}")
    plt.show()


def _get_threshold(emg_rms):
    from config import BURST_PERCENTILE
    baseline_portion = emg_rms[:int(len(emg_rms) * 0.2)]
    baseline_mean = np.mean(baseline_portion)
    baseline_std = np.std(baseline_portion)
    threshold = baseline_mean + (np.percentile(emg_rms, BURST_PERCENTILE) * baseline_std)
    return None, threshold