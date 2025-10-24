from pymongo import MongoClient
from bson import ObjectId

def get_db_handle():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["college_mongo"]
    return db

def convert_objectid(data):
    if isinstance(data, list):
        return [convert_objectid(item) for item in data]
    elif isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if isinstance(value, ObjectId):
                new_data[key] = str(value)
            elif isinstance(value, (dict, list)):
                new_data[key] = convert_objectid(value)
            else:
                new_data[key] = value
        return new_data
    else:
        return data


