from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import os
import openai
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random
from twilio.rest import Client

@app.route('/alert_emergency', methods=['POST'])
def alert_emergency():
    # ... existing logic ...
    
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM")
    to_number = os.getenv("TWILIO_TO")

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"🚨 Emergency Alert for patient {patient['first_name']} {patient['last_name']}.",
            from_=from_number,
            to=to_number
        )
        print(f"SMS sent: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a secure secret key

# Simulated provider database
valid_providers = [
    {"npi": "1457689023", "dea": "OB7432196", "first_name": "Victor", "last_name": "Izekor", "ssn": "111-11-1111"},
    {"npi": "1674938201", "dea": "MC9283745", "first_name": "Marcus", "last_name": "Chen", "ssn": "222-22-2222"},
    {"npi": "1092837410", "dea": "AR5739204", "first_name": "Amanda", "last_name": "Reyes", "ssn": "333-33-3333"},
    {"npi": "1782394563", "dea": "HP3489271", "first_name": "Henry", "last_name": "Patel", "ssn": "444-44-4444"},
    {"npi": "1328495076", "dea": "SO8247105", "first_name": "Samantha", "last_name": "O’Neil", "ssn": "555-55-5555"},
    {"npi": "1902837465", "dea": "EG9073416", "first_name": "Elijah", "last_name": "Grant", "ssn": "666-66-6666"},
    {"npi": "1439765018", "dea": "NF6271389", "first_name": "Naomi", "last_name": "Fisher", "ssn": "777-77-7777"},
    {"npi": "1567823490", "dea": "JM1948372", "first_name": "Jordan", "last_name": "Matthews", "ssn": "888-88-8888"},
    {"npi": "1213987456", "dea": "SM8573920", "first_name": "Sofia", "last_name": "Moreno", "ssn": "999-99-9999"},
    {"npi": "1749052387", "dea": "DO6428917", "first_name": "David", "last_name": "Okafor", "ssn": "000-00-0000"}
]

users = []  # Registered provider accounts

# Simulated patient data
patients = [
    {"id": 1, "first_name": "Oliva", "last_name": "Brooks", "dob": "2002-03-23", "email": "brook@gmail.com", "sex": "Male", "age": 21, "status": "Active", "department": "Cardiology", "joined_date": "March 23rd, 2023"},
    {"id": 2, "first_name": "Alice", "last_name": "Anderson", "dob": "1985-01-15", "email": "alice@example.com", "sex": "Female", "age": 38, "status": "Active", "department": "Cardiology", "joined_date": "2023-01-20"},
    {"id": 3, "first_name": "Bob", "last_name": "Brown", "dob": "1990-02-20", "email": "bob@example.com", "sex": "Male", "age": 33, "status": "Active", "department": "Cardiology", "joined_date": "2023-02-15"},
]

# Simulated patient profiles with vitals, medical conditions, allergies, and interacting drugs
patient_profiles = [
    {
        "patient_id": 1,
        "vitals": {
            "blood_pressure": {"value": "120/89", "unit": "mmHg"},
            "heart_rate": {"value": 120, "unit": "bpm"},
            "glucose": {"value": 95, "unit": "mg/dL"},
            "oxygen_saturation": {"value": 98, "unit": "%"},
            "temperature": {"value": 99.1, "unit": "°F"}
        },
        "medical_history": [
            {"medication": "Med A", "time": "Jan 21, 2023 - 09:00 AM", "status": "Cured"},
            {"medication": "Med B", "time": "Jan 22, 2023 - 10:30 AM", "status": "Ongoing"},
            {"medication": "Med C", "time": "Jan 25, 2023 - 01:00 PM", "status": "Critical"}
        ]
    },
    {
        "patient_id": 2,
        "vitals": {
            "blood_pressure": {"value": "130/85", "unit": "mmHg"},
            "heart_rate": {"value": 82, "unit": "bpm"},
            "glucose": {"value": 100, "unit": "mg/dL"},
            "oxygen_saturation": {"value": 96, "unit": "%"},
            "temperature": {"value": 98.6, "unit": "°F"}
        },
        "medical_history": [
            {"medication": "Med D", "time": "Feb 10, 2023 - 11:00 AM", "status": "Cured"},
            {"medication": "Med E", "time": "Feb 15, 2023 - 02:00 PM", "status": "Ongoing"}
        ]
    }
]

# --------------------------
# Routes
# --------------------------

@app.route('/')
def index():
    return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        npi_number = request.form.get('npi_number')
        ssn = request.form.get('ssn')
        first_name_input = request.form.get('first_name')
        last_name_input = request.form.get('last_name')
        username = request.form.get('username')
        password = request.form.get('password')

        matched_provider = next(
            (p for p in valid_providers if p['npi'] == npi_number and
             p['first_name'].lower() == first_name_input.lower() and
             p['last_name'].lower() == last_name_input.lower() and
             p['ssn'] == ssn),
            None
        )

        if not matched_provider:
            flash("Invalid credentials.")
            return redirect(url_for('signup'))

        users.append({
            'username': username,
            'password': generate_password_hash(password),
            'npi': npi_number,
            'ssn': ssn,
            'first_name': matched_provider['first_name'],
            'last_name': matched_provider['last_name']
        })
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = next((u for u in users if u['username'] == username and check_password_hash(u['password'], password)), None)
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        flash("Invalid login credentials.")
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash("Please log in to access the dashboard.")
        return redirect(url_for('login'))
    return render_template('dashboard.html', users=users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signup'))

@app.route('/patient_search', methods=['GET', 'POST'])
def patient_search():
    if request.method == 'POST':
        dob = request.form.get('dob')
        last_name = request.form.get('last_name')
        matches = [p for p in patients if p['dob'] == dob and p['last_name'].lower() == last_name.lower()]
        return render_template('patient_search.html', patients=matches)
    return render_template('patient_search.html', patients=None)

@app.route('/patient_profile')
def patient_profile():
    patient_id = request.args.get('patient_id')
    if not patient_id:
        flash("Patient ID is required.")
        return redirect(url_for('patient_search'))
    try:
        patient_id = int(patient_id)
    except ValueError:
        flash("Invalid Patient ID.")
        return redirect(url_for('patient_search'))
    patient = next((p for p in patients if p['id'] == patient_id), None)
    if not patient:
        flash("Patient not found.")
        return redirect(url_for('patient_search'))
    profile = next((p for p in patient_profiles if p['patient_id'] == patient_id), None)
    return jsonify({"patient": patient, "profile": profile})

@app.route('/ask_llm', methods=['GET', 'POST'])
def ask_llm():
    if request.method == 'POST':
        user_message = request.form.get('message')
        if not user_message:
            flash("No message provided.")
            return redirect(url_for('ask_llm'))

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful medical assistant helping a doctor analyze a patient."},
                    {"role": "user", "content": user_message}
                ]
            )
            reply = response['choices'][0]['message']['content']
            return render_template('llm_response.html', message=user_message, reply=reply)
        except Exception as e:
            flash(f"Error: {str(e)}")
            return redirect(url_for('ask_llm'))

    return render_template('ask_llm.html')

@app.route('/alert_emergency', methods=['POST'])
def alert_emergency():
    # ... existing logic ...
    
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM")
    to_number = os.getenv("TWILIO_TO")

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"🚨 Emergency Alert for patient {patient['first_name']} {patient['last_name']}.",
            from_=from_number,
            to=to_number
        )
        print(f"SMS sent: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")
if __name__ == '__main__':
    app.run(debug=True)
