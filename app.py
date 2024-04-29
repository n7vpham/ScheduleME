from flask import Flask, redirect, render_template, request
from dotenv import load_dotenv

from repositories import event_repo

load_dotenv()

app = Flask(__name__)

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

@app.get('/events/<int:event_id>/edit')
def get_edit_events_page(event_id: int):
    return render_template('edit_event.html')


@app.post('/events/<int:event_id>')
def update_event(event_id: int):
    return redirect(f'/events/{event_id}')


@app.post('/events/<int:event_id>/delete')
def delete_event(event_id: int):
    return redirect(f'/events')