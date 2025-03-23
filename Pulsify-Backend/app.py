from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import os
import openai
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a secure secret key

# Simulated provider database
valid_providers = [
    {"npi": "1457689023", "dea": "OB7432196", "first_name": "Olivia", "last_name": "Brooks", "ssn": "111-11-1111"},
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
patients = [
    {"id": 1, "first_name": "Alice", "last_name": "Anderson", "dob": "1985-01-15"},
    {"id": 2, "first_name": "Bob", "last_name": "Brown", "dob": "1990-02-20"},
    {"id": 3, "first_name": "Carol", "last_name": "Clark", "dob": "1978-03-10"},
    {"id": 4, "first_name": "David", "last_name": "Davis", "dob": "1965-04-05"},
    {"id": 5, "first_name": "Eva", "last_name": "Evans", "dob": "2000-05-25"},
    {"id": 6, "first_name": "Frank", "last_name": "Foster", "dob": "1982-06-30"},
    {"id": 7, "first_name": "Grace", "last_name": "Green", "dob": "1995-07-12"},
    {"id": 8, "first_name": "Henry", "last_name": "Hill", "dob": "1970-08-08"},
    {"id": 9, "first_name": "Ivy", "last_name": "Ingram", "dob": "1988-09-19"},
    {"id": 10, "first_name": "Jack", "last_name": "Johnson", "dob": "1992-10-03"}
]

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
    # If no patient_id is provided, redirect to the patient search page
    if not patient_id:
        flash("Patient ID is required.")
        return redirect(url_for('patient_search'))
    try:
        patient_id = int(patient_id)
    except ValueError: hi
        # If patient_id is not a valid integer, redirect to the patient search page
        flash("Invalid Patient ID.")
        return redirect(url_for('patient_search'))
    # Find the patient in the database
    patient = next((p for p in patients if p['id'] == patient_id), None)
    # If the patient is not found, redirect to the patient search page
    if not patient:
        flash("Patient not found.")
        return redirect(url_for('patient_search'))
    # Render the patient profile page with the patient data
    return render_template('patient_profile.html', patient=patient)

@app.route('/ask_llm', methods=['POST'])
def ask_llm():
    user_message = request.form.get('message')
    if not user_message:
        return jsonify({"response": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant helping a doctor analyze a patient."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
