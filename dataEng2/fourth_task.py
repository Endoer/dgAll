import pickle
import json

with open('fourth_task_products.json', 'rb') as file:
    products = pickle.load(file)

with open('fourth_task_updates.json', 'r', encoding='utf-8') as file:
    price_updates = json.load(file)

for update in price_updates:
    product_name = update['name']
    method = update['method']
    param = update['param']

    for product in products:
        if product['name'] == product_name:
            if method == 'add':
                product['price'] += param
            elif method == 'sub':
                product['price'] -= param
            elif method == 'percent+':
                product['price'] *= (1 + param )
            elif method == 'percent-':
                product['price'] *= (1 - param )

print(products)
with open('fourth_task.pkl', 'wb') as file:
    pickle.dump(products, file)

