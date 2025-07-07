import os #as im puhsing to github so we need to keep these like pdatabase urls secret 
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET') #secret key, used for signing cookies and security features
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")# defaults to sqlite if there is no database url set in environment variables
    SQLALCHEMY_TRACK_MODIFICATIONS - False #disables track mdoifciton in roder ot save memory
    JWT_SECRET_KEY = os,getenv("JWT_SECRET") #secret key for JWT, used for signing tokens