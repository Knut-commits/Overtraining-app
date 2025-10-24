from flask import Blueprint, redirect, request, jsonify, session, render_template, request # import neccessary moudles ofr all routes (logging in, submitting data etc)
from datetime import date, datetime
from Backend.extension import db # importing database instance
from Backend.database import Data, User #importing user and data databases
from Backend.calculations import calculate_score # importing the fucntion to calculate the overtrianing scores

routes= Blueprint('routes', __name__) # creating blue prints for the routes, so easier to organise and less redudant code

@routes.route('/')
def index():
    return redirect('/login') # login page will be the first page.


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
        if not getattr(user,'Base_heart_rate',None): #checking if user has calibraiton data
            return redirect('/calibrate_data') #redirects to calibrate data page')
        
        latest = Data.query.filter_by(user_id=user.id).order_by(Data.dateinput.desc()).first()
        if not latest or latest.dateinput.date() < date.today():
            return redirect('/submit_data')
        #chekcing that most recent data entry was today otherwise getting redirecting to submit data
        return redirect('/home')
    
    return render_template('login.html')

@routes.route('/logout', methods = ['POST']) 
def logout():

    session.pop('user_id', None) # removes user ID form the session, logging them out
    return redirect('/login')


@routes.route('/calibrate_data', methods = ['GET','POST'])
def calibrate_data():
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    user = User.query.get(user_id)
    if request.method == 'POST':
        try:
           h1 = float(request.form.get('day1_hr'))
           h2=float(request.form.get('day2_hr'))
           h3=float(request.form.get('day3_hr'))
        except ValueError:
            return render_template('calibrate_data.html')
        
        
        base_heart_rate = (h1 + h2 + h3) /3.0
        user.Base_heart_rate = base_heart_rate
        db.session.commit()

        return redirect('/home')
    
    return render_template('calibrate_data.html')
    

@routes.route('/submit_data', methods = ['GET','POST'])
def submit_data():
    if 'user_id' not in session: # checks if user is logged and is authorised for this route
        return redirect('/login')
    
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        try:    
            heart_rate = float(request.form.get('heart_rate')) 
            sleep = float(request.form.get('sleep')) # gets teh data from the submit data form
        except (TypeError, ValueError, AttributeError):
            return render_template('submit_data.html', error = "invalid input, number only")
        
        base_hr = getattr(user,'Base_heart_rate',None) #getting base heart rate from user table
        
        if base_hr is None:
            return redirect('/calibrate_data')

        input_data = Data(
            user_id = session['user_id'],
            dateinput = datetime.utcnow(), #sets the date and time inputed to now as the requets is now
            Base_heart_rate = base_hr,
            heart_rate = heart_rate,
            sleep = sleep,
            score = calculate_score(heart_rate, sleep, base_hr)[0], #storing just the score value not the descriptor
        # mood = data.get('mood'),
        # fatigue = data.get('fatigue')
    


        )  # creates a new data instance with the user ID and the data inputted
        db.session.add(input_data) # adds the new data to the database session

        db.session.commit() 
        return redirect('/home')
    return render_template('submit_data.html')

def get_recovery_advice(score:float) ->str:
    if score >=7.0:
        return("You are overtrained. Take 1-2 rest days, sleep 8-9 hours. Stay hydrated and only light mobility DISCLAIMER: not a doctor")
    elif score >=4.0:
        return ("Moderate stress, reduce volume by 30-40% or keep intensity low, prioritize 8h sleep, hydration. DISCLAIMER: not a doctor")
    else:
        return("Well recovered,continue training, but keep good habits. Adequate sleep, fueling properly, carbs/protein after sessions. DISCLAIMER: not a doctor ")
    
@routes.route('/home', methods = ['GET'])  
def home():
    if 'user_id' not in session:
        return redirect('/login') #redirect if not logged in
    user_id = session['user_id']
    user = User.query.get(user_id) 
    if not user:
        return redirect('/login') #redirect if user not found
    
    latest = Data.query.filter_by(user_id=user.id).order_by(Data.dateinput.desc()).first()
    if not latest:
        return redirect('/submit_data') #redirect if no data found
    
    calibration = latest.Base_heart_rate
    heart = latest.heart_rate
    sleep = latest.sleep
    score_value, descriptor = calculate_score(heart,sleep,calibration) #splitting the returned tuple into score value and descriptor

    advice = get_recovery_advice(float(score_value)) 

    data = Data.query.filter_by(user_id = user_id).all()
    history = [
        {
            'dateinput': d.dateinput,
            'heart_rate' : d.heart_rate,
            'sleep' : d.sleep,
            'score' : d.score if d.score is not None else "N/A" #only use score if the score is there.
            
        }
        for d in data
    ]

    chart_labels = [d.dateinput.strftime('%Y-%m-%d') for d in data]
    chart_scores = [d.score if d.score is not None else 0 for d in data]
    return render_template('home.html', history = history, score = round(score_value,2),descriptor = descriptor ,advice = advice, chart_labels = chart_labels, chart_scores = chart_scores) 


    
