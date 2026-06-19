import os
import json
import uuid
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"patients": [], "care_logs": []}
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            # Ensure new keys exist if migrating from old version
            if "patients" not in data:
                data["patients"] = []
            if "care_logs" not in data:
                data["care_logs"] = []
            return data
    except (json.JSONDecodeError, IOError):
        return {"patients": [], "care_logs": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def calculate_status(patient_id):
    data = load_data()
    
    # Find the patient
    patient = next((p for p in data.get("patients", []) if p.get("id") == patient_id), None)
    if not patient:
        return "Unknown"
        
    # Get all logs for this patient
    logs = [log for log in data.get("care_logs", []) if log.get("patient_id") == patient_id]
    
    if not logs:
        return "No Logs"
        
    # Sort logs by timestamp descending
    logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    recent_log = logs[0]
    
    try:
        # Expected format: ISO 8601 string like "2026-06-13T10:30"
        last_check = datetime.fromisoformat(recent_log.get("timestamp"))
    except ValueError:
        return "Invalid Date"
        
    interval_hours = float(patient.get("care_interval_hours", 0))
    deadline = last_check + timedelta(hours=interval_hours)
    now = datetime.now()
    
    if now > deadline:
        return "Overdue"
    elif (deadline - now).total_seconds() <= 3600: # 1 hour
        return "Checkup Due"
    else:
        return "Stable"

@app.route('/')
def dashboard():
    data = load_data()
    patient_list = data.get("patients", [])
    
    # Inject dynamic status
    for p in patient_list:
        p['status'] = calculate_status(p['id'])
        
    return render_template('dashboard.html', patients=patient_list)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.form.get('name')
    room_number = request.form.get('room_number')
    condition = request.form.get('condition')
    care_interval_hours = request.form.get('care_interval_hours')
    
    if not all([name, room_number, condition, care_interval_hours]):
        return "Missing fields", 400
        
    data = load_data()
    new_patient = {
        "id": str(uuid.uuid4()),
        "name": name,
        "room_number": room_number,
        "condition": condition,
        "care_interval_hours": float(care_interval_hours)
    }
    
    data.setdefault("patients", []).append(new_patient)
    save_data(data)
    
    return redirect(url_for('dashboard'))

@app.route('/add_care_log', methods=['POST'])
def add_care_log():
    patient_id = request.form.get('patient_id')
    action_taken = request.form.get('action_taken')
    notes = request.form.get('notes')
    timestamp = request.form.get('timestamp') # Comes from datetime-local input, e.g., "2026-06-13T10:30"
    
    if not all([patient_id, action_taken, timestamp]):
        return "Missing fields", 400
        
    data = load_data()
    new_log = {
        "id": str(uuid.uuid4()),
        "patient_id": patient_id,
        "timestamp": timestamp,
        "action_taken": action_taken,
        "notes": notes or ""
    }
    
    data.setdefault("care_logs", []).append(new_log)
    save_data(data)
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
