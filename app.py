from flask import Flask, render_template, request, url_for, redirect, flash
import logging

from openai import OpenAI
import requests
import os

from flask_sitemap import Sitemap

# for connecting to mongo db server
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime , timedelta , date
# System files
import database as database
import time

# load .env variables that we stored cluter string from mongodv in .env 
load_dotenv()

app = Flask(__name__)
# for flashing notification and mongodb server
app.secret_key = os.getenv("SECRET_KEY", "default_secret")


# for generating sitemap (sitemap.xml) for google search console
ext = Sitemap(app=app)


# if If your actual site and backend are on different domains, Flask needs flask-cors so browsers allow the request.
from flask_cors import CORS
CORS(app)


# configure logging
# for production, consider writing to a file or an external logging service

if not app.debug:
    file_handler = logging.FileHandler('app_error.log')
    file_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(asctime)s- %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

# Connect to MongoDB
mongo_uri = os.getenv("MONGO_URI")
# print("Connecting to:", mongo_uri)
if not mongo_uri:
    # Use app.logger for critical errors
    app.logger.critical("MONGO_URI is not set in .env. Application cannot to database.")
    raise ValueError("MONGO_URI is not set in .env")

try:
    client = MongoClient(mongo_uri)

    # The ping command is cheap and does not require authorization
    client.admin.command('ping')
    app.logger.info("Sucessfully connected to MongoDB!")
    
except Exception as e:
    app.logger.critical(f'Could not connect to MongoDB : {e}')
    # Depending on criticality, you might want to raise here or make the app unusable

    raise ConnectionError(f"Failed to connect to MongoDB: {e}")



db = client["contactdb"]  # Database name
contacts = db["contacts"] # Collection name




@app.route('/')
def homepage():
    data = [
        {
            "question" : "Which language is used in Data Science?",
            "option1":"Python",
            "option2":"Java",
            "option3":"C++",
            "level":"easy",
            "language":"python",
            "id": 1,
            "ans":"python"
        },
        {
            "question" : "What is the DATATYPE of (3,4)?",
            "option1":"List",
            "option2":"Dictionary",
            "option3":"Tuple",
            "level":"easy",
            "language":"DSA",
            "id": 2 ,
            "ans":"Tuple"
            
        },
        {
            "question" : "3==3.0?",
            "option1":"True",
            "option2":"False",
            "option3":"NA",
            "level":"easy",
            "language":"Boolean",
            "id":4,
            "ans":"True"
            
        },
        {
            "question" : "What does len command does?",
            "option1": "calculate the length",
            "option2": "convert into integer",
            "option3":"calculate the sum",
            "level":"easy",
            "language":"",
            "id":5,
            "ans":"calculate the length"
            
        }
    ]
    return render_template('index.html', data = data)
    # return "our site is live"

    

@app.route('/blogs', methods = ['GET', 'POST'] )
def blogs():


    return render_template('blogs.html')

@app.route('/contact', methods = ['GET', 'POST'] )
def contact():

     return render_template('contact.html')
    
@app.route('/projects', methods = ['GET', 'POST'] )
def projects():

    return render_template('projects.html')




# for collecting user detail from contact.html
@app.route('/collect_subscribe', methods = ['POST', 'GET'])
def collect_subscribe():
    if request.method == "POST":
        

        name = request.form.get('Name')
        email = request.form.get('Email')
        message = request.form.get('Message')

        if not (name and email and message):
            flash('All fields required', 'error')
            raise redirect(url_for('contact'))

        try:
            contacts.insert_one({
                'name': name,
                'email': email,
                'message' : message
            })
            flash('Submission Sucessfull') # flashes notification of submission
        except Exception as e:
            app.logger.error(f"MongoDB insertion error: {e}")
            flash('An unexcepted error occurred while submitting your response. ')
        
        
        
        # return f'Your name is {name}, email is {email}, message is {message} '
        return redirect(url_for('contact'))
      
    else:
        return 'not logged'
    

def showNotifica():
    pass

@app.route('/portfolio')
def portfolio():
    return render_template('projects.html')

@app.route('/services')
def services():
    return 'Services'


@app.route('/chatbot_page' ,methods = ['POST', 'GET'])
def chatbot_page():
    if request.method == 'POST':

        inp = request.form.get('Chat')
        content = generate_response(inp)
        return 'Sucessfullfully collected' + inp + content
    
    return render_template('chatbot.html')



# This works fine

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def generate_response(data):
  response = client.responses.create(
    model="gpt-4o-mini",
    instructions="You are a comedian that tells jokes about {data}",
    input=data,
    # store=True,
  )
  return response.output_text






# Habit Tracker

key = '000000'
username = ''
email = ''
keys =[]
data = {}
start_date = ''

@app.route("/habitTracker", defaults={"username": "Friend", "email": ""})
@app.route("/habitTracker/<username>/<email>")
def habitTracker(username, email):
    
    # print(username, email)
    list_item = ["Assignment" , "Work" , "Physical Exercise", "Project1", "Project2" ,"Today's learning", "A good thing", "A bad thing", "Note"]
    
    todays_date = date.today()
    totalweek = []
    # print("in tracker",username, email)

    if email != "":
        for i in range(4, -1, -1):
            day = str(todays_date - timedelta(i))
            docs = database.find_by_date(email, day)

            day_data = {}

            for d in docs:
                day_data[d["habit"]] = {
                    "status": d["data"].get("status", ""),
                    "note": d["data"].get("note", "")
                }

            totalweek.append({
                "date": day,
                "habits": day_data
            })
    # print(username, email)
    # print(totalweek)
    return render_template("habithomepage.html", activities = list_item , totalweekdata = totalweek, username = username, email = email)
 



@app.route("/submitTracker", methods = ["POST", "GET" ])
def habit():
    # print("THE HABIT IS CALLED")

    global username , email ,data, start_date
    
    payload = request.get_json()
    start_date = payload["start_date"]
    changes = payload["changes"]
    # print(start_date)
    # print(changes)

    date_format = '%Y-%m-%d'
    start_date  = datetime.strptime(start_date , date_format).date()

    data = changes

    print("Log of a day " , data , email)

    print(email )
    print(email  == "")
    if   email == '' :
        
        return render_template('login.html')
    
    else:
        save_cell(username ,email, changes , start_date)    
    return redirect(url_for('habitTracker' , username = username ,email = email))


def save_cell(username ,email, changes , startdate):
    print("Save cell called")
    for habit, value1 in changes.items():

        for afterdate , value2 in value1.items():
            # print("om", habit, startdate + timedelta( int(afterdate)) , value2)
            upload_data(username ,email, habit,  startdate , str(startdate + timedelta(int(afterdate))) , value2)

    return 

def upload_data(username ,email , habit, upload_date ,event_date, data):
    # print("upload cell called")   
    res = database.save_habit(username ,email, habit, upload_date , event_date, data)
    # print(res , 'sucessfull')
    return 


import user
import traceback
import threading
import random
@app.route('/login' , methods = ['POST', 'GET'])
def login():
    global username, email, key

    try:
        if request.method == "POST":
            username = request.form.get("Name")
            email = request.form.get('Email')
            print(username, email)

            key_val = random.randint(100000, 999999)
            time = datetime.utcnow()


            threading.Thread(
                target = user.userlogin,
                args = (email, key_val, time),
                daemon =True
            ).start()

            global key
            key = key_val

            print(key, "in login")
            print(type(key))
            print(keys)
            return render_template("entercode.html" )
        else:
            return render_template("login.html")
    except Exception as e:
        print(traceback.format_exc())  # 👈 shows error in Render logs
        return "Server error", 500


@app.route('/entercode' , methods = ['POST', 'GET'])
def code():
    global username, email
    if request.method == "POST" :
        userinput = request.form['enteredcode']
        print(userinput)
        global key
        print(key ,"in code")
        print(type(userinput) , userinput, key)
        if int(userinput) == key:
            database.add_user(username, email)
            # print(username)
            # print(key)
            # flash("Account created Sucessfully.")

            if data:
                print(data  , " in the code function.")
                save_cell(username, email, data , start_date)
            time.sleep(.5)
            print("in code",username, email)
            return redirect(url_for('habitTracker' , username = username , email = email))
            # return habitTracker(username , email)
        
        else:
            flash("Input Mismatched Try Again" )
            return render_template("entercode.html")
    else:            
        return render_template("entercode.html")


# Fetch the Notebooks 
from kaggle.api.kaggle_api_extended import KaggleApi
@app.route("/kaggleNotebook" , methods =[ "POST", "GET"])
def kaggle():

    kaggle_api = os.getenv("KAGGLE_API_TOKEN")
    api = KaggleApi()
    api.authenticate()

    kernels_list = api.kernels_list(user = os.getenv("KAGGLE_USERNAME"))
    print(kernels_list)
    # print(kernels_list)

    notebooks = []
    for k in kernels_list:
        # if k.author == userName:
        notebooks.append({
            "title": k.title,
            "url": f"https://www.kaggle.com/code/{k.author}/{k.title}"
        })

    return render_template("kaggle.html", notebooks = notebooks)
# print(notebooks)
# print("gvdfjhsbkal")

@app.route("/projectCalculus2", methods =[ "POST", "GET"])
def Calculus():
    return render_template("calculus2.html")

@app.route("/visLearn")
def vislearn():
    return render_template("vislearn.html",methods =[ "POST", "GET"])


if __name__ == '__main__' :

    app.run(debug  = True)