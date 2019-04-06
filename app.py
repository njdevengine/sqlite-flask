# how to kill the app: kill -9 `lsof -i:5000 -t`
#import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import request, Flask, jsonify

# engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# session_factory = sessionmaker(bind=engine)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href= \"/api/v1.0/precipitation\">Route 1: date & prcp</a><br/>"
        f"<a href= \"/api/v1.0/stations\">Route 2: station list</a><br/>"
        f"<a href= \"/api/v1.0/tobs\">Route 3: last year's temp observations & dates</a><br/>"
        f"<a href=\"/api/v1.0/start?s=2017-01-01\">min, avg, max from start date</a><br/>"
        f"<a href=\"/api/v1.0/start_end?s=2017-01-01&e=2018-01-01\">min, avg, max in range</a><br/>"           
           )

@app.route("/api/v1.0/precipitation")
def precipitation():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    array = []
    x = session.query(Measurement).all()
    for i in x:
        prcp_dict = {}
        prcp_dict[i.date] = i.prcp
        array.append(prcp_dict)
    return jsonify(array)
# Measurement table:
################
# id
# station
# date
# prcp
# tobs

@app.route("/api/v1.0/stations")
def stations():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    array = []
    x = session.query(Station).all()
    for i in x:
        stat_dict = {}
        stat_dict["elevation"]  = i.elevation
        stat_dict["lon"]  = i.longitude
        stat_dict["lat"]  = i.latitude
        stat_dict["name"]  = i.name
        stat_dict["station"] = i.station
        array.append(stat_dict)
    return jsonify(array)
# Station table:
################
# station
# name
# latitude
# longitude
# elevation

@app.route("/api/v1.0/tobs")
def tobs():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    x = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
    tobs_dict = {}
    for i in x:
        tobs_dict[i.tobs] = i.date
    return jsonify(tobs_dict)
# Measurement table:
################
# id
# station
# date
# prcp
# tobs

@app.route("/api/v1.0/start")
def start():
    s = request.args.get('s')
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    x = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= s).all()
    start_dict = {}
    for i in x:
        start_dict["min"] = x[0][0]
        start_dict["avg"] = x[0][1]
        start_dict["max"] = x[0][2]
    return jsonify(start_dict)

@app.route("/api/v1.0/start_end")
def start_and_end():
    s = request.args.get('s')
    e = request.args.get('e')
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    x = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date.between(s,e)).all()
    se_dict = {}
    se_dict["min"] = x[0][0]
    se_dict["avg"] = x[0][1]
    se_dict["max"] = x[0][2]    
    return jsonify(se_dict)

if __name__ == "__main__":
    app.run(debug=False)
