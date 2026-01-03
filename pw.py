from pymongo import MongoClient
import os

from dotenv import load_dotenv
load_dotenv()
mongo_URI = os.getenv("MONGO_URI")
client = MongoClient(mongo_URI)
db = client.HabitTracker

collection2 = db.userdata
def check(email ,pw):

    
    data = collection2.find_by_email({
        'email' :email,
    })
    return data['password'] == pw

