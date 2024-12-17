import pandas as pd
import json
import msgpack
import pickle
import os

data = pd.read_csv('kaggle_london_house_price_data.csv')
selected_columns = ['fullAddress','postcode','country','outcode','latitude',
                    'longitude','bathrooms','bedrooms','history_date','history_price','history_percentageChange']
data = data[selected_columns]
statistics = {}

for column in data.columns:
    print(data[column].dtype)
    if data[column].dtype in ['int64', 'float64']:
        statistics[column] = {
            'max': float(data[column].max()),
            'min': float(data[column].min()),
            'mean': float(data[column].mean()),
            'sum': float(data[column].sum()),
            'std': float(data[column].std())
        }
    elif data[column].dtype == 'object':
        statistics[column] = {
            'frequency': data[column].value_counts().to_dict()
        }

with open('statistics.json', 'w', encoding='utf-8') as file:
    json.dump(statistics, file, ensure_ascii=False, indent=4)

data.to_csv('data_fifth.csv', index=False)
data.to_json('data_fifth.json', orient='records', force_ascii=False, indent=4)
with open('data_fifth.msgpack', 'wb') as file:
    file.write(msgpack.packb(data.to_dict(orient='records'), use_bin_type=True))
with open('data_fifth.pkl', 'wb') as file:
    pickle.dump(data, file)

size_csv = os.path.getsize('data_fifth.csv')
size_json = os.path.getsize('data_fifth.json')
size_msgpack = os.path.getsize('data_fifth.msgpack')
size_pkl = os.path.getsize('data_fifth.pkl')

print(f"Размер CSV-файла: {size_csv} байт")
print(f"Размер JSON-файла: {size_json} байт")
print(f"Размер MessagePack-файла: {size_msgpack} байт")
print(f"Размер PKL-файла: {size_pkl} байт")
