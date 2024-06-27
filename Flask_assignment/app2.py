from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from transformers import pipeline
import os
import secrets
import string

def generate_secret_key(length=24):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Generate a secure random key
secure_key = generate_secret_key()

app = Flask(__name__)
app.secret_key = secure_key  # Change this to a secure random key in production

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Omer Khalid/Desktop/Flask_assignment/Users.db'
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Hard-coded username and password for testing
HARDCODED_USERNAME = 'admin'
HARDCODED_PASSWORD = 'password'

pipe = pipeline("summarization", model="pszemraj/long-t5-tglobal-base-16384-book-summary")

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hard-coded credentials check
        if username == HARDCODED_USERNAME and password == HARDCODED_PASSWORD:
            session['username'] = username
            return redirect(url_for('index'))
        
        return render_template('login.html', message='Invalid username or password')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username already exists (not necessary for hard-coded login)
        if username == HARDCODED_USERNAME:
            return render_template('signup.html', message='Username already exists')
        
        # Create a new user (not necessary for hard-coded login)
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        session['username'] = username
        return redirect(url_for('index'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        pubmed_text = request.form['pubmed_text']

        # Use the translation pipeline for summarization
        summarized_text = pipe(pubmed_text)[0]['summarization']

        return render_template('summary.html', original_text=pubmed_text, summarized_text=summarized_text)
    
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Create database tables within the application context
    with app.app_context():
        db.create_all()  # Create all tables defined by models
        print("Database tables created")
    
    # Directly redirect to the index and summarize routes
    app.run(debug=True, port=5000, host='0.0.0.0', threaded=True)
