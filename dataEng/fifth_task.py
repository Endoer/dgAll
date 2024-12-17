import pandas as pd
from bs4 import BeautifulSoup

input_file_path = 'fifth_task.html'
output_file_path = 'output_table5.csv'
stats_file_path = 'output_stats5.txt'
def read_html_table(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
    return df

def process_html(input_file_path, output_file_path, stats_file_path):
    df = read_html_table(input_file_path)

    df = df.drop(columns=['Status'])

    mean_price = df['Price'].mean()
    max_price = df['Price'].max()
    min_price = df['Price'].min()

    filtered_df = df[df['Quantity'] < 97]

    # Записываем результаты в отдельные файлы
    with open(stats_file_path, 'w') as stats_file:
        stats_file.write(f"Mean Price: {mean_price}\n")
        stats_file.write(f"Max Price: {max_price}\n")
        stats_file.write(f"Min Price: {min_price}\n")

    filtered_df.to_csv(output_file_path, index=False)

process_html(input_file_path, output_file_path, stats_file_path)