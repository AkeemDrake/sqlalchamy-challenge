# 1. Import Flask
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import cast, DATE
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
    
# reflect the tables
Base.prepare(engine, reflect = True)

# Save reference to the table
Measurements = Base.classes.measurement
Stations = Base.classes.station

# 2. Create an app
app = Flask(__name__)

#stations list
stations = [{"Station": "USC00519397", "name": "WAIKIKI 717.2, HI US"},
 {"Station": "USC00513117", "name": "KANEOHE 838.1, HI US"},
 {"Station": "USC00514830", "name": "KUALOA RANCH HEADQUARTERS 886.9, HI US"},
 {"Station": "USC00517948", "name": "PEARL CITY, HI US"},
 {"Station": "USC00518838", "name": "UPPER WAHIAWA 874.3, HI US"},
 {"Station": "USC00519523", "name": "WAIMANALO EXPERIMENTAL FARM, HI US"},
 {"Station": "USC00519281", "name": "WAIHEE 837.5, HI US"},
 {"Station": "USC00511918", "name": "HONOLULU OBSERVATORY 702.2, HI US"},
 {"Station": "USC00516128", "name": "MANOA LYON ARBO 785.2, HI US"}]
#empty lists to add dictionaries
precipitation_list = []
temp_list = []

#3. Define static routes

@app.route ("/api/v1.0/precipitation")
def Precipitation():
    
    session = Session(engine)
    
    #Query the date and the precipitation data
    data = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date > dt.datetime(2016, 8, 23)).order_by(Measurements.date).all()
     
    #Convert the data into dictionary
    for x in data:
        print(x._asdict())
        precipitation_list.append(x)
    session.close()
    return jsonify(data)

#Route for dictionary of stations
@app.route("/api/v1.0/stations")
def Station() :
    
    return jsonify(stations)

#Route for the temperature data
@app.route("/api/v1.0/tobs")
def Temperature():
    
    session = Session(engine)
    #Query the temperature data
    temp = session.query(Measurements.date, Measurements.station, Measurements.tobs).filter(Measurements.date > dt.datetime(2016, 8, 23), Measurements.station.like('%USC00519281%')).all()
    #Convert list into dictionary
    for x in temp:
        print(x._asdict())
        temp_list.append(x)
     #Jsonify the results
    return jsonify(temp)
#Route for the start input date
@app.route("/api/v1.0/<start>")
def start(start):
           
    session = Session(engine)
     #Query the average, minimum, and maximum temps of user inputted date      
    start_input = session.query(Measurements.date, func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).filter(Measurements.date >= start).group_by(Measurements.date).order_by(Measurements.date).all()
           
    session.close()
    print(start_input)
           
    #Convert tuple to list       
    start_list = list(np.ravel(start_input))
    #Jsonify the results       
    return jsonify(start_list)

#Route for the range of dates
@app.route("/api/v1.0/<start><end>")
def startend(start,end):
    
    session = Session(engine)
     #Query the average, minimum, and maximum temps of user inputted range           
    start_end_input = session.query(Measurements.date, func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).filter(Measurements.date >= start).filter(Measurements.date <= end).group_by(Measurements.date).order_by(Measurements.date).all()
           
    session.close()
    
    #Convert tuple to list 
    
    start_end_data = list(np.ravel(start_end_input))
    
    print(start_end_input)
    #Jsonify the results       
    return jsonify(start_end_data)
           
@app.route ("/")
def Home():
    return ( "Hello! Welcome to the home page<br/>"
            "The routes avaliable are:<br/>"
            "/api/v1.0/precipitation<br/>"
            "/api/v1.0/stations<br/>"
            "/api/v1.0/tobs<br/>"
            "/api/v1.0/start<br/>"
            "/api/v1.0/end<br/>"
           )
if __name__ == "__main__":
    app.run(debug=True)