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
    # TODO: Feature 1
    all_events = event_repo.get_all_events_for_table()
    return render_template('list_all_events.html', events=all_events)


'''@app.get('/events/new')
def create_events_form():
    return render_template('create_events_form.html')'''


'''@app.post('/movies')
def create_movie():
    #basic input for events
    Name = request.form.get('name')
    EventName = request.form.get('director')
    Time = request.form.get('time')
    #temp address input
    Address = request.form.get('address')
    
    movie_repository.create_movie(Name, EventName, Time, Address)
    return redirect('/movies')'''



'''@app.get('/events/search')
def search_event():
    #todo
    return render_template('search_event.html', search_active=True)'''

'''@app.get('/')
def index():
    all_images = images_repo.get_all_images()
    return render_template('index.html', images=all_images)'''

'''@app.get('/')
def index():
    all_events = event_repo.get_all_events_for_table()
    print(all_events)
    return render_template('index.html',events=all_events)'''

# THis route was meant to implement the get_event_by_title function from event_repo.py( Single even)
'''@app.get('/event/<str:title>') 
def get_event(title):
    event = event_repo.get_event_by_title(title)
    return render_template('events.html', events=event)
'''

''