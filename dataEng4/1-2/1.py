import sqlite3
import csv
import json

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT,
    begin TEXT,
    system TEXT,
    tours_count INTEGER,
    min_rating REAL,
    time_on_game INTEGER
)
''')

conn.commit()

with open('item.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        cursor.execute('''
        INSERT INTO data (id, name, city, begin, system, tours_count, min_rating, time_on_game)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['id'], row['name'], row['city'], row['begin'], row['system'], row['tours_count'], row['min_rating'], row['time_on_game']))

conn.commit()

# вывод первых 39 отсортированных по произвольному числовому полю строк из таблицы в файл формата json;
cursor.execute('SELECT * FROM data ORDER BY time_on_game LIMIT 39')
rows = cursor.fetchall()
print(rows)
column_names = [description[0] for description in cursor.description]

json_data = json.dumps([dict(zip(column_names, row)) for row in rows], indent=4, ensure_ascii=False)

with open('output11.json', 'w', encoding='utf-8') as file:
    file.write(json_data)

# вывод (сумму, мин, макс, среднее) по произвольному числовому полю;
cursor.execute('SELECT SUM(time_on_game), MIN(time_on_game), MAX(time_on_game), AVG(time_on_game) FROM data')
result = cursor.fetchone()

print(f"Sum: {result[0]}, Min: {result[1]}, Max: {result[2]}, Avg: {result[3]}")

# вывод частоты встречаемости для категориального поля;
cursor.execute('SELECT system, COUNT(*) FROM data GROUP BY system')
rows = cursor.fetchall()

for row in rows:
    print(f"Category: {row[0]}, Count: {row[1]}")

# Вывод первых 39 отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json
cursor.execute('SELECT * FROM data WHERE system="Olympic" ORDER BY time_on_game LIMIT 39')
rows = cursor.fetchall()

column_names = [description[0] for description in cursor.description]
json_data = json.dumps([dict(zip(column_names, row)) for row in rows], indent=4, ensure_ascii=False)
with open('output14.json', 'w', encoding='utf-8') as file:
    file.write(json_data)

conn.close()