import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_url TEXT NOT NULL,
            short_url TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at INTEGER DEFAULT strftime("%s")
        )
    ''')
    conn.commit()
    conn.close()

def add_url(source_url, short_url, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO urls (source_url, short_url, password) VALUES (?, ?, ?)',
              (source_url, short_url, password))
    conn.commit()
    conn.close()

def get_url(short_url):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT source_url FROM urls WHERE short_url = ?', (short_url,))
    url = c.fetchone()
    conn.close()
    return url[0] if url else None

def check_password(short_url, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT password FROM urls WHERE short_url = ?', (short_url,))
    stored_password = c.fetchone()
    conn.close()
    return stored_password[0] == password if stored_password else False

init_db()  # Initialize the database
