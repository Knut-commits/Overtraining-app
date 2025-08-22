from flask import Flask  #my lightweight web frameowrk
from Backend.config import Config #stores resuable settings, keeps the app organized
from Backend.routes import routes #improting the bluepritn routes from route file.
from Backend.extension import db,jwt 
from waitress import serve #importing waitress to run the app in production


def create_app():

    app = Flask(__name__)#creats new flask instance
    app.config.from_object(Config)#loads the config settings from the config file
    
    
    db.init_app(app) #intilizes the data with the app instance
    jwt.init_app(app) # intiliES THE jwt with teh app instance

    app.register_blueprint(routes) #registers the blue print routes wiht the app instance
    return app



if __name__ == "__main__":
    app = create_app() #calls the create app function to create teh app ibstance
    serve(app, host = "0.0.0.0", port = 5000) 
    
    
        