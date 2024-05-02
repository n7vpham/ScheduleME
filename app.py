from flask import Flask, abort, redirect, render_template, request, session
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import os
import googlemaps
from repositories import event_repo, user_repository

load_dotenv()

app = Flask(__name__)

bcrypt = Bcrypt(app) 

app.secret_key = os.getenv('APP_SECRET_KEY')

gmaps = googlemaps.Client(key='AIzaSyDUNewuSDlRLem-I3kcBnvU6467VleNicM')


@app.get('/')
def index():
    if 'user_id' in session:
        return render_template('logged_index.html')
    else:
        return render_template('index.html')


@app.get('/events')
def list_all_events():
    # TODO: Feature 1
    all_events = event_repo.get_all_events_for_table()
    return render_template('list_all_events.html', events=all_events )

@app.get('/events/<int:event_id>')
def get_event(event_id):
    event = event_repo.get_event_by_id(event_id)
    return render_template('get_single_event.html', event=event)

@app.get('/events/new')
def new_event():
    if 'user_id' in session:
        return render_template('create_event.html')
    else:
        return render_template('index.html')

@app.post('/events')
def create_event():
    if 'user_id' in session:
        host_id = session['user_id']
        event_name = request.form['event_name']
        event_description = request.form['event_description']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        user_address = request.form['user_address']
        geocode_result = gmaps.geocode(user_address)
        event_address_pre = geocode_result[0]["place_id"]

        rev_geocode_result = gmaps.reverse_geocode(event_address_pre)
        event_address = rev_geocode_result[0]["formatted_address"]
        
        if not host_id or not event_name or not event_description or not start_time or not end_time:
            return 'Bad Request', 400
        # More tests to be added
        
        event_repo.create_event(host_id, event_name, event_description, start_time, end_time, event_address)
        return redirect('/events')
    else:
        return render_template('index.html')

@app.get('/users') # /secret, render secret.html in video
def new_user():
    return render_template('user_registration.html')

@app.post('/users') # /signup, redirect to secret in video
def register():
    user_fname = request.form['user_fname']
    user_lname = request.form['user_lname']
    user_email = request.form['user_email']
    user_password = request.form['user_password']
    if not user_fname or not user_lname or not user_email or not user_password:
        abort(400)
    does_user_email_exist = user_repository.does_user_email_exist(user_email)
    
    if  does_user_email_exist:
        return redirect('/')
    hashed_password = bcrypt.generate_password_hash(user_password).decode('utf-8')
    user_repository.create_user(user_fname, user_lname, user_email, hashed_password)
    return redirect('/login')

@app.get('/login')
def nav_login():
    return render_template('login.html')
    
@app.post('/login')
def login():
    user_email = request.form.get('user_email')
    user_password = request.form.get('user_password')
    if not user_email or not user_password:
        abort(400)
    user = user_repository.get_user_by_user_email(user_email)
    if user is None:
        abort(401)
    if not bcrypt.check_password_hash(user['hashed_password'], user_password):
        abort(401)
    session['user_id'] = user['user_id']
    return redirect('/profile')

@app.post('/logout')
def logout():
    del session['user_id']
    return redirect('/')

#edit events

#edit individual event items
@app.get('/events/<int:event_id>/edit')
def get_edit_events_page(event_id: int):
    event = event_repo.get_event_by_id(event_id)
    if not event:
        return 'Event not found', 404
    
    # Fetch event details from the database
    event_name = event['event_name']
    event_description = event['event_description']
    start_time = event['start_time']
    end_time = event['end_time']
    event_address = event['event_address']
    
    return render_template('edit_event.html', event=event)

#redirects to single event page for editing
@app.post('/events/<int:event_id>')
def update_event(event_id: int):
    event = event_repo.get_event_by_id(event_id)
    if not event:
        return 'Event not found', 404

    # Fetch updated event details from the form
    event_name = request.form['event_name']
    event_description = request.form['event_description']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    event_address = request.form['event_address']
    
    # Update the event in the database
    event_repo.update_eventName(event_name, event_id)
    event_repo.update_eventDescription(event_description, event_id)
    event_repo.update_eventStartTime(start_time, event_id)
    event_repo.update_eventEndTime(end_time, event_id)
    event_repo.update_eventAddress(event_address, event_id)

    # Redirect to the event details page
    return redirect(f'/events/{event_id}')


#delete whole event
@app.post('/events/<int:event_id>/delete')
def delete_event(event_id: int):
    event = event_repo.get_event_by_id(event_id)
    if not event:
        return 'Event not found', 404
    event_repo.delete_event(event_id)
    print("Event has been deleted. Redirecting...")
    return redirect('/profile/events')

#Nam nam nam
@app.get('/profile')
def get_user():
    if 'user_id' in session:
        user = user_repository.get_user_by_id(session['user_id'])
        return render_template('get_single_user.html', user=user)        
    else:
        return render_template('index.html')  

@app.get('/profile/events')
def list_all_user_events():
    if 'user_id' in session:
        all_events = event_repo.get_all_events_by_user_id(session['user_id'])
        return render_template('list_all_user_events.html', events=all_events)
    else:
        return render_template('index.html')

