from flask import Flask, redirect, render_template, request


app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')


@app.get('/events')
def list_all_events():
    # TODO: Feature 1
    return render_template('list_all_events.html', list_events_active=True, event_list = list_all_events.get_all_events())


@app.get('/events/new')
def create_events_form():
    return render_template('create_events_form.html')


@app.post('/movies')
def create_movie():
    #basic input for events
    Name = request.form.get('name')
    EventName = request.form.get('director')
    Time = request.form.get('time')
    #temp address input
    Address = request.form.get('address')
    
    movie_repository.create_movie(Name, EventName, Time, Address)
    return redirect('/movies')



@app.get('/events/search')
def search_event():
    #todo
    return render_template('search_event.html', search_active=True)

