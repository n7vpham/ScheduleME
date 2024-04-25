import os
from flask import Flask, abort, redirect, render_template, request, session
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from repositories import user_repository
from datetime import datetime
import googlemaps



load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET_KEY')

bcrypt = Bcrypt(app)

gmaps = googlemaps.Client(key='APP_SECRET_KEY')


@app.get('/')
def index():
    if 'user_id' in session:
        return redirect('/listevents')
    return render_template('index.html')

@app.get('/listevents')
def list_all_events():
   if 'user_id' not in session:
               return redirect('/')
    user_id = session.get('user_id')
    user = user_repository.get_user_by_id(user_id)  # type: ignore
    return render_template('list_all_events.html', list_events_active=True, event_list = list_all_events.get_all_events())


@app.get('/createevents')
def create_events_form():
        #basic input for events
    Name = request.form.get('user_name', type=str)
    EventName = request.form.get('eventname', type=str)
    Time_start = request.form.get('time1', type=datetime)
    Time_end = request.form.get('time2', type=datetime)
    Date = request.form.get('date', type=str)
    #address input
    geocode_result = gmaps.geocode('address')


    
    create_events_form(Name, EventName, Time_start, Time_end, geocode_result)

    return render_template('create_events_form.html')

@app.post('/signup')
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        abort(400)
    does_user_exist = user_repository.does_username_exist(username)
    if does_user_exist:
        abort(400)
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_repository.create_user(username, hashed_password)
    return redirect('/')

@app.post('/login')
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        abort(400)
    user = user_repository.get_user_by_username(username)
    if user is None:
        abort(401)
    if not bcrypt.check_password_hash(user['hashed_password'], password):
        abort(401)
    session['user_id'] = user['user_id']
    return redirect('/listevents')

@app.post('/logout')
def logout():
    del session['user_id']
    return redirect('/')
