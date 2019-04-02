import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
##################################
# Measurement table 
# id INTEGER
# station TEXT
# date TEXT
# prcp FLOAT
# tobs FLOAT

# Station table 
# id
# station
# name
# latitude
# longitude
# elevation
##################################

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    return(f"working")

@app.route("/api/v1.0/stations")
def stations():
    return(f"working")

@app.route("/api/v1.0/tobs")
def tobs():
    return(f"working")

@app.route("/api/v1.0/<start>")
def start():
    return(f"working")

@app.route("/api/v1.0/<start>/<end>")
def startEnd():
    return(f"working")

if __name__ == "__main__":
    app.run(debug=False)

# @app.route("/api/v1.0/precipitation")
# def prcp():
#     """Return a list of all precipitation"""
#     # Query all precipitation
#     results = session.query(Measurement.prcp).all()
#     all_prcp = []
#     for prcp in results:
#         prcp_dict = {}
#         prcp_dict[Measurement.date] = Measurement.prcp
#         all_prcp.append(prcp_dict)

# #     all_prcp = list(np.ravel(results))

#     return jsonify(all_prcp)


# @app.route("/api/v1.0/stations")
# def stations():
#     """Return a list of stations"""
#     # Query all passengers
#     results = session.query(Station).all()
#     # Create a dictionary from the row data and append to a list of all_stations
#     all_stations = []
#     for station in results:
#         station_dict = {}
#         station_dict["id"] = Station.id
#         station_dict["station"] = Station.station
#         station_dict["name"] = Station.name
#         station_dict["latitude"] = Station.latitude
#         station_dict["longitude"] = Station.longitude
#         station_dict["elevation"] = Station.elevation
#         all_stations.append(station_dict)

#     return jsonify(all_stations)

# if __name__ == '__main__':
#     app.run(debug=False)

- - -

# ## Step 2 - Climate App

# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

# * Use FLASK to create your routes.

# ### Routes

# * `/`

#   * Home page.

#   * List all routes that are available.

# * `/api/v1.0/precipitation`

#   * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.

#   * Return the JSON representation of your dictionary.

# * `/api/v1.0/stations`

#   * Return a JSON list of stations from the dataset.

# * `/api/v1.0/tobs`
#   * query for the dates and temperature observations from a year from the last data point.
#   * Return a JSON list of Temperature Observations (tobs) for the previous year.

# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

# ## Hints

# * You will need to join the station and measurement tables for some of the analysis queries.

# * Use Flask `jsonify` to convert your API data into a valid JSON response object.
