#In order to analysis the table
import pandas as pd
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
engine = create_engine("sqlite://hawaii.sqlite")
#relfect an existing databse into a new model
Base = automap_base()
#relfect the tables
Base.classes.keys()
#save reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
#create our session from python to the db
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def homepage():
    return(f"Welcome to weather analysis API in Hawaii<br/>"
        f"Here is all the routes you can use: <br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>")



if __name__ == "__main__":
    app.run(debug=True)