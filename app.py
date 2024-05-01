from flask import Flask, abort, redirect, render_template, request, session
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from datetime import datetime
import os
import googlemaps
from repositories import event_repo, user_repository

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET_KEY')

gmaps = googlemaps.Client(key='AIzaSyDUNewuSDlRLem-I3kcBnvU6467VleNicM')


@app.get('/')
def index():
    if 'user_id' in session:
        return redirect('/listevents')
    else:
        return render_template('index.html')


@app.get('/events')
def list_all_events():
    # TODO: Feature 1
    all_events = event_repo.get_all_events_for_table()
    return render_template('list_all_events.html', events=all_events)

@app.get('/events/<int:event_id>')
def get_event(event_id):
    event = event_repo.get_event_by_id(event_id)
    return render_template('get_single_event.html', event=event)

#@app.get('/events/newmap')
#def new_eventmap():
    return render_template('googlemaps_input.html')

#@app.post('/events')
#def create_event_map():
    user_address = request.form['address']
    event_address = gmaps.geocode(user_address)

    #if not event_address:
     #   return 'Bad Request', 400
    # More tests to be added
    event_repo.create_event(event_address)
    return redirect('/events/new')

@app.get('/events/new')
def new_event():
    return render_template('create_event.html')

@app.post('/events/new')
def create_event():
    host_id = request.form['host_id']
    event_name = request.form['event_name']
    event_description = request.form['event_description']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    user_address = request.form['user_address']
    event_address = gmaps.geocode(user_address)
    
    #if not host_id or not event_name or not event_description or not start_time or not end_time:
     #   return 'Bad Request', 400
    # More tests to be added
    
    event_repo.create_event(host_id, event_name, event_description, start_time, end_time, event_address)
    return redirect('/events')


#@app.post('/signup')
#def signup():
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

#@app.post('/login')
#def login():
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

#@app.post('/logout')
#def logout():
    del session['user_id']
    return redirect('/')