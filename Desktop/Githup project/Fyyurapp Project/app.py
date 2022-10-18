#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db,Venue,Artist,Shows
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
migrate = Migrate(app, db)
app.config.from_pyfile('config.py')
db.init_app(app)
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
        date = dateutil.parser.parse(value)
  else:
      date = value
  return babel.dates.format_datetime(date, format, locale='en')
app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  venu_data= []
  Ven = Venue.query.distinct(Venue.city, Venue.state).all()
  for row in Ven:
    vn = Venue.query.filter(Venue.city == row.city, Venue.state == row.state).all()
    for row1 in vn:
      venu_data += [{
        "id": row1.id,
        "name": row1.name,
      }]
    data +=[{
    "city": row.city,
    "state": row.state,
    "venues": venu_data
    }]
    venu_data=[]
  return render_template('pages/venues.html', areas=data)

#------------------------------------------------
# Search Venues
#-----------------------------------------------------------------

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_value = request.form['search_term']
  query1 =  db.session.query(Venue).filter(Venue.name.ilike(f'%{search_value}%')).all()
  if query1:
    data_values = []
    for qry in query1:
      data_values.append({
      "id": qry.id,
      "name": qry.name,
      })
    response={
      "count": len(search_value),
      "data": data_values
    }
  else:
    response={}
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))
#-----------------------------------------------------
#   Show a particular Venue
#----------------------------------------------------
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  query_result1 = Venue.query.filter(Venue.id == venue_id).first()
  
  past = db.session.query(Artist, Shows).join(Shows).filter(Shows.venue_id==query_result1.id, Shows.start_time<=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).all()
  past_shows = []
    
  if past:
      for item, sh in past:
        past_shows.append({
          "artist_id": item.id,
          "artist_name": item.name,
          "artist_image_link": item.image_link,
          "start_time": sh.start_time,
        })
  
  upcoming = db.session.query(Artist, Shows).join(Shows).filter(Shows.venue_id==query_result1.id, Shows.start_time>=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).all()
  upcoming_shows = []
    
  if upcoming:
      for artist_row, show in upcoming:
        upcoming_shows.append({
          "artist_id": artist_row.id,
          "artist_name": artist_row.name,
          "artist_image_link": artist_row.image_link,
          "start_time": show.start_time,
        })
  data={
    "id": query_result1.id,
    "name": query_result1.name,
    "genres": [query_result1.genres],
    "address": query_result1.address,
    "city": query_result1.city,
    "state": query_result1.state,
    "phone": query_result1.phone,
    "website": query_result1.website_link,
    "facebook_link": query_result1.facebook_link,
    "seeking_talent": query_result1.seeking_talent,
    "seeking_description": query_result1.seeking_description,
    "image_link": query_result1.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = request.form
  try:
     new_venue = Venue(
       name =  form['name'],
      city =  form['city'],
      state =  form['state'],
      address = form['address'],
      phone =  form['phone'],
      image_link = form['image_link'],
      genres =   form.getlist('genres'),
      facebook_link =  form['facebook_link'],
      website_link =  form['website_link'],
      seeking_talent =  bool(form.get('seeking_talent')),
      seeking_description = form["seeking_description"]
    )
     db.session.add(new_venue)
     db.session.commit()
     flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
        print(sys.exc_info())
        flash('Venue ' + request.form['name'] + ' Failure!! to create venue')
        db.session.rollback()
  finally:
      db.session.close()
      return render_template('pages/home.html')
    
#-------------------------------
#     Delete Venue

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    venue =  Venue.query.filter_by(id=venue_id)
    db.session.delete(venue)
    db.session.Commit()
    flash('Your Venue has been deleted' +  ' Success')
  except:
     flash('Your Venue has  not been deleted')
    
  finally:
    
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return render_template('pages/home.html')

  
  
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data= db.session.query(Artist.id, Artist.name).all()
  return render_template('pages/artists.html', artists=data)


#### Search for artist
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_value = request.form['search_term']
  query1 =  db.session.query(Artist).filter(Artist.name.ilike(f'%{search_value}%')).all()
  if query1:
    data_values = []
    for qry in query1:
      data_values +=[{
      "id": qry.id,
      "name": qry.name,
      }]
    response={
      "count": len(search_value),
      "data": data_values
    }
  else:
    response={}
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
##---------------------------------------------
# show a particular Artist

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  query_result = Artist.query.filter(Artist.id == artist_id).first()

  query_result1 = db.session.query(Artist, Shows).join(Shows).filter(Shows.artist_id==query_result.id, Shows.start_time<=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).all()
  past_shows = []
    
  if query_result1:
      for artist_row, show in query_result1:
        past_shows.append({
          "artist_id": artist_row.id,
          "artist_name": artist_row.name,
          "artist_image_link": artist_row.image_link,
          "start_time": show.start_time,
        })
  
  query_upcoming = db.session.query(Artist, Shows).join(Shows).filter(Shows.artist_id==query_result.id, Shows.start_time>=datetime.now().strftime("%Y-%m-%d %H:%M:%S")).all()
  upcoming_shows = []
    
  if query_upcoming:
      for artist_row, show in query_upcoming:
        upcoming_shows.append({
          "artist_id": artist_row.id,
          "artist_name": artist_row.name,
          "artist_image_link": artist_row.image_link,
          "start_time": show.start_time,
        })
  data={
    "id": query_result.id,
    "name": query_result.name,
    "genres": [query_result.genres],
    "city": query_result.city,
    "state": query_result.state,
    "phone": query_result.phone,
    "website": query_result.website_link,
    "facebook_link": query_result.facebook_link,
    "seeking_venue": query_result.seeking_venue,
    "seeking_description": query_result.seeking_description,
    "image_link": query_result.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist=Artist.query.filter(Artist.id==artist_id).first()
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist=Artist.query.get(artist_id)
  form = request.form
  try:
    
       artist.name = form['name']
       artist.city = form['city']
       artist.state = form['state'] 
       artist.phone = form['phone'] 
       artist.image_link = form['image_link'] 
       artist.genres = form.getlist('genres')
       artist.facebook_link = form['facebook_link'] 
       artist.website_link = form['website_link'] 
       artist.seeking_venue = bool(form.get('seeking_venue')) 
       artist.seeking_description= form["seeking_description"] 
       
       db.session.commit()
       flash('Artist ' + request.form['name'] + ' was successfully updated!')
  except:
        print(sys.exc_info())
        flash('Artist ' + request.form['name'] + ' Failure!! to update Arttist')
        db.session.rollback()
  finally:
      db.session.close()
      return redirect(url_for('show_artist', artist_id=artist_id))
  
  
#Udate Venue
#----------------------------------------------------------------------------
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter(Venue.id==venue_id).first()
   
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)
  form = request.form
  try:
     
       venue.name = form['name'] 
       venue.city = form['city'] 
       venue.state = form['state'] 
       venue.address = form['address'] 
       venue.phone = form['phone'] 
       venue.image_link = form['image_link'] 
       venue.genres =  form.getlist('genres')
       venue.facebook_link = form['facebook_link'] 
       venue.website_link = form['website_link'] 
       venue.seeking_talent = bool(form.get('seeking_talent'))
       venue.seeking_description = form["seeking_description"] 
    
       db.session.commit()
       flash('Venue '  + ' was successfully updated!')
  except:
        print(sys.exc_info())
        flash('Venue ' +' Failure!! to update venue')
        db.session.rollback()
  finally:
      db.session.close()
      return redirect(url_for('show_venue', venue_id=venue_id))
    
  

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form= ArtistForm()
  form = request.form
  try:
     add_artist = Artist(
      name =  form['name'],
      city =  form['city'],
      state =  form['state'],
      phone =  form['phone'],
      image_link = form['image_link'],
      genres =   form.getlist('genres'),
      facebook_link =  form['facebook_link'],
      website_link =  form['website_link'],
      seeking_venue  =  bool(form.get('seeking_venue')),
      seeking_description = form["seeking_description"]
    )
     db.session.add(add_artist)
     db.session.commit()
     flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
        print(sys.exc_info())
        flash('Artist ' + request.form['name'] + ' Failure!! to create Arttist')
        db.session.rollback()
  finally:
      db.session.close()
      return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  result = db.session.query(Venue, Shows, Artist).select_from(Venue).join(Shows).join(Artist).all()

  data = []
  for venue, shows, artist in result: 
    data +=[{
    "venue_id": venue.id,
    "venue_name": venue.name,
    "artist_id": artist.id,
    "artist_name": artist.name,
    "artist_image_link": artist.image_link,
    "start_time": shows.start_time
  }]
    
 
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = request.form
  try:
     add_show = Shows(
      artist_id =  form['artist_id'],
      venue_id =  form['venue_id'],
      start_time =  form['start_time']
      
    )
     
     db.session.add(add_show)
     db.session.commit()
     flash('Show ' + ' was successfully listed!')
  except:
        print(sys.exc_info())
        flash('Show ' +' Failure!! to create venue')
        db.session.rollback()
  finally:
      db.session.close()
      return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
