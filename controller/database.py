from pymongo import MongoClient
from controller.config_URI import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["Grau_B"]

users_collection = db["users"]
tasks_collection = db["tasks"]