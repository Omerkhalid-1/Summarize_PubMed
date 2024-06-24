from flask import Flask, render_template, request, redirect, url_for, session
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure random key in production

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("Falconsai/text_summarization")
model = AutoModelForSeq2SeqLM.from_pretrained("Falconsai/text_summarization")

# Mock user database (you should use a database like SQLAlchemy in production)
users = {
    'user1': {
        'username': 'Omer',
        'password': '1234'
    },
    'user2': {
        'username': 'Maham',
        'password': '1234'
    }
}

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('signup.html', message='Username already exists')
        users[username] = {'username': username, 'password': password}
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'username' in session:
        if request.method == 'POST':
            pubmed_text = request.form['pubmed_text']

            # Tokenize input text
            inputs = tokenizer.encode("summarize: " + pubmed_text, return_tensors="pt", max_length=1024, truncation=True)

            # Generate summary
            summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
            summarized_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

            return render_template('summary.html', original_text=pubmed_text, summarized_text=summarized_text)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
