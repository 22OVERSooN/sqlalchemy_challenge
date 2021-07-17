#In order to analysis the table
import pandas as pd
from sqlalchemy.sql.elements import Null
import numpy as np
#In order to retrive data from sqlite database
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
#In order to create API
import flask
from flask import Flask,jsonify

#create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")
#relfect an existing databse into a new model
Base = automap_base()
#relfect the tables
Base.prepare(engine, reflect = True)
#save reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
#create our session from python to the db


app = Flask(__name__)

@app.route("/")
def homepage():
    return(f"Welcome to weather analysis API in Hawaii<br/>"
        f"Here is all the routes you can use:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end<br/>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    one_year_before = dt.date(2017,8,23)-dt.timedelta(days = 365)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_before).\
            order_by(Measurement.date).all()
    session.close()
    precdic = {date: x for date, x in results}
    return jsonify(precdic)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    station_names = list(np.ravel(results))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
            filter(Measurement.date >= '2017,8,23').all()
    tobs_list = list(np.ravel(results))
    session.close()
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start = None, end = None):
    session = Session(engine)
    stas = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*stas).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)        

    results = session.query(*stas).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)