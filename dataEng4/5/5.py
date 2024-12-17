import sqlite3
import csv
import json

conn = sqlite3.connect('5task.db')
cursor = conn.cursor()

with open('books.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
        cursor.execute('''
        INSERT INTO books (bookID,title,authors,average_rating,isbn,isbn13,language_code,  num_pages,ratings_count,text_reviews_count,publication_date,publisher)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (  int(row['bookID']),
                row['title'],
                row['authors'], 
                row['average_rating'],  
                row['isbn'],
                row['isbn13'],
                row['language_code'],
                row['num_pages'],
                int(row['ratings_count']),   
                int(row['text_reviews_count']),
                row['publication_date'],
                row['publisher']))
        
with open('best-selling-books.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for row in data:
    print(row)
    cursor.execute('''
    INSERT INTO best_selling_books (Book, "Author(s)", "Original language", "First published", "Approximate sales in millions", Genre)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (row['Book'], row['Author(s)'], row['Original language'], int(row['First published']), float(row['Approximate sales in millions']), row['Genre']))


conn.commit()
conn.close()

