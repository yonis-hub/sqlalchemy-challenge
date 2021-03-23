
# Import Flask
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
Measurement = Base.classes.measurement

# 2nd table

Station = Base.classes.station



# Create our session (link) from Python to the DB
session = Session(engine)


# Create an app
app = Flask(__name__)


# Define static routes
@app.route("/")
def welcome():
    return """<html>
    <h1>Hawaii Climate App </h1>
        <p>Precipitation Analysis:</p>
            <ul>
                <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
            </ul>
        <p>Station Analysis:</p>
            <ul>
                <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
            </ul>
        <p>Temperature Analysis:</p>
            <ul>
                <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
            </ul>
        <p>Start Day Analysis:</p>
            <ul>
                <li><a href="/api/v1.0/2017-03-14">/api/v1.0/2017-03-14</a></li>
            </ul>
        <p>Start & End Day Analysis:</p>
            <ul>
                <li><a href="/api/v1.0/2017-03-14/2017-03-28">/api/v1.0/2017-03-14/2017-03-28</a></li>
            </ul>
    </html>
    """


@app.route("/api/v1.0/precipitation")
def precipitation():
    previous_year = dt.date(2017,8,23) - dt.timedelta(days = 365)

    prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).\
    order_by(Measurement.date).all()

    prcp_df = pd.DataFrame(prcp, columns=['date', 'prcp'])

    prcp_dic = prcp_df.to_dict()

    return jsonify(prcp_dic)




# # Station Route
# @app.route("/api/v1.0/stations")
# def stations():
#         print("station info")
#         return 




# # TOBs Route
# @app.route("/api/v1.0/tobs")
# def tobs():
#     print("print tobs info here")
#     return 


# # Start Day Route
# @app.route("/api/v1.0/<start>")
# def start_day(start):
#     print("start_day info here")
#     return


# # Start to End Route
# @app.route("/api/v1.0/<start>/<end>")
# def start_to_end(start, end):
#     print('start and end info here')
#     return 


#define main behavior
if __name__ == '__main__':
    app.run(debug = True)