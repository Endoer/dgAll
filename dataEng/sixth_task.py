import requests
import pandas as pd

url = "https://petstore.swagger.io/v2/pet/findByStatus?status=available"
output_file_path = 'output6.html'

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def create_html_table(data, output_file_path):
    df = pd.DataFrame(data)
    html_table = df.to_html(index=False)
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(html_table)

data = fetch_data(url)
data = data[:50]

create_html_table(data, output_file_path)