from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, session
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
app.permanent_session_lifetime = timedelta(days=7)


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
list_item =[]
weekdata = []

@app.route("/projectHabitTracker")
def projecthabittracker():
    if session.get("email") or email:
        return redirect(url_for("habitTracker"))
    return render_template("login.html")

@app.route("/habitTracker", defaults={"username": "Friend", "email": ""})
@app.route("/habitTracker")
def habitTracker():
    username = session.get("username")
    email = session.get("email")
    # print(session["username"])
    # print(session["email"])

    # print(username, email)
    if not email:
        # print(email)
        return render_template("login.html")

    global list_item, weekdata
    list_item = ["Assignment" , "Work" , "Physical Exercise", "Project1", "Project2" ,"Today's learning", "A good thing", "A bad thing", "Note"]    
    todays_date = date.today()
    totalweek = []
    # print("in tracker",username, email)
    last_date = todays_date 
    if session["email"] != "":
        for i in range(-3,4):

            day = str(last_date + timedelta(i))

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
            
    # global username, email
    # username = session["usernam"]
    # email = session["emai"]
    # print("username start page",username, email)
    # print(totalweek)
    weekdata = totalweek
    return render_template("habithomepage.html", activities = list_item , totalweekdata = totalweek, username = username, email = email)
 



@app.route("/submitTracker", methods = ["POST", "GET" ])
def habit():
    print("THE HABIT IS CALLED")

    global data, start_date
    payload = request.get_json()
    start_date = payload["start_date"]
    changes = payload["changes"]

    print(start_date)
    print(changes)

    date_format = '%Y-%m-%d'
    start_date  = datetime.strptime(start_date , date_format).date()
    data = changes
    print("Log of a day " , data , session["email"])

    # print(email )
    # print(email  == "")
    if   session["email"] == '' :
        
        return render_template('login.html')
    
    else:
        save_cell(session["username"] ,session["email"], changes , start_date)    
        print(session["username"] ,session["email"], changes , start_date)
    return redirect(url_for('habitTracker' , username = session["username"] ,email = session["email"]))


def save_cell(username ,email, changes , startdate):
    global weekdata
    print("Save cell called")
    for habit, value1 in changes.items():

        for afterdate , value2 in value1.items():
            print(username, email, habit, startdate , afterdate , value2)
            
            
            if len(value2) == 1:
                # date1 = datetime.strptime(startdate, "%Y-%m-%d")
                # converting
                date2 = date.fromisoformat( afterdate )
                
                print(type(startdate), type(afterdate))
                delta = date2 - startdate
                diff_in_days = abs(delta.days)
                print(diff_in_days)
                if "note" in value2.keys():
                    dayData = weekdata[diff_in_days]
                    hab = dayData['habits']
                    print(dayData , "daydata")
                    if habit in hab:
                        kit = hab[habit]
                        if "status" in kit.keys():
                            print("inside1")
                            habi = hab[habit]
                            print(habi , ' habit')
                            value2["status"] = habi["status"]

                else:
                    dayData = weekdata[diff_in_days]
                    hab = dayData['habits']
                    if habit in hab:
                        kit = hab[habit]
                        if "note" in hab[habit].keys():
                            print("inside2")
                            habi = hab[habit]
                            value2["note"] = habi["note"]
                        
                print(afterdate)
                print(value2)


            upload_data(username ,email, habit,  startdate , afterdate , value2)

    return 

def upload_data(username ,email , habit, upload_date ,event_date, data):
    # print("upload cell called")   
    res = database.save_habit(username ,email, habit, upload_date , event_date, data)
    # print(res , 'sucessfull')
    return 

from datetime import datetime, timedelta

@app.route('/retrieve_data', methods=['GET'])
def retrieve_data():
    global email, username
    print(email, username, "username email")

    start = request.args.get("start")
    end = request.args.get("end")
    days = int(request.args.get("day"))
    # print(start, end , days , "this is retrive function")
    start_date = datetime.fromisoformat(start.replace("Z", ""))
    end_date = datetime.fromisoformat(end.replace("Z", ""))

    totalweek = []
    for i in range(days, -1, -1):
        day_str = str((end_date - timedelta(days=i)).strftime("%Y-%m-%d"))
        # print(email, username, "username email")

        docs = database.find_by_date(email, day_str)
        # print(docs)
        print(list(docs))
        day_data = {}
        for d in docs:
            day_data[d["habit"]] = {
                "status": d["data"].get("status", ""),
                "note": d["data"].get("note", "")
            }

        totalweek.append({
            "date": day_str,
            "habits": day_data
        })

    print(totalweek)
    return jsonify(totalweek)

@app.route('/week_data', methods=['GET'])
def week_data():
    global email, username
    print(email,  "username email")

    start = request.args.get("start")
    end = request.args.get("end")
    days = int(request.args.get("day"))
    start_date = datetime.fromisoformat(start.replace("Z", ""))
    end_date = datetime.fromisoformat(end.replace("Z", ""))
    movement = int(request.args.get("movement"))
    
    # if movement == -1:
    #     end_date = end + timedelta(-7)
    # else:
    #     end_date = end + timedelta(7)  
    # print(email,  "username email")
    print(start_date, end_date , days , "this is week function")

    totalweek = []
    for i in range(days):
        day_str = str((start_date + timedelta(i)).strftime("%Y-%m-%d"))

        docs = database.find_by_date(session["email"], day_str)
        # print(docs)
        # print(list(docs))
        day_data = {}
        for d in docs:
            day_data[d["habit"]] = {
                "status": d["data"].get("status", ""),
                "note": d["data"].get("note", "")
            }

        totalweek.append({
            "date": day_str,
            "habits": day_data
        })
    print("total week",totalweek)
    return jsonify(totalweek)


import user
import traceback
import threading
import random
# session.permanent = True
import pw
password = ''
@app.route('/login' , methods = ['POST', 'GET'])
def login():
    global  key,password   
    try:
        if request.method == "POST":
            session["username"] = request.form.get("Name")
            session["email"] = request.form.get('Email')
            password = request.form.get('Password')
            print(session["email"], session["username"], password)
            

            if database.find_by_email(session['email']):
                check = pw.check(session['email'], password)
                print(check)
                if check == True:
                    print(True)
                   
                    if not session["username"]:
                        user = database.username_by_email(session["email"]) 
                        if user != "NoData": 
                            session["username"] = user
                        else:
                            session["username"] = "Admin"

                    return redirect(url_for('habitTracker'))
                elif check == False:
                    print(check)
                    flash("Invalid Credintials, Try again.")                   
                    return render_template('login.html')
                
                else:
                    print(check)
                    key_val = random.randint(100000, 999999)
                    time = datetime.utcnow().isoformat()

                    # THreading is used to run send email asynchonocolly
                    threading.Thread(
                        target = user.resend_user_email,
                        args = (session["email"], key_val, time),
                        daemon =True
                    ).start()

                    key = key_val
                    # print(key, "in login")

                    return render_template("entercode.html" )

            # print(username, email)
            else:
                key_val = random.randint(100000, 999999)
                time = datetime.utcnow().isoformat()

        # THreading is used to run send email asynchonocolly

                threading.Thread(
                    target = user.resend_user_email,
                    args = (session["email"], key_val, time),
                    daemon =True
                ).start()

                key = key_val
                print(key, "in login")
                print("functiom called nothing")
                return render_template("entercode.html" )
        else:
            return render_template("login.html")
    except Exception as e:
        print(traceback.format_exc())  # 👈 shows error in Render logs
        return "Server error", 500
    
@app.route('/logincheck')
def logincheck():
    

    
        # print("in log out" , session["email"], session["username"])
    logOut()
    if session:
        print(session, "session")
    return  render_template('login.html')

def logOut():

    session.clear()
    return 



@app.route('/entercode' , methods = ['POST', 'GET'])
def code():
    # global username, email
    global password
    if request.method == "POST" :
        userinput = request.form['enteredcode']
        print(userinput)
        global key
        # print(key ,"in code")
        # print(type(userinput) , userinput, key)
        if int(userinput) == key:
            database.add_user(session["email"], password, session["username"])
            # print(username)
            # print(key)
            # flash("Account created Sucessfully.")

            if data:
                print(data  , " in the code function.")
                save_cell(session["username"], session["email"], data , start_date)
            time.sleep(.5)
            print("in code the session data",session["username"], session["email"])
            return redirect(url_for('habitTracker'))
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

@app.route("/recording")
def record():
    return render_template("recording.html")

if __name__ == '__main__' :
    app.run(debug  = True)