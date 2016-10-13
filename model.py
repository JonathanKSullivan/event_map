import os, sys, datetime, config
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()
DATABASE_URI =  config.DATABASE_URI

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    event_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    signup_email = Column(Boolean, nullable=False)
    reminder_email = Column(Boolean, nullable=False)
    reminder_time = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    address1 = Column(String, nullable=False)
    address2 = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zipCode = Column(String, nullable=True)
    venue = Column(String, nullable=True)
    capacity = Column(Integer, nullable=True)
    directions = Column(String, nullable=True)
    length = Column(Integer, nullable=True)
    length_unit = Column(String, nullable=True)
    phone = Column(Integer, nullable=True)
    public_phone = Column(Boolean, nullable=True)
    host = Column(String, nullable=True)
    email = Column(String, nullable=True)
    event_time = Column(DateTime(timezone=False), nullable=False)
    lat =  Column(Float, nullable=False)
    lng =  Column(Float, nullable=False)
    creation_date = Column(DateTime(timezone=True), nullable=False)

    def __init__(self, event_type, title, description, signup_email, reminder_email, reminder_time, country, address1, address2, city, state, zipCode, venue, capacity, directions, event_time, length, length_unit, phone, public_phone, host, email, lat, lng):
        self.event_type = event_type
        self.title = title
        self.description = description
        self.signup_email = signup_email
        self.reminder_email = reminder_email
        self.reminder_time = reminder_time
        self.country = country
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.venue = venue
        self.capacity = capacity
        self.directions = directions
        self.event_time = event_time
        self.length = length
        self.length_unit = length_unit
        self.phone = phone
        self.public_phone = public_phone
        self.host = host
        self.email = email
        self.lat = lat
        self.lng = lng
        self.creation_date = datetime.datetime.today()

    def __repr__(self):
        return '<Event %r>' % self.title

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'event_type': self.event_type,
            'title': self.title,
            'description': self.description,
            'signup_email': self.signup_email,
            'reminder_email': self.reminder_email,
            'reminder_time': self.reminder_time,
            'country': self.country,
            'address1': self.address1,
            'address2': self.address2,
            'city': self.city,
            'state': self.state,
            'zipCode': self.zipCode,
            'venue': self.venue,
            'capacity': self.capacity,
            'directions': self.directions,
            'event_time': self.event_time,
            'length': self.length,
            'length_unit': self.length_unit,
            'phone': self.phone,
            'public_phone': self.public_phone,
            'host': self.host,
            'email': self.email,
            'lat': self.lat,
            'lng': self.lng,
            'creation_date': self.creation_date
        }

def create_app():
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)

def db():
    engine = create_engine(DATABASE_URI)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    db = DBSession()
    return db

#Main Function
if __name__ == "__main__":
    create_app()