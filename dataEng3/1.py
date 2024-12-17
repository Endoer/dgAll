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
                    item = {
                        'category': soup.find('span', text=lambda t: t and t.strip().startswith('Категория')).text.split(":", 1)[-1].strip() if soup.find('span', text=lambda t: t and t.strip().startswith('Категория')) else None,
                        'title': soup.find('h1', {'class': 'book-title'}).text.strip() if soup.find('h1', {'class': 'book-title'}) else None,
                        'author': soup.find('p', {'class': 'author-p'}).text.strip() if soup.find('p', {'class': 'author-p'}) else None,
                        'pages': int(soup.find('span', {'class': 'pages'}).text.strip().split(" ")[-2]) if soup.find('span', {'class': 'pages'}) else None,
                        'year': int(soup.find('span', {'class': 'year'}).text.strip().split(' ')[-1]) if soup.find('span', {'class': 'year'}) else None,
                        'ISBN': soup.find('span', text=lambda t: t and t.strip().startswith('ISBN')).text.split(":", 1)[-1] if soup.find('span', text=lambda t: t and t.strip().startswith('ISBN')) else None,
                        'description': soup.find('p', text=lambda t: t and t.strip().startswith('Описание')).text.split(" ", 1)[-1] if soup.find('p', text=lambda t: t and t.strip().startswith('Описание')) else None,
                        'rating': float(soup.find('span', text=lambda t: t and t.strip().startswith('Рейтинг')).text.split(":", 1)[-1]) if soup.find('span', text=lambda t: t and t.strip().startswith('Рейтинг')) else None,
                        'views': int(soup.find('span', text=lambda t: t and t.strip().startswith('Просмотры')).text.split(":", 1)[-1]) if soup.find('span', text=lambda t: t and t.strip().startswith('Просмотры')) else None
                    }
                    print(item)
                    data.append(item)
    return data

def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Загрузка данных из JSON-файла
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

if __name__ == "__main__":
    input_directory = "1"

    data = parse_html_files(input_directory)
    save_to_json(data, "output_data1.json")

    sorted_data = sort_data(data, 'rating')
    save_to_json(sorted_data, "sorted_data1.json")

    filtered_data = filter_data(data, 'category', 'фэнтези')
    save_to_json(filtered_data, "filtered_data1.json")

    stats = calculate_statistics(data, 'rating')
    print("Статистические характеристики для 'value':", stats)

    label_frequency = calculate_label_frequency(data, 'category')
    print("Частота меток для 'category':", label_frequency)
