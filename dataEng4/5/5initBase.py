import sqlite3

conn = sqlite3.connect('5task.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    bookID INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    authors TEXT,
    average_rating REAL,
    isbn TEXT,
    isbn13 TEXT,
    language_code TEXT,  
    num_pages INTEGER,
    ratings_count INTEGER,
    text_reviews_count INTEGER,
    publication_date TEXT,
    publisher TEXT
)
''')
conn.commit()
cursor.execute('''
CREATE TABLE IF NOT EXISTS best_selling_books (
    Book TEXT,
    "Author(s)" TEXT,
    "Original language" TEXT,
    "First published" INTEGER,
    "Approximate sales in millions" REAL,
    Genre TEXT
)
''')

conn.commit()
conn.close()