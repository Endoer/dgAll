import csv
from pymongo import MongoClient
import json
import pickle
import pandas as pd

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "5_database"
COLLECTION_NAME = "5_4_collection"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

df1 = pd.read_csv("part1.csv")
df2 = pd.read_pickle("part2.pkl")

records = df1.to_dict(orient='records')
records.extend(df2.to_dict(orient='records'))

collection.insert_many(records)


query_1 = collection.find().sort("average_rating", -1).limit(50)
with open("4_1.json", "w", encoding="utf-8") as file:
    json.dump(list(query_1), file, indent=4, ensure_ascii=False, default=str)

query_2 = collection.find({"average_rating": {"$gt": 4.0}})
with open("4_2.json", "w", encoding="utf-8") as file:
    json.dump(list(query_2), file, indent=4, ensure_ascii=False, default=str)

query_3 = collection.find({"authors": {"$in": ["Bill Bryson", "Molly Hatchet"]}})
with open("4_3.json", "w", encoding="utf-8") as file:
    json.dump(list(query_3), file, indent=4, ensure_ascii=False, default=str)

query_4 = collection.find({"language_code": "eng"})
with open("4_4.json", "w", encoding="utf-8") as file:
    json.dump(list(query_4), file, indent=4, ensure_ascii=False, default=str)

query_5 = collection.count_documents({"num_pages": {"$gt": 400}})
with open("4_5.json", "w", encoding="utf-8") as file:
    json.dump({"count":query_5}, file, indent=4, ensure_ascii=False, default=str)

query_6 = collection.aggregate([
    {
        "$group": {
            "_id": None,
            "average_rating": {"$avg": "$average_rating"}
        }
    }
])
with open("4_6.json", "w", encoding="utf-8") as file:
    json.dump(list(query_6), file, indent=4, ensure_ascii=False, default=str)

query_7 = collection.aggregate([
    {
        "$group": {
            "_id": "$publisher",
            "count": {"$sum": 1}
        }
    }
])
with open("4_7.json", "w", encoding="utf-8") as file:
    json.dump(list(query_7), file, indent=4, ensure_ascii=False, default=str)

query_8 = collection.aggregate([
    {
        "$group": {
            "_id": "$publisher",
            "max_pages": {"$max": "$num_pages"},
            "min_pages": {"$min": "$num_pages"}
        }
    }
])
with open("4_8.json", "w", encoding="utf-8") as file:
    json.dump(list(query_8), file, indent=4, ensure_ascii=False, default=str)

query_9 = collection.aggregate([
    {
        "$group": {
            "_id": "$authors",
            "avg_rating": {"$avg": "$average_rating"}
        }
    }
])
with open("4_9.json", "w", encoding="utf-8") as file:
    json.dump(list(query_9), file, indent=4, ensure_ascii=False, default=str)

query_10 = collection.aggregate([
    {
        "$group": {
            "_id": "$authors",
            "minRating": { "$min": "$average_rating" },
            "avgRating": { "$avg": "$average_rating" },
            "maxRating": { "$max": "$average_rating" }
        }
    }
])
with open("4_10.json", "w", encoding="utf-8") as file:
    json.dump(list(query_10), file, indent=4, ensure_ascii=False, default=str)

query_11 = collection.update_one({"bookID": 1}, {"$set": {"num_pages": 200}})
query_12 = collection.delete_one({"isbn": "0743273567"})
query_13 = collection.update_many({"authors": "Harper Lee"}, {"$set": {"average_rating": 4.5}})
query_14 = collection.delete_many({"ratings_count": {"$lt": 1000}})
query_15 = collection.update_many({"publication_date": {"$lt": "1950-01-01"}}, {"$inc": {"average_rating": 0.1}})

with open(f'4_after_all_queries.json', 'w', encoding="utf-8") as f:
        json.dump(list(collection.find()), f, indent=4, ensure_ascii=False,  default=str)