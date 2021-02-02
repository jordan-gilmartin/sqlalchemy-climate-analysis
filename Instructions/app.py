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
meas = Base.classes.measurement
sta = Base.classes.station

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
        f"/api/v1.0/<start>" 
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query dates and prcp levels for the last year
    dateprcp = session.query(meas.date, meas.prcp).filter(meas.date > '2016-08-23').order_by(meas.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list 
    measurement = []
    for date, prcp in dateprcp:
        dateprcp_dict = {}
        dateprcp_dict[date] = prcp
        measurement.append(dateprcp_dict)

    return jsonify(measurement)    
        
    
    
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(sta.station).all()

    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)
   
   
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    tempfreq = session.query(meas.station, meas.date, meas.tobs).filter(meas.station == 'USC00519281').filter(meas.date > '2016-08-23').order_by(meas.date).all()

    session.close()

    # Convert list of tuples into normal list
    temps = list(np.ravel(tempfreq))

    return jsonify(temps)
   
      
   
@app.route("/api/v1.0/<start>")
def start_date(start):
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""

    canonicalized = start.replace(" ", "").lower()
    for date in measurement:
        search_date = date["date"].replace(" ", "").lower()

        if search_date == canonicalized:
            return jsonify(date)

    return jsonify({"error": f"Date of {start} not found."}), 404
   
   
   
   
   
   
   
    # # Convert list of tuples into normal list
    # all_names = list(np.ravel(results))

    # return jsonify(all_names)


# @app.route("/api/v1.0/passengers")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
