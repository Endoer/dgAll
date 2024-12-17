import os
import json
import xml.etree.ElementTree as ET
from collections import Counter

# Функция для парсинга XML-файлов и извлечения данных
def parse_xml_files(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            filepath = os.path.join(directory, filename)
            tree = ET.parse(filepath)
            root = tree.getroot()

            for clothing in root.findall('clothing'):
                clothing_data = {
                    'id': int(clothing.findtext('id', default=None).strip()),
                    'name': clothing.findtext('name', default='').strip(),
                    'category': clothing.findtext('category', default='').strip(),
                    'size': clothing.findtext('size', default='').strip(),
                    'color': clothing.findtext('color', default='').strip(),
                    'material': clothing.findtext('material', default='').strip(),
                    'price': int(clothing.findtext('price', default='0').strip()),
                    'rating': float(clothing.findtext('rating', default='0').strip()),
                    'reviews': int(clothing.findtext('reviews', default='0').strip()),
                    'new': clothing.findtext('new', default='').strip(),
                    'exclusive': clothing.findtext('exclusive', default='').strip(),
                    'sporty': clothing.findtext('sporty', default='').strip()
                }
                data.append(clothing_data)
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
    return [item for item in data if item[field] == value]

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

# Основной блок выполнения
if __name__ == "__main__":
    input_directory = "4"

    data = parse_xml_files(input_directory)

    save_to_json(data, "output_data4.json")

    sorted_data = sort_data(data, 'price')
    save_to_json(sorted_data, "sorted_data4.json")

    filtered_data = filter_data(data, 'material', 'Нейлон')
    save_to_json(filtered_data, "filtered_data4.json")

    stats = calculate_statistics(data, 'price')
    print("Статистические характеристики для радиуса:", stats)

    label_frequency = calculate_label_frequency(data, 'material')
    print("Частота меток для спектрального класса:", label_frequency)