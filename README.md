# Digital Procrastination Detector

A Python-based productivity monitoring system that tracks computer activity and classifies it into **Productive, Neutral, or Distracting** activities.

## Features

* Real-time computer activity tracking
* Automatic activity classification
* Productivity monitoring
* Procrastination detection
* Daily productivity report
* Activity database storage
* Flask-based dashboard
* Productivity and distraction statistics

## Technologies Used

* Python
* Flask
* SQLite
* HTML
* CSS
* JavaScript
* PyGetWindow
* Activity Classification

## Project Structure

```text
Digital-Procrastination-Detector/
│
├── activity_tracker.py
│
├── detection/
│   ├── DASHBOARD.PY
│   ├── activity_classifier.py
│   └── database/
│       └── activity_database.py
│
├── .gitignore
└── README.md
```

## How It Works

The system monitors the currently active application or browser window and records the user's activity.

Activities are classified into three categories:

* **PRODUCTIVE** — activities related to useful work or study
* **NEUTRAL** — activities that are neither strongly productive nor distracting
* **DISTRACTING** — activities that may contribute to procrastination

The collected activity data is stored and displayed through the productivity dashboard.

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/sreelekshmi-001/Digital-Procrastination-Detector.git
```

### 2. Open the project

```bash
cd Digital-Procrastination-Detector
```

### 3. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install flask pygetwindow
```

### 5. Start the activity tracker

```bash
python activity_tracker.py
```

### 6. Start the dashboard

```bash
python detection/DASHBOARD.PY
```

Then open:

```text
http://127.0.0.1:5000
```

## Project Goal

The goal of this project is to help users understand their digital habits, identify distracting activities, and improve their daily productivity.

## Author

**Sreelekshmi**
