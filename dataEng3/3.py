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

            # Извлечение данных из XML-структуры
            star_data = {
                'name': root.findtext('name', default=None).strip(),
                'constellation': root.findtext('constellation', default=None).strip(),
                'spectral_class': root.findtext('spectral-class', default=None).strip(),
                'radius': float(root.findtext('radius', default='0').strip()),
                'rotation': float(root.findtext('rotation', default='0').split()[0]),
                'age': float(root.findtext('age', default='0').split()[0]),
                'distance': float(root.findtext('distance', default='0').split()[0]),
                'absolute_magnitude': float(root.findtext('absolute-magnitude', default='0').split()[0])
            }
            data.append(star_data)
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
    input_directory = "3"

    data = parse_xml_files(input_directory)

    save_to_json(data, "output_data3.json")


    sorted_data = sort_data(data, 'age')
    save_to_json(sorted_data, "sorted_data3.json")

    filtered_data = filter_data(data, 'constellation', 'Рыбы')
    save_to_json(filtered_data, "filtered_data3.json")

    stats = calculate_statistics(data, 'radius')
    print("Статистические характеристики для радиуса:", stats)

    label_frequency = calculate_label_frequency(data, 'spectral_class')
    print("Частота меток для спектрального класса:", label_frequency)
