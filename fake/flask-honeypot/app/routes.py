from flask import Blueprint, render_template, request, redirect, url_for

# Create a Blueprint for the app
app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def home():
    return render_template('index.html')

@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        username = request.form['username']
        password = request.form['password']
        # For honeypot purposes, we can log the credentials
        print(f"Username: {username}, Password: {password}")
        return redirect(url_for('app_routes.home'))
    return render_template('login.html')

@app_routes.route('/about')
def about():
    return render_template('about.html')