from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')

# Supabase-Setup
supabase: Client = create_client(supabase_url, supabase_key)

# Flask-Setup
app = Flask(__name__)


@app.route('/')
def home():
    user = supabase.auth.get_session()
    logged_in = 'eingeloggt' if user else 'nicht eingeloggt'
    return render_template('index.html', logged_in=logged_in)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            supabase.auth.sign_in_with_password({"email": email, "password": password})
            return redirect(url_for('home'))
        except Exception as e:
            return redirect(url_for('login', error=e))
    # if user is already logged in, redirect to home
    if supabase.auth.get_session():
        return redirect(url_for('home'))
    # if there is an error, display it
    if request.args.get('error'):
        return render_template('login.html', error=request.args.get('error'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    supabase.auth.sign_out()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
