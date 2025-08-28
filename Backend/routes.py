from flask import Blueprint, redirect, request, jsonify, session, render_template, request # import neccessary moudles ofr all routes (logging in, submitting data etc)
from datetime import datetime
from Backend.extension import db # importing database instance
from Backend.database import User, data #importing user and data databases
from Backend.calculations import calculate_score # importing the fucntion to calculate the overtrianing scores

routes= Blueprint('routes', __name__) # creating blue prints for the routes, so easier to organise and less redudant code

@routes.route('/')
def index():
    return render_template('register.html') # renders the first page which is the register page.


@routes.route('/register', methods = ['GET','POST']) # route for signing up a new account
def register():
    
    if request.method == 'POST':  #checking that reuqest method is post so data is being sent to server
      username = request.form['username']  # gets user name + password from the form data from frontend
      password = request.form['password']

      if User.query.filter_by(username=username).first(): #checks if username is taken
        return render_template('register.html', error="Username already exists")

      new_user = User(username=username, password=password)
      db.session.add(new_user)
      db.session.commit()  # commits and created a new user in the database

      return redirect('/login') # redirets to login page after registering.

    return render_template('register.html') # renders the register page


@routes.route('/login', methods = ['GET','POST']) # route for loggin into an exisitng account
def login():
    
    if request.method == 'POST':
        username = request.form['username'] 
        password = request.form['password'] #this all the same as previous route as it is just reading data from the form

        user = User.query.filter_by(username = username, password = password).first() #checks if the user details inputted macthes one in the database
        if not user:
            return render_template('login.html', error="Invalid username or password")
        session['user_id'] = user.id # if user is found then the session will store their ID sp they can be recognised in futrue requests
        return render_template('home.html') # redirects to home page 
    return render_template('login.html')

@routes.route('/logout', methods = ['POST']) 
def logout():

    session.pop('user_id', None) # removes user ID form the session, logging them out
    return redirect('/login')


@routes.route('/calibrate_data', methods = ['POST'])
def calibrate_data():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        user_id = session['user_id']
        user = User.query.get(user_id)

        input_data = data(
            user_id=user.id,
            dateinput=datetime.utcnow(),
            day_1_heart_rate=request.form.get('day_1_heart_rate'),
            day_2_heart_rate=request.form.get('day_2_heart_rate'),
            day_3_heart_rate=request.form.get('day_3_heart_rate'),
            day_1_sleep=request.form.get('day_1_sleep'),
            day_2_sleep=request.form.get('day_2_sleep'),
            day_3_sleep=request.form.get('day_3_sleep')
        )

        db.session.add(input_data)
        db.session.commit()

    return redirect('/home')
    
    
    
# need to chnage rest from json to form data
@routes.route('/submit_data', methods = ['POST'])
def submit_data():
    if 'user_id' not in session: # checks if user is logged and is authorised for this route
        return redirect('/login')
    
    heart_rate = request.form('heart_rate') 
    sleep = request.form('sleep') # gets teh data from the submit data form

    input_data = data(
        user_id = session['user_id'],
        dateinput = datetime.utcnow(), #sets the date and time inputed to now as the requets is now
        heart_rate = heart_rate,
        sleep = sleep
        # mood = data.get('mood'),
        # fatigue = data.get('fatigue')
    


    )  # creates a new data instance with the user ID and the data inputted
    db.session.add(input_data) # adds the new data to the database session

    db.session.commit() 


    score = calculate_score(session['user_id']) #alng teh user id and the calculate_scoore fucniton is imported from caluclations.py
    return render_template('home.html', score = score) 

routes.route('/home', methods = ['GET'])  
def home():
    if 'user_id' not in session:
        return redirect('/Login') #redirect if not logged in
    user_id = session['user_id']
    user = User.query.get(user_id) 
    if not user:
        return redirect('/login') #redirect if user not found
    score = calculate_score(user_id)

    data = data.query.filter_by(user_id = user_id).all()
    history = [
        {
            'dateinput': d.dateinput,
            'heart_rate' : d.heart_rate,
            'sleep' : d.sleep
            
        }
        for d in data
    ]
    return render_template('home.html', history = history, score = score)


    
