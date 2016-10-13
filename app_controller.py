import os, random, string, json, requests, httplib2, config, datetime, HTMLParser
from flask import Flask, render_template, make_response, request, redirect, jsonify, url_for, flash, send_from_directory, g
from flask import session as login_session
from flask import session as login_session
from flask_jsglue import JSGlue
from flask.ext import assets
from flask_assets import Environment, Bundle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Event
import re, htmlentitydefs
from geopy.geocoders import Nominatim


app = Flask(__name__)
jsglue = JSGlue(app)
assets = Environment(app)

#configurations
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY

# Tell flask-assets where to look for our sass file.
cs = Bundle(
        'style/sass/all.sass',
        filters='sass',
        output='style/main.css'
    )
assets.register('css_all', cs)

#Database Binding
engine = create_engine(config.DATABASE_URI)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Route Binding
def verifyCaptcha(response_from_google, remote_addr):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    params = {"secret": "6Lc4SCkTAAAAAKS7xU7K53IbPwI1BC2dv0RUqJk2", "response": response_from_google, "remoteip": remote_addr}
    return requests.post(url, params=params)
    
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

@app.route("/")
def home():
    events = session.query(Event).all()
    resp = make_response(render_template('index.html', events = events))
    return resp

@app.route("/admin/")
def admin():
    events = session.query(Event).all()
    resp = make_response(render_template('admin.html', events = events))
    return resp

@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
        flash(u'You Have Been Logged In')
    else:
        resp = make_response(render_template('login.html'))
        return resp

@app.route("/json/events", methods=['GET'])
def json_events():
    events = session.query(Event).all()
    return jsonify(json_list=[i.serialize for i in events]), 200

@app.route("/create/", methods=['GET', 'POST'])
def createEvent():
    if request.method == 'POST':
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr
        if verifyCaptcha(request.form['g-recaptcha-response'], ip).status_code != 200:
            flash(u'You Are Not A Human. Gain A Corpeal Form And Try Again')
            redirect(url_for('home'))
        event_type = request.form['event_type']

        title = request.form['title']
        description = request.form['description']
        print 'b'
        signup_email = request.form['signup_email']
        
        signup_email = True if signup_email == 'on' else False
        reminder_email = request.form['reminder_email']
        reminder_email = True if reminder_email == 'Yes' else False
        reminder_time = request.form['reminder_time']
        country = request.form['country']
        address1 = request.form['address1']
        address2 = request.form['address2']
        city = request.form['city']
        state = request.form['state']

        zipCode = request.form['zipCode']
        venue = request.form['venue']
        capacity = request.form['capacity']
        directions = request.form['directions']
        date =  request.form['date']
        date =   date.split('-')
        time_hour =  int(request.form['time_hour'])
        time_minutes =  request.form['time_minutes']
        time_day =  request.form['time_day']
        if time_day == 'pm':
            time_hour += 12 
        event_time = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time_hour), int(time_minutes), 0)
        length =  request.form['length']
        length_unit =  request.form['length_unit']
        phone  =  request.form['phone']
        public_phone  =  request.form['public_phone']
        host  =  request.form['host']
        email =  request.form['email']
        loc = address1 + " " + address2 + " " + city + ", " + state + " " + zipCode
        print loc
        geolocator = Nominatim()
        location = geolocator.geocode(loc)
        print(location.address)
        print((location.latitude, location.longitude))
        lat = location.latitude
        lng = location.longitude
        newEvent = Event(event_type=event_type, title=title, description= description, signup_email=signup_email, reminder_email=reminder_email, reminder_time=reminder_time, country=country, address1=address1, address2=address2, city=city, state=state, zipCode=zipCode, venue=venue, capacity=capacity, directions=directions, event_time = event_time, length=length, length_unit=length_unit, phone=phone, public_phone=public_phone, host=host, email=email, lat = lat, lng =lng)
        session.add(newEvent)
        session.commit()
        flash(u'You Have Created a New Event')
        return redirect(url_for('home'))
    else:
        resp = make_response(render_template('event.html', captcha=True))
        return resp

@app.route("/read/<int:event_id>/")
def readEvent(event_id):
    event = session.query(Event).filter_by(id = event_id).one()
    resp = make_response(render_template('event_detail.html', event=event))
    return resp

@app.route("/update/<int:event_id>/", methods=['GET','PUT'])
def updateEvent(event_id):
    event = session.query(Event).filter_by(id = event_id).one()
    if request.method == 'PUT':
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr
        if verifyCaptcha(request.form['g-recaptcha-response'], ip).status_code != 200:
            flash(u'You Are Not A Human. Gain A Corpeal Form And Try Again')
            redirect(url_for('home'))
        event.event_type = request.form['event_type']
        event.title = request.form['event_title']
        event.description = request.form['event_description']
        event.signup_email = request.form['event_email_signup']
        event.reminder_email = request.form['event_email_reminder']
        event.reminder_time = request.form['reminder_time']
        event.country = request.form['country']
        event.address1 = request.form['address1']
        event.address2 = request.form['address2']
        event.city = request.form['city']
        event.state = request.form['state']
        event.zipCode = request.form['zipCode']
        event.venue = request.form['venue']
        event.capacity = request.form['capacity']
        event.directions = request.form['directions']
        event.timezone = request.form['timezone']
        event.date =  request.form['date']
        event.time_hour =  request.form['time_hour']
        event.time_minutes =  request.form['time_minutes']
        event.time_day =  request.form['time_day']
        event.length =  request.form['length']
        event.length_unit =  request.form['length_unit']
        event.phone  =  request.form['phone']
        event.phone_public  =  request.form['phone_public']
        event.host  =  request.form['host']
        event.email =  request.form['email']
        flash(u'You Have Updated a New Event')
    else:
        resp = make_response(render_template('updateEvent.html', event=event, captcha = True))
        return resp

@app.route("/delete/<int:event_id>/", methods=['DELETE'])
def deleteEvent(event_id):
    event = session.query(Event).filter_by(id = event_id).one()
    session.delete(event)
    session.commit()
    flash(u'You Have Deleted a New Event')
    redirect(url_for('home'))
    return request.headers.get('referer')

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('404.html')), 404
    return resp

#Main Function
if __name__ == "__main__":
	app.debug = True
	app.run(host= '0.0.0.0', port=5001)