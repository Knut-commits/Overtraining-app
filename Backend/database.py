from Backend.extension import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False) #size of 80 characters and can't be empty
    password = db.Column(db.String(200), nullable = False) #size of 200 characters and can;t be empty

class Data(db.Model):
    data_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False) #foreign key for the user table, links the user ot their data
    dateinput = db.Column(db.DateTime, default = datetime.utcnow) #date and time of teh data entry, defualts to current date and time 
    Base_heart_rate = db.Column(db.Float, nullable = False) #base heart rate in beats per minute
    heart_rate = db.Column(db.Float, nullable = False) 
    sleep = db.Column(db.Float, nullable = False) #amount of sleep in hours  
    # mood = db.Column(db.Float, nullable = False) #mood on a scale of 1 to 10
    # fatigue = db.Column(db.Float, nullable = false) # fatique ona  scale of 1 to 10
    

