# import dependencies 
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session 
session = Session(engine)

###################################
#  Flask Setup
###################################
app = Flask(__name__)

###################################
#Flask Routes
###################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- 12 month look back of precipitation totals from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of Station Names and Numbers <br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- 12 month look back of observed temperatures from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/<start><br/>"
        f"- Calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date (8/23/16)<br/>"
        f"<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"- Calculate the MIN/AVG/MAX temperature for dates between the start and end date (8/23/16 -8/23/17) <br/>"
    )

####################################

@app.route("/api/v1.0/precipitation")
def precipitation():
# Query the last 12 months of precipitation 
#  Convert the query results to a Dict
#  Return the json representation of your dictionary.
    precip_last_year = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date).all()

# Create a list of dicts with `date` and `prcp` as the keys and values
    precipitation = []
    for result in precip_last_year:
        row = {}
        row["date"] = precip_last_year[0]
        row["prcp"] = precip_last_year[1]
        precipitation.append(row)
    return jsonify(precipitation)

###################################
@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(Station.name, Station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    return jsonify(stations.to_dict())

###################################
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperatures for prior year"""
# Query last 12 months of temperature observations 
# Convert the query results to a Dictionary 
# Return the json representation of your dictionary.
    temperature = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date).all()

# Create a list of dicts with `date` and `tobs` as the keys and values
    temp_totals = []
    for result in temperature:
        row = {}
        row["date"] = temperature[0]
        row["tobs"] = temperature[1]
        temp_totals.append(row)
    return jsonify(temp_totals)

#####################################

@app.route("/api/v1.0/<start>")
def date1(start):
 # Min/Avg/Max temp   
    start = dt.date(2016, 8, 23)
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    trip = list(np.ravel(temp_data))
    return jsonify(trip)

####################################

@app.route("/api/v1.0/<start>/<end>")
def date2(start,end):
  # Min/Avg/Max temp     
    start = dt.date(2016, 8, 23)
    end = dt.date(2016, 8 ,23)
    temp_data2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(temp_data2))
    return jsonify(trip)

####################################

if __name__ == "__main__":
    app.run(debug=True)