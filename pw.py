from pymongo import MongoClient
import os

from dotenv import load_dotenv
load_dotenv()
mongo_URI = os.getenv("MONGO_URI")
client = MongoClient(mongo_URI)
db = client.HabitTracker

collection2 = db.userdata
def check(email ,pw):

    
    data = collection2.find({
        'email' :email,
    })
    
    # print(list(data))
    for d in data:
        print(d)
        if "password" in d.keys():
            print(d["password"], "password is here")
            return d['password']  == pw
        
    return "nothing password detected"



# output = check("omprakashmahato0010@gmail.com", "asdfghjkl")
# print(output)