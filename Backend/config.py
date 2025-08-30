import os #as im puhsing to github so we need to keep these like pdatabase urls secret 
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET', "my_dev_secret_key") #secret key, used for signing cookies and security features
    SQLALCHEMY_DATABASE_URI = os.getenv( "DATABASE_URL",
    "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "../instance/app.db"))# using instance folder as Flask convention
    SQLALCHEMY_TRACK_MODIFICATIONS = False #disables track mdoifciton in roder ot save memory
    JWT_SECRET_KEY = os.getenv("JWT_SECRET") #secret key for JWT, used for signing tokens