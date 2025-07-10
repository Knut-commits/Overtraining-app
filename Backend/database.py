from app import db
from datetime import datetime

class User(db.Model):
    user_id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable - False) #size of 80 characters and can't be empty
    password = db.Column(db.String(200), nullable = False) #size of 200 characters and can;t be empty

class data(db.Model):
    data_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable = False) #foreign key for the user table, links the user ot their data
    dateinput = db.Column(db.DateTime, defualt = datetime.utcnow) #date and time of teh data entry, defualts to current date and time 
    Base_heart_rate = db.Column(db.Float, nullable = False) #base heart rate in beats per minute
    Recorded_heart_rate = db.Column(db.Float, nullable = False) 
    sleep = db.Column(db.Float, nullable = False) #amount of sleep in hours  
    
    

