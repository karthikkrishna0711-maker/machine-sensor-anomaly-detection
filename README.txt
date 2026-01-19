# Machine Sensor Anomaly Detection & Predictive Maintenance

This project focuses on monitoring machine health using multivariate sensor
data and predicting potential failures before they occur. It combines
unsupervised anomaly detection with supervised failure prediction and
Remaining Useful Life (RUL) estimation, and presents results through an
interactive dashboard.

The goal of the project is to understand how machines degrade over time and
to convert sensor behavior into actionable maintenance insights.

---

## Dataset

The project uses the NASA CMAPSS turbofan engine degradation dataset.  
It contains sensor readings collected over multiple operating cycles for
several engines until failure.

Each engine degrades gradually, making the dataset suitable for:
- anomaly detection
- failure risk prediction
- remaining life estimation

---

## Project Overview

The project is structured as a progression rather than isolated tasks.

### 1. Anomaly Detection (Unsupervised)

An unsupervised model is used to learn normal operating behavior from sensor
data and detect deviations without relying on failure labels.

This stage answers:
- Is the engine behaving abnormally?
- Are there early signs of degradation?

Isolation Forest is used to generate anomaly scores across operating cycles.

---

### 2. Failure Prediction (Supervised Classification)

A supervised classification model predicts whether an engine is likely to fail
within a defined future window.

This stage answers:
- Is failure likely soon?

The model prioritizes recall to avoid missed failures, since false negatives
are more costly than false alarms in maintenance scenarios.

---

### 3. Remaining Useful Life (RUL) Estimation (Regression)

A regression model estimates how many operating cycles remain before failure.

This stage answers:
- How much time is left before failure?

Window-based statistical features are used instead of raw sensor values to
capture degradation trends. Prediction uncertainty is higher early in an
engine’s life and decreases as failure approaches.

---

### 4. Unified Monitoring Dashboard

All outputs are integrated into a single Streamlit dashboard with multiple
views:
- anomaly detection
- failure prediction and RUL
- combined engine health view

This allows engine-wise inspection of degradation behavior, risk level, and
remaining lifetime.

---

## Feature Engineering

Raw sensor values are not used directly for prediction.

Instead, sliding windows are applied to sensor data and statistical features
(such as mean and standard deviation) are extracted. These features better
represent temporal behavior and degradation patterns, which are critical for
predictive maintenance tasks.

---

## Key Learnings

- Anomaly detection provides early warnings but does not indicate failure
  timing.
- Failure classification is more reliable than RUL estimation for safety-
  critical decisions.
- RUL prediction is inherently noisy due to non-linear degradation and
  engine-to-engine variability.
- Combining unsupervised and supervised models provides a more complete view
  of machine health than using either alone.

---

## Project Structure

machine-sensor-anomaly-detection/
│
├── app.py 
├── README.md 
├── .gitignore 
│
├── notebooks/ 
│ ├── anomaly_detection.ipynb
│ ├── failure_classification.ipynb
│ └── rul_regression.ipynb
│
├── data/
│ ├── raw/ 
│ └── processed/ 
│
├── results/
│ ├── anomaly_scores.csv
│ └── results_df.csv
│
└── venv/  (not tracked)


---

## How to Run

1. Create and activate a virtual environment
2. Install dependencies
3. Run the dashboard:


---

## Notes

This project was developed iteratively, starting from anomaly detection and
gradually extending to supervised prediction and system-level integration.
The focus was on understanding degradation behavior rather than optimizing
for perfect metrics.

Author
Karthik Krishna
