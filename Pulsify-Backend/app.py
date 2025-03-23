from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production

# Simulated database of valid healthcare providers (10 fake doctor records)
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

# In-memory registered users list (for providers)
users = []

# Simulated patient data (10 patients)
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

# --------------------------
# Provider Routes: Signup, Login, Dashboard, Logout
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
        
        # Validate that the provider exists with matching first name, last name, NPI, and SSN
        matched_provider = next(
            (p for p in valid_providers if p['npi'] == npi_number and 
             p['first_name'].lower() == first_name_input.lower() and
             p['last_name'].lower() == last_name_input.lower() and
             p['ssn'] == ssn),
            None
        )

        if not matched_provider:
            return "Invalid credentials. Please check your first name, last name, NPI, and Social Security number."

        # Save the provider's chosen login credentials along with provider details
        users.append({
            'username': username,
            'password': password,
            'npi': npi_number,
            'ssn': ssn,
            'first_name': matched_provider['first_name'],
            'last_name': matched_provider['last_name']
        })

        # Redirect to the login page so the provider must verify their credentials
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid login credentials. Please try again."
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', users=users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signup'))

# --------------------------
# Patient Search and Chart Routes
# --------------------------

# Patient search: doctor searches by Date of Birth (DOB)
@app.route('/patient_search', methods=['GET', 'POST'])
def patient_search():
    if request.method == 'POST':
        dob = request.form.get('dob')
        # Filter patients by DOB (exact match for simplicity)
        matching_patients = [p for p in patients if p['dob'] == dob]
        # Render the search page with a dropdown of matching patients
        return render_template('patient_search.html', patients=matching_patients)
    # On GET, no patients are displayed until a search is made
    return render_template('patient_search.html', patients=None)

# Patient chart: display detailed patient information
@app.route('/patient_chart', methods=['GET'])
def patient_chart():
    patient_id = request.args.get('patient_id')
    if not patient_id:
        return "No patient selected", 400
    try:
        patient_id = int(patient_id)
    except ValueError:
        return "Invalid patient id", 400
    patient = next((p for p in patients if p['id'] == patient_id), None)
    if not patient:
        return "Patient not found", 404
    return render_template('patient_chart.html', patient=patient)

if __name__ == '__main__':
    app.run(debug=True)