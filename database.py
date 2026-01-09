from datetime import datetime 
from pymongo import MongoClient
import os

from dotenv import load_dotenv
load_dotenv()


mongo_URI = os.getenv("MONGO_URI")


try:
    client = MongoClient(mongo_URI)

    # The ping command is cheap and does not require authorization
    client.admin.command('ping')
    print("Mongo db connected sucessfully.")
    
    
except Exception as e:
    print(f'Could not connect to MongoDB : {e}')
    # Depending on criticality, you might want to raise here or make the app unusable

    raise ConnectionError(f"Failed to connect to MongoDB: {e}")

db = client.HabitTracker
collection = db.habitTracker

def save_habit(username, email ,habit, upload_date ,event_date , data):

    collection.update_one(
        {
            "email" :email,
            "username": username,
            "habit" : habit,
            "date" : event_date,
            "upload_date": upload_date.isoformat()
        },
        {
            "$set" : {
                "data" : data,
                "updated_at" : datetime.utcnow(),
            },
            "$setOnInsert": {
                "created_at": datetime.utcnow()
            }
            
        },
        upsert = True
    )
    return "Congratulations, for your day."

def find_by_date(email ,date):
    data = collection.find({
        "email" :email,
        "date" : date
    })

    return data if data else None

def habit_history(username , habit):
    data = collection.find({
        "username" : username ,
        "habit" : habit
    }).sort("data" , 1)

    return data

def date_range(username , startdate, enddate):
    data = collection.find({
        "username" : username,
        "date" : {

            "$gte" : startdate,
            "$lte" : enddate
        }
    })

    return data

def find_username(username):
    data = collection.find({
        "username" : username,
    })
    return data


collection2 = db.userdata
def add_user(email , password, username = "Friend" ):
    collection2.update_one(
        {
        'username' :username,
        'email':email,
        'password' : password
        },
        {
            "$set" : {               
                "login_at" : datetime.utcnow(),
            },
            "$setOnInsert": {
                "created_at": datetime.utcnow()
            }
        },
        upsert = True, 
        )
    
def find_by_email(email ):
    data = collection2.find({
        "email" :email,
        
    })
    return True if data else False

