from flask import Flask, request, redirect, render_template
import sqlite3
import random
import string

app = Flask(__name__)
DB = 'database.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.execute('CREATE TABLE IF NOT EXISTS urls (id TEXT PRIMARY KEY, url TEXT)')
    return conn

def generate_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    error = None
    if request.method == 'POST':
        original_url = request.form['url']
        if not original_url.startswith(('http://', 'https://')):
            error = "Please enter a valid URL starting with http:// or https://"
        else:
            short_id = generate_id()
            conn = get_db()
            conn.execute('INSERT INTO urls (id, url) VALUES (?, ?)', (short_id, original_url))
            conn.commit()
            conn.close()
            short_url = request.host_url + short_id
    return render_template('index.html', short_url=short_url, error=error)

@app.route('/<short_id>')
def redirect_short(short_id):
    conn = get_db()
    cur = conn.execute('SELECT url FROM urls WHERE id = ?', (short_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return redirect(row[0])
    else:
        return 'URL not found!', 404

if __name__ == '__main__':
    app.run(debug=True)
