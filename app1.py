# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Set up database engine for Flask app
# Create function allows access to SQLite database file
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes
Base = automap_base()

# reflect the database
Base.prepare(engine, reflect=True)

# set the variables
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# set up flask
app = Flask(__name__)

# Example of app name variable
# import app

# print("example __name__ = %s", __name__)

# if __name__ == "__main__":
   # print("example is being run directly.")
# else:
 #   print("example is being imported")
print("app.py running")
 # define the welcome route
@app.route("/")

def welcome():
    return(
    
    f"Welcome to the Climate Analysis API!<br>"
    f"Available Routes:<br>"
    f"/api/v1.0/precipitation\n<br>"
    f"/api/v1.0/stations\n<br>"
    f"/api/v1.0/tobs\n<br>"
    f"/api/v1.0/temp/start/end<br>"
    )
# 9.5.3 Precipitation Route
@app.route("/api/v1.0/precipitation")


def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# 9.5.4 station route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# 9.5.5 Monthly Temperature route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# 9.5.6 statistic route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)



if __name__=='__main__':
   app.run()