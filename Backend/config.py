import os #as im puhsing to github so we need to keep these like pdatabase urls secret 
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))   # project root
INSTANCE_DIR = os.path.join(BASE_DIR, "instance") #instance folder for database and other files
os.makedirs(INSTANCE_DIR, exist_ok=True)  # making sure the folder exists


DB_PATH = os.path.join(INSTANCE_DIR, "app.db")
DB_URI_DEFAULT = "sqlite:///" + DB_PATH.replace("\\", "/")  # normalize slashes so it works on windows too
class Config:
    SECRET_KEY = os.getenv('SECRET', "my_dev_secret_key") #secret key, used for signing cookies and security features
    SQLALCHEMY_DATABASE_URI = os.getenv( "DATABASE_URL",DB_URI_DEFAULT) #databas url, if nto found uses defualt local sqlite databse
    SQLALCHEMY_TRACK_MODIFICATIONS = False #disables track mdoifciton in roder ot save memory
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "dev_jwt_secret") #secret key for JWT, used for signing tokens