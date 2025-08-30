#this file has been created as my app.py imports routes.py whihc imports db from app.py creating a loop
from flask_sqlalchemy import SQLAlchemy #ORM(Object relational mapping) for databases, so I can define opython classes whihc link to sql databases. )
from flask_jwt_extended import JWTManager #secures routes so only logged in users can access certain parts

db = SQLAlchemy()
jwt = JWTManager()

