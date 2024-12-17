import pickle
import sqlite3


conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS priseData (
    name TEXT,
    place INTEGER,
    prise INTEGER
)
''')

conn.commit()

with open('subitem.pkl', 'rb') as file:
    data = pickle.load(file)

for row in data:
        cursor.execute('''
        INSERT INTO priseData (name, place, prise)
        VALUES (?, ?, ?)
        ''', (row['name'], row['place'], row['prise']))

# Первая таблица описывает даты, формат и местопроведение шахматных турниров, а вторая призовые за определённое место на них

# 1 
cursor.execute('''
SELECT
    d.system,
    AVG(p.prise) AS average_prise
FROM
    data d
JOIN
    priseData p ON d.name = p.name
WHERE
    p.place = 1
GROUP BY
    d.system;
''')

results_1 = cursor.fetchall()
print("Cредние призовые за первое вместо в зависимости от формата турнира:")
for row in results_1:
    print(row)

# 2
cursor.execute('''
SELECT
    d.min_rating
FROM
    data d
JOIN
    priseData p ON d.name = p.name
WHERE
    p.prise = (SELECT MAX(prise) FROM priseData);
''')

results_2 = cursor.fetchall()
print("Минимальный рейтинг турнира с максимальным призом:")
for row in results_2:
    print(row)

# 3
cursor.execute('''
SELECT
    SUM(p.prise) AS total_prise
FROM
    data d
JOIN
    priseData p ON d.name = p.name
WHERE
    d.time_on_game > 160;
''')

# 3
results_3 = cursor.fetchall()
print("Общие призовые турниров с продолжительностью более 160 минут:")
for row in results_3:
    print(row)

conn.close()
