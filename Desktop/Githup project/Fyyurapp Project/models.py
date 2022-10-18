from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from sqlalchemy_utils import PhoneNumberType


class Shows(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
  venue_id = db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'),primary_key=True)
  artist_id = db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'),primary_key=True)
  start_time =db.Column(db.DateTime, nullable=False)   


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(PhoneNumberType())
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres =db.Column(db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean)
    seeking_description =db.Column(db.String())
    shows = db.relationship('Shows', backref='showing', lazy=True)
   # venues = db.relationship('Show', backref='venue', lazy=False)
   # artists = db.relationship('Artist', backref='artists',lazy=True)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(PhoneNumberType())
    genres =db.Column(db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String())
    seeking_venue = db.Column(db.Boolean)
    seeking_description =db.Column(db.String())
    shows = db.relationship('Shows', backref='show', lazy=True)
   # artists = db.relationship('Show', backref='artist', lazy=False)
   # venues = db.relationship('Venue',backref='venues', lazy=True)
    #venue_id = db.Column(db.Integer,db.ForeignKey('venues.id'))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate