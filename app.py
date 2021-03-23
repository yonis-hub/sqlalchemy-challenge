
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
        <p><strong>Precipitation Analysis:</strong></p>
        
             <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a>
            
        <p><strong>Station Analysis:</strong></p>
           
            <a href="/api/v1.0/stations">/api/v1.0/stations</a>
            
        <p><strong>Temperature Analysis:</strong></p>

       
            <a href="/api/v1.0/tobs">/api/v1.0/tobs</a>
          
        <p><strong>Start Day Analysis:</strong></p>
           
            <a href="/api/v1.0/2017-03-14">/api/v1.0/2017-03-14</a>
            
        <p><strong>Start & End Day Analysis:</strong></p>
           
            <a href="/api/v1.0/2017-03-14/2017-03-28">/api/v1.0/2017-03-14/2017-03-28</a>
          
    </html>
    """


@app.route("/api/v1.0/precipitation")
def precipitation():
    previous_year = dt.date(2017,8,23) - dt.timedelta(days = 365)

    prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).\
    order_by(Measurement.date).all()

    prcp_df = pd.DataFrame(prcp, columns=['date', 'prcp'])

     # Convert to list
    prcp_dic = prcp_df.to_dict()

    return jsonify(prcp_dic)


##code below is from climate.ipynb file!!##

# Station Route
@app.route("/api/v1.0/stations")
def stations():

        results = session.query(Station.station, Station.name).all()

        station_list = list(results)

        return jsonify(station_list)




# TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():

    previous_year = dt.date(2017,8,23) - dt.timedelta(days = 365)

    temp = session.query(Measurement.tobs).filter(Measurement.date >= previous_year).filter(Measurement.station == 'USC00519281')

    order_temp = temp.order_by(Measurement.date).all()

   
    tobs_list = list(order_temp)

    return jsonify(tobs_list)



# Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):

    start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))

 
    str_day = start_day.filter(Measurement.date >= start).group_by(Measurement.date).all()
    
    start_list = list(str_day)
        
   
    return jsonify(start_list)


# Start to End Route
@app.route("/api/v1.0/<start>/<end>")
def start_to_end(start, end):
    
    str_to_end = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
    
    str_end = str_to_end.filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
        
   
    start_end_list = list(str_end)
        
       
    return jsonify(start_end_list)


#define main behavior
if __name__ == '__main__':
    app.run(debug = True)