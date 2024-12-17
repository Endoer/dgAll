import json
import msgpack
import os

with open('third_task.json', 'r', encoding='utf-8') as file:
    products = json.load(file)

aggregated_info = {}

for product in products:
    product_name = product['name']
    price = product['price']

    if product_name not in aggregated_info:
        aggregated_info[product_name] = {
            'total_price': 0,
            'count': 0,
            'max_price': float('-inf'),
            'min_price': float('inf')
        }

    aggregated_info[product_name]['total_price'] += price
    aggregated_info[product_name]['count'] += 1
    aggregated_info[product_name]['max_price'] = max(aggregated_info[product_name]['max_price'], price)
    aggregated_info[product_name]['min_price'] = min(aggregated_info[product_name]['min_price'], price)

# Вычислите среднюю цену для каждого товара
for product_name in aggregated_info:
    aggregated_info[product_name]['average_price'] = aggregated_info[product_name]['total_price'] / aggregated_info[product_name]['count']
    del aggregated_info[product_name]['total_price']
    del aggregated_info[product_name]['count']
print(aggregated_info)
with open('aggregated_info.json', 'w', encoding='utf-8') as file:
    json.dump(aggregated_info, file, ensure_ascii=False, indent=4)

with open('aggregated_info.msgpack', 'wb') as file:
    msgpack.dump(aggregated_info, file)

size_json = os.path.getsize('aggregated_info.json')
size_msgpack = os.path.getsize('aggregated_info.msgpack')

print(f"Размер JSON-файла: {size_json} байт")
print(f"Размер MessagePack-файла: {size_msgpack} байт")
