from flask import Flask, render_template, request, url_for, redirect, flash
import logging




# for connecting to mongo db server
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# load .env variables that we stored cluter string from mongodv in .env 
load_dotenv()

app = Flask(__name__)
# for flashing notification and mongodb server
app.secret_key = os.getenv("SECRET_KEY", "default_secret")


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
print("Connecting to:", mongo_uri)
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
    return render_template('index.html')
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

    


if __name__ == '__main__' :

    app.run(debug  = True)