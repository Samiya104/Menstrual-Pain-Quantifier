# Dysmenorrhea EMG Analysis

A low-cost abdominal EMG pipeline for detecting muscle activity patterns associated with menstrual cramping pain, built on the MyoWare 2.0 sensor and Arduino.

This project is inspired by [Oladosu et al. (2018)](https://doi.org/10.1016/j.ajog.2018.04.050), which demonstrated that abdominal skeletal muscle activity precedes spontaneous menstrual cramping pain in primary dysmenorrhea. We replicate and extend this methodology using consumer-grade hardware.

> **Note:** Raw data is not included in this repository as it contains identifiable physiological recordings. The results and plots from a sample session are included in `results/`.

---

## Project Overview

Dysmenorrhea (menstrual cramping pain) affects up to 50% of reproductive-aged women. Research suggests that involuntary abdominal muscle contractions — visceromotor reflexes (VMRs) — may precede and contribute to cramping pain. This project uses surface EMG to capture and analyze those muscle activity patterns.

**What this pipeline does:**
- Loads and preprocesses raw MyoWare EMG recordings (baseline vs. cramping sessions)
- Extracts signal features: RMS, MAV, variance, max amplitude
- Detects burst events (VMR-like activity)
- Compares baseline vs. cramping statistically
- Logs all metrics and artifacts to MLflow for experiment tracking

---

## Hardware Setup

**Materials:**
- Arduino Uno
- MyoWare 2.0 EMG Sensor + Arduino Shield
- MyoWare Cable Shield + Link Shield
- Surface electrodes
- USB-B cable
- 3.5mm audio connector
- Laptop (not connected to mains power during recording)

**Electrode placement (abdominal region):**

| Electrode | Color | Position |
|-----------|-------|----------|
| V+ | Red | 4–6 cm lateral, 2 cm above umbilicus (left) |
| V− | Blue | 4–6 cm lateral, 2 cm above umbilicus (right) |
| Reference | Black | 4 cm below V+, between umbilicus and pubic symphysis |

> ⚠️ **Important:** Disconnect the laptop from its power supply before collecting data to avoid electrical interference.

**Sensor settings:** Set the MyoWare filter to `RAW` mode for best signal quality.

For full step-by-step hardware and software setup, see [`docs/Standard_Operating_Procedure.md`](docs/Standard_Operating_Procedure.md).

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add your data

Place your MyoWare CSV recordings in the `data/myoware_data/` folder:

```
data/
└── myoware_data/
    ├── baseline_<name>_<date>.csv
    └── cramps_<name>_<date>.csv
```

Update file paths in `config.py` to match your filenames.

### 3. Run the analysis

```bash
python main.py
```

### 4. View MLflow dashboard

```bash
mlflow ui
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) to explore logged metrics, parameters, and plots across runs.

---

## Project Structure

```
Menstrual-Pain-Quantifier/
├── README.md
├── .gitignore
├── requirements.txt
├── config.py
├── main.py
├── firmware/
|   ├──CONFIG.md
│   └── myoware_data_collection.ino
├── data/
│   └── .gitkeep
├── results/
│   └── emg_cramp_analysis.png
├── src/
│   ├── preprocess.py
│   ├── features.py
│   ├── analysis.py
│   ├── visualize.py
│   └── mlflow_logging.py
├── notebooks/
│   └── cramp_analysis.ipynb
└── docs/
    ├── images/
    │   └── electrode_placement.png
    └── Standard_Operating_Procedure.md

```

---

## Reference

Oladosu, F. A., Tu, F. F., Farhan, S., Garrison, E. F., Steiner, N. D., Roth, G. E., & Hellman, K. M. (2018). Abdominal skeletal muscle activity precedes spontaneous menstrual cramping pain in primary dysmenorrhea. *American Journal of Obstetrics and Gynecology*, 219(1), 91.e1–91.e7. https://doi.org/10.1016/j.ajog.2018.04.050
