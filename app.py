from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import uuid

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('dera.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS letters (
                    id INTEGER PRIMARY KEY,
                    token TEXT UNIQUE,
                    content TEXT,
                    viewed INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

@app.route('/generate', methods=['POST'])
def generate():
    content = request.form['content']
    token = str(uuid.uuid4())
    conn = sqlite3.connect('dera.db')
    c = conn.cursor()
    c.execute('INSERT INTO letters (token, content) VALUES (?, ?)', (token, content))
    conn.commit()
    conn.close()
    unique_link = url_for('letter', token=token, _external=True)
    return render_template('generate.html', link=unique_link)

@app.route('/letter/<token>')
def letter(token):
    conn = sqlite3.connect('dera.db')
    c = conn.cursor()
    c.execute('SELECT content, viewed FROM letters WHERE token = ?', (token,))
    result = c.fetchone()
    conn.close()

    if not result:
        return render_template('404.html')
    content, viewed = result
    if viewed:
        return render_template('404.html')

    # Mark the letter as viewed
    conn = sqlite3.connect('dera.db')
    c = conn.cursor()
    c.execute('UPDATE letters SET viewed = 1 WHERE token = ?', (token,))
    conn.commit()
    conn.close()
    
    return render_template('letter.html', content=content)

@app.route('/')
def home():
    return render_template('dera.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

