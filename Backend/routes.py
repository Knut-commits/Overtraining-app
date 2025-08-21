from flask import Blueprint, request, jsonify, session # import neccessary moudles ofr all routes (logging in, submitting data etc)
from datetime import datetime
from extension import db # importing database instance
from database import User, data #importing user and data databases
from calculations import calculate_score # importing the fucntion to calculate the overtrianing scores

routes= Blueprint('routes', __name__) # creating blue prints for the routes, so easier to organise and less redudant code

@routes.route('/register', methods = ['POST']) # route for signing up a new account
def register():
    data = reguest.get_json() # get the json data from the reuqest
    username = data.get['username'] # get the username from the data as the data is a dictionary so im accesisng the value of the username key
    password = data.get['password'] # the same but for password

    if User.query.filter_by(username=username).first(): # checks if username already exists in database, first() reyurns the first result or none if none found, saves time
        return jsonify({'errpr': 'Username already exist'}), 409 # if username exists returns the error message and 409 status code
    
    new_user = User(username = username, password= password) # creates a new user instance with the username and password
    db.session.add(new_user) #add the new user to the database session
    db.session.commit()

    return jsonify({'message': "aaccount created'}), 201"})

@routes.route('/login', methods = ['POST']) # route for loggin into an exisitng account
def login():
    data = request.get_json() 
    username = data.get['username'] 
    password = data.get['password'] #this all the same as previous route as it is just reading data from the request

    user = User.query.filter_by(username = username, password = password).first() #checks if the user details inputted macthes one in the database
    if not user:
        return jsonify({'error': 'inavlid username or password'}), 401 
    session['user_id'] = user.id # if user is found then the session will store their ID sp they can be recognised in futrue requests
    return jsonify({'message': 'login succesful'}), 200 

@routes.route('/logout', methods = ['POST']) 
def logout():
    session.pop('user_id', None) # removes user ID form the session, logging them out
    return jsonify({'message': 'logged out'})


@routes.route('/calibrate_data', methods = ['POST'])
def calibrate_data():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorised'}), 401
    
    ata = request.get_json()
    user_id = session['user_id']
    user = User.query.get(user_id) # gets the user data from  the data using their ID stored in the session

    input_data = Data(
        user_id = user.user_id, 
        dateinput = datetime.utcnow(),
        day_1_heart_rate = data.get('day_1_heart_rate'), # gets the heart rate from calibration day 1
        day_2_heart_rate = data.get('day_2_heart_rate'),
        day_3_heart_rate = data.get('day_3_heart_rate'),
        
    
    )
    db.session.add(input_data) 
    db.session.commit()

    return jsonify ({'message':'data submitted successfully'}), 201

@routes.route('/submit_data', methods = ['post'])
def submit_data():
    if 'user_id' not in session: # checks if user is logged and is authorised for this route
        return jsonify ({'error': 'unauthorised'}), 401 
    
    data = request.get_json()
    user_id = session['user_id']
    user = User.query.get(user_id) # gets the user data from  the data using their ID stored in the session

    input_data = Data(
        user_id = user.user_id, #links data to the user
        dateinput = datetime.utcnow(), #sets the date and time inputed to now as the requets is now
        heart_rate = data.get('heart_rate'), # gets the heart rate from the data 
        sleep = data.get('sleep'),
        # mood = data.get('mood'),
        # fatigue = data.get('fatigue')
    


    )  # creates a new data instance with the user ID and the data inputted
    db.session.add(input_data) # adds the new data to the database session

    db.session.commit() 


    score = calculate_score(user_id) # calculates the overtraining score using teh user id and the calculate_scoore fucniton is imported from caluclations.py
    return jsonify({'message': 'data submitted successfully', 'score': score}), 201

routes.route('/score', methods = ['GET'])
def get_score():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorised'}), 401
    user_id = session['user_id']
    user = User.query.get(user_id) 
    if not user:
        return jsonify ({'error': 'user not found'}), 404
    score = calculate_score(user_id)
    return jsonify({'score': score}), 200 # returns the score a a json obect so it can be used in the frontend plus we use status code 200 to indicate usccess

    JWT_SECRET_KEY = os.getenv("JWT_SECRET") # secret key for JWT, used for signing tokens in this case  the token is used ot authenticate users and poretct routs
    SQLALCHEMY_TRACK_MODIFICATIONS= False # disables track modifcation to save memory
    JWT_ACCESS_TOKEN_EXPIRES = 3600 # expires in one hour
    JWT_REFRESH_TOKEN_EXPIRES = 86400 # refresh token expires in one day

    
@routes.route('/history', methods=['GET'])
def get_history():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorised'}), 401
    user_id= session['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404
    data = Data.query.filter_by(user_id = user_id).all()
    history = [{'dateinput': d.dateinput, 'heart_rate': d.heart_rate, 'sleep': d.sleep} for d in data] # retrieves all data for the user and formats it into a list of dictionaries
    return jsonify({'history' : history}), 200


    
