import sqlite3

conn = sqlite3.connect('issued_books.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS issued_books(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          author TEXT NOT NULL,
          genre TEXT,
          isbn TEXT UNIQUE,
          year INTEGER)
          ''')
conn.commit()
conn.close()