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
        f"/api/v1.0/<start> (**DO NOT COPY THIS SECTION** Enter date in the format: YYYY-MM-DD)<br/>"
        f"/api/v1.0/<start>/<end> (**DO NOT COPY THIS SECTION** Enter date in the format: YYYY-MM-DD)<br/>")

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
    print("Server received request for 'Temperature (tobs)' page...")
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

# Create the Start Date Flask route
@app.route("/api/v1.0/<start>")
def temp_start(start):
    print("Server received request for the 'Start Date' page...")
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start range.
    session = Session(engine)
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    start_date_query = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    
    start_date_list = [start_date_query[0][0], start_date_query[0][1], round(start_date_query[0][2],2)]
    
    return jsonify(start_date_list)

# Create the Start and End Date Flask route
@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    print("Server received request for the 'Start and End Date' page...")
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start and end range.
    session = Session(engine)
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    start_end_query = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date, measurement.date <= end_date).all()
    
    start_end_list = [start_end_query[0][0], start_end_query[0][1], round(start_end_query[0][2],2)]
    
    return jsonify(start_end_list)

if __name__ == "__main__":
    app.run(debug=True)
