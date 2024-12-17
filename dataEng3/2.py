import os
import json
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter

def parse_html_files(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                
                objects = soup.find_all('div', {'class': 'pad'})  # Предполагается, что объекты заключены в div с классом "pad"
                for obj in objects:
                    product_item = obj.find('div', {'class': 'product-item'})
                    if not product_item:
                        continue
                    name = product_item.find('span').text.strip() if product_item.find('span') else None

                    price_tag = product_item.find('price')
                    price = None
                    if price_tag:
                        price_text = price_tag.text.strip().replace('₽', '').replace(' ', '')
                        try:
                            price = float(price_text)
                        except ValueError:
                            price = None

                    strong_tag = product_item.find('strong')
                    bonuses = None
                    if strong_tag:
                        bonus_text = strong_tag.text.strip().replace('+ начислим ', '').replace(' бонусов', '')
                        try:
                            bonuses = int(bonus_text)
                        except ValueError:
                            bonuses = None

                    characteristics = {}
                    ul_tag = product_item.find('ul')
                    if ul_tag:
                        for li in ul_tag.find_all('li'):
                            li_type = li.get('type')
                            li_value = li.text.strip()
                            if li_type:
                                characteristics[li_type] = li_value

                    item = {
                        'name': name,
                        'price': price,
                        'bonuses': bonuses,
                        'characteristics': characteristics
                    }
                    data.append(item)
    return data

def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_from_json(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def sort_data(data, field):
    return sorted(data, key=lambda x: x[field] if x[field] is not None else 0, reverse=True)

def filter_data(data, field, value):
    return [item for item in data if value in item[field]]

def calculate_statistics(data, field):
    values = [item[field] for item in data if item[field] is not None]
    return {
        'sum': sum(values),
        'min': min(values),
        'max': max(values),
        'mean': sum(values) / len(values) if values else None,
        'count': len(values)
    }

def calculate_label_frequency(data, field):
    labels = [item[field] for item in data if item[field] is not None]
    return Counter(labels)

if __name__ == "__main__":
    input_directory = "2"

    data = parse_html_files(input_directory)
    save_to_json(data, "output_data2.json")


    sorted_data = sort_data(data, 'price')
    save_to_json(sorted_data, "sorted_data2.json")

    filtered_data = filter_data(data, 'name', 'Xiaomi')
    save_to_json(filtered_data, "filtered_data2.json")

    stats = calculate_statistics(data, 'price')
    print("Статистические характеристики для 'price':", stats)

    label_frequency = calculate_label_frequency(data, 'name')
    print("Частота меток для 'name':", label_frequency)