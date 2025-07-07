from flask import Flask #my lightweight web frameowrk
from flask_sqlalchemy import SQLALchemy #ORM(Object relational mapping) for databases, so I can define opython classes whihc link to sql databases. )
from flask_jwt_extended import JWTManager #secures routes so only logged in users can access certain parts
from config import Config #stores resuable settings, keeps the app organized

db= SQLALchemy() #creates a new instancew of sqLALchemy class
jwt= JWTManager() #creates a new instance of the jwtManager class

def create_app():
    app = Flask(__name__)#creats new flask instance
    app.config.from_object(Config)#loads the config settings from the config file
    
    
    db.init_app(app) #intilizes the data with the app instance
    jwt.init_app(app) # intiliES THE jwt with teh app instance


    if__name__ == "__main__":
        app = create_app() #calls the create app function to create teh app ibstance
        app.run(debug=True_)

        