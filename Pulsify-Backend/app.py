from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)  # ✅ This is the correct way

# Root route that redirects to /signup
@app.route('/')
def index():
    return redirect(url_for('signup'))

# In-memory user store
users = []

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users.append({'username': username, 'password': password})
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)