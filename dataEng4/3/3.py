import msgpack
import sqlite3
import json

with open("_part_1.msgpack", 'rb') as file:
    data = msgpack.unpackb(file.read(), raw=False)

# Вывод данных
print(data)

with open("_part_2.text", 'r', encoding='utf-8') as file:
    data2 = file.read()

records = data2.split('=====')
text_data_list = []
for record in records:
    record_dict = {}
    lines = record.strip().split('\n')
    print(lines)
    for line in lines:
        key, value = line.split('::')
        record_dict[key] = value
    text_data_list.append(record_dict)

# Общие ключи файлов
print(set(text_data_list[0].keys()).intersection(data[0].keys())) 

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS data (
    artist TEXT,
    genre TEXT,
    duration_ms INTEGER,
    song TEXT,
    year INTEGER,
    tempo REAL,
    instrumentalness REAL
)
''')

for row in data:
        cursor.execute('''
        INSERT INTO data (artist, genre, duration_ms, song, year, tempo, instrumentalness)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (row['artist'], row['genre'], row['duration_ms'], row['song'], row['year'], row['tempo'], row['instrumentalness']))

for row in text_data_list:
        cursor.execute('''
        INSERT INTO data (artist, genre, duration_ms, song, year, tempo, instrumentalness)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (row['artist'], row['genre'], row['duration_ms'], row['song'], row['year'], row['tempo'], row['instrumentalness']))

conn.commit()

# вывод первых 39 отсортированных по произвольному числовому полю строк из таблицы в файл формата json;
cursor.execute('SELECT * FROM data ORDER BY year LIMIT 39')
rows = cursor.fetchall()
print(rows)
column_names = [description[0] for description in cursor.description]

json_data = json.dumps([dict(zip(column_names, row)) for row in rows], indent=4, ensure_ascii=False)

with open('output31.json', 'w', encoding='utf-8') as file:
    file.write(json_data)

# вывод (сумму, мин, макс, среднее) по произвольному числовому полю;
cursor.execute('SELECT SUM(duration_ms), MIN(duration_ms), MAX(duration_ms), AVG(duration_ms) FROM data')
result = cursor.fetchone()

print(f"Sum: {result[0]}, Min: {result[1]}, Max: {result[2]}, Avg: {result[3]}")

# вывод частоты встречаемости для категориального поля;
cursor.execute('SELECT genre, COUNT(*) FROM data GROUP BY genre')
rows = cursor.fetchall()

for row in rows:
    print(f"Category: {row[0]}, Count: {row[1]}")

# Вывод первых 39 отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json
cursor.execute('SELECT * FROM data WHERE genre="rock" ORDER BY year LIMIT 39')
rows = cursor.fetchall()

column_names = [description[0] for description in cursor.description]
json_data = json.dumps([dict(zip(column_names, row)) for row in rows], indent=4, ensure_ascii=False)
with open('output34.json', 'w', encoding='utf-8') as file:
    file.write(json_data)

conn.close()