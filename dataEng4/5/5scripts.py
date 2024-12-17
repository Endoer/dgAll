import sqlite3
import json

# Подключение к базе данных SQLite
conn = sqlite3.connect('5task.db')
cursor = conn.cursor()


# Выборка с простым условием + сортировка + ограничение количества
cursor.execute('''
SELECT Book, "Author(s)"
FROM best_selling_books
WHERE Genre = 'Fiction'
ORDER BY "Approximate sales in millions" DESC
LIMIT 3
''')
result = cursor.fetchall()
print(json.dumps(result, indent=4))

# Подсчет объектов по условию
cursor.execute('''
SELECT COUNT(*)
FROM books
WHERE num_pages > 300
''')
result = cursor.fetchone()
print(json.dumps(result, indent=4))

# Группировка
cursor.execute('''
SELECT Genre, COUNT(*) AS count
FROM best_selling_books
GROUP BY Genre
''')
result = cursor.fetchall()
print(json.dumps(result, indent=4))

# Обновление данных
cursor.execute('''
UPDATE books
SET average_rating = average_rating * 1.1
WHERE authors = 'Jane Austen'
''')
conn.commit()

# Агрегация
cursor.execute('''
SELECT Genre, AVG("Approximate sales in millions") AS avg_sales
FROM best_selling_books
GROUP BY Genre
''')
result = cursor.fetchall()
print(json.dumps(result, indent=4))


# Закрытие соединения с базой данных
conn.close()
