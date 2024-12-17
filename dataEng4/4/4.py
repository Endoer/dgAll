import sqlite3
import csv
import json

# Подключение к базе данных SQLite
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# Создание таблицы для хранения информации о товарах
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    quantity INTEGER,
    category TEXT,
    fromCity TEXT,
    isAvailable BOOLEAN,
    views INTEGER,
    update_count INTEGER DEFAULT 0
)
''')

# Сохранение изменений
conn.commit()

# Чтение данных из CSV файла и запись их в таблицу
with open('_product_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        cursor.execute('''
        INSERT INTO products (name, price, quantity, category, fromCity, isAvailable, views)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (row['name'], float(row['price']), int(row['quantity']), row['category'], row['fromCity'], row['isAvailable'] == 'True', (row['views'])))

# Сохранение изменений
conn.commit()

# Чтение данных из JSON файла
with open('_update_data.json', 'r', encoding='utf-8') as file:
    changes = json.load(file)

uniq_method = set(change['method'] for change in changes)
print(uniq_method)
# Применение изменений с использованием транзакций
for change in changes:
    name = change['name']
    method = change['method']
    param = change['param']

    cursor.execute('BEGIN TRANSACTION')

    if method == 'price_abs':
        new_price = float(param)
        cursor.execute('''
        UPDATE products
        SET price = ? + price, update_count = update_count + 1
        WHERE name = ? AND ? >= 0
        ''', (new_price, name, new_price))
    elif method == 'price_percent':
        percent_change = float(param)
        cursor.execute('''
        UPDATE products
        SET price = price - ? , update_count = update_count + 1
        WHERE name = ? AND price - ? >= 0
        ''', (percent_change, name, percent_change))
        # Я честно не понял что вы автор хотел сказать этими методами и сделал просто + и -
    elif method == 'quantity_add':
        add_quantity = int(param)
        cursor.execute('''
        UPDATE products
        SET quantity = quantity + ?, update_count = update_count + 1
        WHERE name = ? AND quantity + ? >= 0
        ''', (add_quantity, name, add_quantity))
    elif method == 'quantity_sub':
        sub_quantity = int(param)
        cursor.execute('''
        UPDATE products
        SET quantity = quantity - ?, update_count = update_count + 1
        WHERE name = ? AND quantity - ? >= 0
        ''', (sub_quantity, name, sub_quantity))
    elif method == 'available':
        cursor.execute('''
        UPDATE products
        SET isAvailable = NOT isAvailable, update_count = update_count + 1
        WHERE name = ?
        ''', (name,))
    elif method == 'remove':
        cursor.execute('''
        DELETE FROM products
        WHERE name = ?
        ''', (name,))

    conn.commit()

# Вывести топ-10 самых обновляемых товаров
cursor.execute('''
SELECT name, update_count
FROM products
ORDER BY update_count DESC
LIMIT 10
''')
top_10_updated = cursor.fetchall()
print("Top 10 most updated products:", top_10_updated)

# Анализ цен товаров
cursor.execute('''
SELECT category, SUM(price) AS total_price, MIN(price) AS min_price, MAX(price) AS max_price, AVG(price) AS avg_price, COUNT(*) AS count
FROM products
GROUP BY category
''')
price_analysis = cursor.fetchall()
print("Price analysis by category:", price_analysis)

# Анализ остатков товаров
cursor.execute('''
SELECT category, SUM(quantity) AS total_quantity, MIN(quantity) AS min_quantity, MAX(quantity) AS max_quantity, AVG(quantity) AS avg_quantity, COUNT(*) AS count
FROM products
GROUP BY category
''')
quantity_analysis = cursor.fetchall()
print("Quantity analysis by category:", quantity_analysis)

# Пример произвольного запроса: найти товары с количеством меньше 10
cursor.execute('''
SELECT *
FROM products
WHERE quantity < 10
''')
low_quantity_products = cursor.fetchall()
print("Products with quantity less than 10:", low_quantity_products)

# Закрытие соединения с базой данных
conn.close()
