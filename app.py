# Import Dependencies
import pandas as pd
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# Import Flask
from flask import Flask, jsonify

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Create the HomePage Flask route
@app.route("/")
def home():
    print("Server received request for 'Home' Page...")
    return (
        f"Welcome to the Home Page for the Measurement and Station Data API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>")

# Create the Precipitation Flask route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitaion' page...")
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    session = Session(engine)
    precipitation = session.query(measurement.date, measurement.prcp).all()
    session.close()

    precipitation_dict = {}
    for x in precipitation:
        precipitation_dict[x[0]]= x[1]

    # Return the JSON representation of your dictionary.
    return jsonify (precipitation_dict)

# Create the Stations Flask route
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    # Return a JSON list of stations from the dataset.
    session = Session(engine)
    stations = session.query(station.station).all()
    session.close()

    stations_list = []
    for x in stations:
        stations_list.append(x[0])
    
    return jsonify(stations_list)

# Create the Tobs Flask route
@app.route("/api/v1.0/tobs")
def tobs():
   # Query the dates and temperature observations of the most active station for the previous year of data.
   session = Session(engine)
   temp_query = session.query(measurement.date, measurement.station, measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= '2016-08-23', measurement.date <='2017-08-23').\
    order_by(measurement.date).all()
   session.close()
   
   tobs_list = []
   for x in temp_query:
       tobs_list.append(x[2])
       
   # Return a JSON list of temperature observations (TOBS) for the previous year. 
   return jsonify(tobs_list)

if __name__ == "__main__":
    app.run(debug=True)
