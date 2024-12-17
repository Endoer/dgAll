import csv
from pymongo import MongoClient
import pickle
import json

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "5_database"
COLLECTION_NAME = "5_collection"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

file_path = 'task_2_item.pkl'


data = []
with open(file_path, "rb") as file:
    reader = pickle.load(file)
    for row in reader:
        row["salary"] = int(row["salary"])
        row["age"] = int(row["age"])
        row["year"] = int(row["year"])
        row["_id"] = row.pop("id") # Подсунуть как id mongo
        data.append(row)

try:
    collection.insert_many(data, ordered=False)  
except Exception as e:
    print(f"Error inserting data: {e}")

query_1 = collection.aggregate([
    {
        "$group": {
            "_id": None,
            "minSalary": { "$min": "$salary" },
            "avgSalary": { "$avg": "$salary" },
            "maxSalary": { "$max": "$salary" }
        }
    }
])

# 2. Вывод количества данных по представленным профессиям
query_2 = collection.aggregate([
    {
        "$group": {
            "_id": "$job",
            "count": { "$sum": 1 }
        }
    }
])

# 3. Вывод минимальной, средней, максимальной зарплаты по городу
query_3 = collection.aggregate([
    {
        "$group": {
            "_id": "$city",
            "minSalary": { "$min": "$salary" },
            "avgSalary": { "$avg": "$salary" },
            "maxSalary": { "$max": "$salary" }
        }
    }
])

# 4. Вывод минимальной, средней, максимальной зарплаты по профессии
query_4 = collection.aggregate([
    {
        "$group": {
            "_id": "$job",
            "minSalary": { "$min": "$salary" },
            "avgSalary": { "$avg": "$salary" },
            "maxSalary": { "$max": "$salary" }
        }
    }
])

# 5. Вывод минимального, среднего, максимального возраста по городу
query_5 = collection.aggregate([
    {
        "$group": {
            "_id": "$city",
            "minAge": { "$min": "$age" },
            "avgAge": { "$avg": "$age" },
            "maxAge": { "$max": "$age" }
        }
    }
])

# 6. Вывод минимального, среднего, максимального возраста по профессии
query_6 = collection.aggregate([
    {
        "$group": {
            "_id": "$job",
            "minAge": { "$min": "$age" },
            "avgAge": { "$avg": "$age" },
            "maxAge": { "$max": "$age" }
        }
    }
])

# 7. Вывод максимальной заработной платы при минимальном возрасте
query_7 = collection.aggregate([
    {
        "$group": {
            "_id": { "age": "$age" },
            "maxSalary": { "$max": "$salary" }
        }
    },
    {
        "$sort": { "_id.age": 1 }
    },
    {
        "$limit": 1
    }
])

# 8. Вывод минимальной заработной платы при максимальном возрасте
query_8 = collection.aggregate([
    {
        "$group": {
            "_id": { "age": "$age" },
            "minSalary": { "$min": "$salary" }
        }
    },
    {
        "$sort": { "_id.age": -1 }
    },
    {
        "$limit": 1
    }
])

# 9. Вывод минимального, среднего, максимального возраста по городу при условии, что зарплата больше 50 000, отсортировать по убыванию среднего возраста
query_9 = collection.aggregate([
    {
        "$match": { "salary": { "$gt": 50000 } }
    },
    {
        "$group": {
            "_id": "$city",
            "minAge": { "$min": "$age" },
            "avgAge": { "$avg": "$age" },
            "maxAge": { "$max": "$age" }
        }
    },
    {
        "$sort": { "avgAge": -1 }
    }
])

# 10. Вывод минимальной, средней, максимальной зарплаты в произвольных диапазонах по городу, профессии и возрасту
query_10 = collection.aggregate([
    {
        "$match": {
            "age": { "$gt": 18, "$lt": 25 },
            "salary": { "$gt": 50000 }
        }
    },
    {
        "$group": {
            "_id": { "city": "$city", "job": "$job" },
            "minSalary": { "$min": "$salary" },
            "avgSalary": { "$avg": "$salary" },
            "maxSalary": { "$max": "$salary" }
        }
    }
])

# 11. Произвольный запрос с использованием $match, $group, $sort
query_11 = collection.aggregate([
    {
        "$match": { "age": { "$gt": 30 } }
    },
    {
        "$group": {
            "_id": "$job",
            "avgSalary": { "$avg": "$salary" }
        }
    },
    {
        "$sort": { "avgSalary": -1 }
    }
])

# Сохраняем запросы в формате JSON
queries = {
    "query_1": query_1,
    "query_2": query_2,
    "query_3": query_3,
    "query_4": query_4,
    "query_5": query_5,
    "query_6": query_6,
    "query_7": query_7,
    "query_8": query_8,
    "query_9": query_9,
    "query_10": query_10,
    "query_11": query_11
}

for query_num, query in queries.items():
    with open(f'2_{query_num}.json', 'w', encoding="utf-8") as f:
        json.dump(list(query), f, indent=4, ensure_ascii=False,  default=str)


