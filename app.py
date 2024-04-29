from flask import Flask, redirect, render_template, request, abort
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

from repositories import event_repo, user_repository
from flask import abort

load_dotenv()

app = Flask(__name__)

bcrypt = Bcrypt(app)

@app.get('/')
def index():
    return render_template('index.html')


@app.get('/events')
def list_all_events():
    all_events = event_repo.get_all_events_for_table()
    return render_template('list_all_events.html', events=all_events)

@app.get('/events/<int:event_id>')
def get_event(event_id):
    event = event_repo.get_event_by_id(event_id)
    return render_template('get_single_event.html', event=event)

@app.get('/events/new')
def new_event():
    return render_template('create_event.html')

@app.post('/events')
def create_event():
    host_id = request.form['host_id']
    event_name = request.form['event_name']
    event_description = request.form['event_description']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    event_address = request.form['event_address']
    if not host_id or not event_name or not event_description or not start_time or not end_time or not event_address:
        return 'Bad Request', 400
    # More tests to be added
    
    event_repo.create_event(host_id, event_name, event_description, start_time, end_time, event_address)
    return redirect('/events')

@app.get('/users')
def new_user():
    return render_template('user_registration.html')

@app.post('/users')
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
    return redirect('/users')

    
    
