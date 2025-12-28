# Next update user login
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
import os
import random

def userlogin(email, key , time):

    msg = MIMEText(f"HabitTracker login service code : {key} \n This event requested at {time}. \n If you didn't request this code, please email to: \nadmin@ommahato.com ")
    msg['Subject'] = "HabitTracker Code"
    msg["From"] = os.getenv("EMAILZOHO")
    msg["To"] = email


    with smtplib.SMTP("smtp.zoho.com" , 587) as server:
        server.starttls()
        server.login(os.getenv("EMAILZOHO"), os.getenv("PWZOHO"))
        server.send_message(msg)
             
    
def key_value(key = 000000):
    return key