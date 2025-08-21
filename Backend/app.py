from flask import Flask #my lightweight web frameowrk
from config import Config #stores resuable settings, keeps the app organized
from routes import routes #improting the bluepritn routes from route file.
from extension import db,jwt 


def create_app():
    app = Flask(__name__)#creats new flask instance
    app.config.from_object(Config)#loads the config settings from the config file
    
    
    db.init_app(app) #intilizes the data with the app instance
    jwt.init_app(app) # intiliES THE jwt with teh app instance

    app.register_blueprint(routes) #registers the blue print routes wiht the app instance
    return app



if __name__ == "__main__":
    app = create_app() #calls the create app function to create teh app ibstance
    app.run(debug=True)

        