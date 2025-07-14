from flask import Blueprint, request, jsonify, session # import neccessary moudles ofr all routes (logging in, submitting data etc)
from datetime import datetime
from app import db # importing database instance
from backend.database import User, Data #importing user and data databases
from backend.calculations import calculate_score # importing the fucntion to calculate the overtrianing scores

routes= Blueprint('routes', __name__) # creating blue prints for the routes, so easier to organise and less redudant code

@routes.route('/signup', methods = ['POST']) # route for signing up a new account
def signup():
    data = reguest.get_json() # get the json data from the reuqest
    username = data.get['username'] # get the username from the data as the data is a dictionary so im accesisng the value of the username key
    password = data.get['password'] # the same but for password

    if User.query.filter_by(username=username).first(): # checks if username already exists in database, first() reyurns the first result or none if none found, saves time
        return jsonify({'errpr': 'Username already exist'}), 409 # if username exists returns the error message and 409 status code
    
    new_user = User(username = username, password= password) # creates a new user instance with the username and password
    db.session.add(new_user) #add the new user to the database session
    db.session.commit()

    return jsonify({'message': "aaccount created'}), 201"})