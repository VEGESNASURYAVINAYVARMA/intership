from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Change URI if needed
db = client["quiz_db"]
quiz_collection = db["quizzes"]
