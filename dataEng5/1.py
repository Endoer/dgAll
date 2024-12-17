import csv
from pymongo import MongoClient
import json

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "5_database"
COLLECTION_NAME = "5_collection"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

file_path = "task_1_item.csv"  

data = []
with open(file_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter=';')
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

query_1 = collection.find().sort("salary", -1).limit(10)
with open("1_1.json", "w", encoding="utf-8") as file:
    json.dump(list(query_1), file, indent=4, ensure_ascii=False,  default=str)

query_2 = collection.find({"age": {"$lt": 30}}).sort("salary", -1).limit(15)
with open("1_2.json", "w", encoding="utf-8") as file:
    json.dump(list(query_2), file, indent=4, ensure_ascii=False, default=str)
print(list(query_2))

city = "Хельсинки"  
jobs = ["Программист", "Врач", "Повар"]  
query_3 = collection.find({
    "$and": [
        {"city": city},
        {"job": {"$in": jobs}}
    ]
}).sort("age", 1).limit(10)
with open("1_3.json", "w", encoding="utf-8") as file:
    json.dump(list(query_3), file, indent=4, ensure_ascii=False, default=str)

age_range = {"$gte": 20, "$lte": 35} 
query_4_count = collection.count_documents({
    "$and": [
        {"age": age_range},
        {"year": {"$gte": 2019, "$lte": 2022}},
        {"$or": [
            {"salary": {"$gt": 50000, "$lte": 75000}},
            {"salary": {"$gt": 125000, "$lt": 150000}}
        ]}
    ]
})
with open("1_4.json", "w", encoding="utf-8") as file:
    json.dump({"count": query_4_count}, file, indent=4, default=str)
