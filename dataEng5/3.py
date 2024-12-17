import msgpack
from pymongo import MongoClient
import json

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "5_database"
COLLECTION_NAME = "5_collection"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

data = []
with open('task_3_item.msgpack', "rb") as file:
    reader = msgpack.unpack(file)
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

collection.delete_many({
    "$or": [
        {"salary": {"$lt": 25000}},
        {"salary": {"$gt": 175000}}
    ]
})

collection.update_many({}, {"$inc": {"age": 1}})

collection.update_many(
    {"job": {"$in": ["Повар", "Программист"]}},
    {"$mul": {"salary": 1.05}}
)

collection.update_many(
    {"city": {"$in": ["Афины", "Осера"]}},
    {"$mul": {"salary": 1.07}}
)

collection.update_many(
    {"city": "Афины", "job": {"$in": ["Повар", "Программист"]}, "age": {"$gt": 25, "$lt": 45}},
    {"$mul": {"salary": 1.10}}
)

collection.delete_many({"age": {"$lt": 18}})

with open(f'3_after_all_queries.json', 'w', encoding="utf-8") as f:
        json.dump(list(collection.find()), f, indent=4, ensure_ascii=False,  default=str)