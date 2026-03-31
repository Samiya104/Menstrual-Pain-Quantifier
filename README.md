# EMG-Based Menstrual Cramp Detection System

A wearable EMG acquisition and analysis system for detecting and characterizing abdominal muscle activity associated with menstrual cramping pain in primary dysmenorrhea.

---

## Table of Contents

- [Overview](#overview)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Hardware Setup](#hardware-setup)
- [Software Setup](#software-setup)
- [Running the Analysis](#running-the-analysis)
- [Output Files](#output-files)
- [Use Cases](#use-cases)
- [Project Structure](#project-structure)
- [Safety Notice](#safety-notice)

---

## Overview

This system uses a MyoWare EMG sensor paired with an Arduino Uno to record abdominal muscle activity during menstrual cramping. Signals are logged via PuTTY and analyzed using a custom Python pipeline that performs:

- Signal preprocessing and RMS envelope extraction
- Feature extraction (RMS, MAV, variance, max amplitude)
- Adaptive burst detection for visceromotor reflex (VMR)-like events
- Statistical comparison between baseline and cramping recordings
- Visualization and CSV report export

---

## Hardware Requirements

| Component | Details |
|---|---|
| Arduino Uno | Microcontroller for data acquisition |
| MyoWare EMG Sensor | Surface EMG signal acquisition |
| MyoWare Arduino Shield | Interfaces sensor with Arduino |
| MyoWare Cable Shield | Cable connection support |
| MyoWare Link Shield | Electrode cable connection |
| Surface EMG Electrodes | Disposable, standard |
| 3.5mm Audio Connector | Sensor to cable shield connection |
| USB-B Cable | Arduino to laptop connection |
| Laptop | Data logging — must be unplugged from power during recording |

---

## Software Requirements

```
Python 3.x
pandas
numpy
scipy
matplotlib
```

Install dependencies:

```bash
pip install pandas numpy scipy matplotlib
```

Additional software:

- **Arduino IDE** — for flashing acquisition code to the Arduino
- **PuTTY** — for serial data logging to CSV

---

## Hardware Setup

> ⚠️ **SAFETY: Disconnect the laptop from all power outlets before collecting data.**

1. Connect the Arduino Uno and the MyoWare Arduino Shield.
2. Connect the sensor, link shield, and cable shield.
3. Connect one end of the 3.5mm audio cable to the sensor and the other to the Arduino cable shield. Note which analog pin is used.
4. Connect the electrode cable to the link shield.
5. Place electrodes on the abdominal region:
   - **Red (V+):** 4–6 cm lateral, 2 cm above umbilicus (left side)
   - **Blue (V−):** 4–6 cm lateral, 2 cm above umbilicus (right side)
   - **Black (Ref):** 4 cm below V+, between umbilicus and pubic symphysis
6. Turn the sensor on.
7. Select the correct filter mode on the sensor (**RAW recommended**).
8. Connect Arduino to laptop and flash acquisition code.

---

## Software Setup

1. Open **Arduino IDE** and update the analog pin number in the code to match your hardware setup.
2. Open **PuTTY** and select **Serial** as the connection type.
3. Match the COM port and baud rate to the values in your Arduino code.
4. Navigate to **Logging** and select **All session output**.
5. Set the log file name and location. **Ensure the filename ends in `.csv`**.
6. Open the connection only after both hardware and software are fully configured.

---

## Running the Analysis

1. Place your recorded CSV files in the `myoware_data/` directory:
   - `baseline_samiya_myoware_03_16_1833.csv` — resting/non-cramping session
   - `cramps_samiya_03_19_1537.csv` — cramping session

2. Run the analysis script:

```bash
python cramp_analysis.py
```

3. The script will print a full statistical summary to the console and save outputs automatically.

---

## Output Files

| File | Description |
|---|---|
| `emg_cramp_analysis.png` | Multi-panel visualization of signals, RMS envelopes, distributions, and feature comparisons |
| `myoware_results/emg_analysis_results.csv` | Summary metrics including mean RMS, burst counts, and burst rate |

---

## Use Cases

**1. Closed-Loop Pain Management Device**
EMG-derived cramp severity scores can be used to automatically adjust the output of a connected heating pad or TENS unit — delivering proportional heat or electrical stimulation without requiring the user to manually adjust settings during a painful episode.

**2. Patient Cycle Tracking Dashboard**
Aggregated multi-session data can be presented in a longitudinal dashboard showing burst frequency, intensity, and RMS trends across menstrual cycles. This provides clinicians with objective physiological data to complement self-reported pain diaries and support more informed treatment decisions.

---

## Project Structure

```
emg-cramp-detection/
│
├── myoware_data/
│   ├── baseline_samiya_myoware_03_16_1833.csv
│   └── cramps_samiya_03_19_1537.csv
│
├── myoware_results/
│   └── emg_analysis_results.csv
│
├── cramp_analysis.py
├── emg_cramp_analysis.png
└── README.md
```

---

## Safety Notice

- **Always disconnect the laptop from its power outlet before attaching electrodes or collecting data.**
- Do not use this system on broken or irritated skin.
- This system is intended for research and proof-of-concept purposes only. It is not a certified medical device.
