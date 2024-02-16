from flask import Flask, render_template, request, redirect, url_for, session, jsonify
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
app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/')
def home():
    user_session = supabase.auth.get_session()
    logged_in = True if user_session else False
    if logged_in:
        try:
            user = supabase.table('users').select('*').eq('id', user_session.user.id).execute()
            if user.data:
                return render_template('index.html', username=user.data[0]['name'], logged_in=logged_in)
        except Exception as e:
            return render_template('index.html', error=e, logged_in=logged_in)

    return render_template('index.html', logged_in=logged_in)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = supabase.table('users').select('*').eq('email', email).execute()
            if not user.data:
                try:
                    supabase.auth.sign_up({"email": email, "password": password})
                    return redirect(url_for('verify'))
                except Exception as e:
                    return render_template('login.html', error=e)
            else:
                try:
                    supabase.auth.sign_in_with_password({"email": email, "password": password})
                    if user.data[0]['name']:
                        return redirect(url_for('home'))
                    else:
                        return redirect(url_for('onboard'))
                except Exception as e:
                    return render_template('login.html', error=e)
        except Exception as e:
            return render_template('login.html', error=e)
    if supabase.auth.get_session():
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    supabase.auth.sign_out()
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/verify')
def verify():
    return render_template('verify.html')


@app.route('/onboard')
def onboard():
    return render_template('onboard.html')


if __name__ == '__main__':
    app.run(debug=True)
