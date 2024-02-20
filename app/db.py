from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import json
import os

# Load environment variables from config.py
load_dotenv()
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/your_database_name')

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client.get_database()
users_collection = db['users']

# User Schema
user_schema = {
    "userId": str,
    "name": str,
    "email": str,
    "createdAt": str,
}

# Custom JSON encoder to handle ObjectId serialization
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)
