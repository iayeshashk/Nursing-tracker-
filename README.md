# Nursing Shift & Patient Care Tracker

A highly portable, "drag-and-drop" Nursing Care Tracker built with Python, Flask, and Bootstrap 5. Data is persisted locally in a pure `data.json` file—no Docker or SQL required!

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to:
   [http://localhost:5000](http://localhost:5000)

## Features
- **JSON Database**: Zero-configuration data storage via `data.json`.
- **Patient Roster**: Easily admit patients and track their room and condition.
- **Dynamic Status**: Automatically calculates if a patient is 'Stable', 'Checkup Due' (within 1 hour), or 'Overdue' based on their custom care interval.
- **Responsive UI**: Clean and calm UI built with Bootstrap 5.
