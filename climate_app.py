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
        f"/api/v1.0/calc/start<br/>"
        f"/api/v1.0/calc/start/end<br/>"
        f"/api/v1.0/alldates/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """Return a list of all precipitation the last 12 months"""
    #  Design a query to retrieve the last 12 months of precipitation data and plot the results
#    results = session.query(Passenger.name).all()
    results = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date > '2016-08-23').filter(Measurement.prcp != 'None').\
                order_by(Measurement.date).all()
    for p in results:
        print(p.date, p.prcp)

    # Convert list of tuples into normal list
    all_precipation = list(np.ravel(results))

    session.close()

    return jsonify(all_precipation)


@app.route("/api/v1.0/stations")
def stations():
#    result_stactivity = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).\
#                         order_by(func.count(Measurement.tobs).desc()).all()
    session = Session(engine)
    result_station = session.query(Measurement.station).group_by(Measurement.station).all()


    all_station = list(np.ravel(result_station))
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():

    results_stationtobs = session.query(Measurement.date, Measurement.tobs).group_by(Measurement.date).\
                         filter(Measurement.date > '2016-08-23').all()
#                         order_by(Measurement.tobs).desc()).all()
    all_stationtobs = list(np.ravel(results_stationtobs))
    session.close()
    return jsonify(all_stationtobs)

@app.route("/api/v1.0/calc/<start_date>")
# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_tempstart(start_date):
    """TMIN, TAVG, and TMAX for a start dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    session = Session(engine)
    results_calc_tempstart = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
#    print(calc_tempstart('2012-02-28'))
#    all_calc_tempstart = list(np.ravel(results_calc_tempstart))
    session.close()
    return jsonify(results_calc_tempstart)

@app.route("/api/v1.0/calc/<start_date>/<end_date>")
# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    session = Session(engine)
    results_calc_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
#    print(calc_temps('2012-02-28', '2012-03-05'))
    all_calc_temps = list(np.ravel(results_calc_temps))
    session.close()
    return jsonify(results_calc_temps)


@app.route("/api/v1.0/alldates/<start_date>/<end_date>")
# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_datetemps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    session = Session(engine)
    results_calc_datetemps = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        group_by(Measurement.date).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_calcs = []
    for calc in results_calc_datetemps:
#        print(calc)

        calc_dict = {}
        calc_dict["date"] = calc[0]
        calc_dict["min"] = calc[1]
        calc_dict["avg"] = calc[2]
        calc_dict["max"] = calc[3]
        all_calcs.append(calc_dict)

#    print(calc_temps('2012-02-28', '2012-03-05'))
#    all_calc_datetemps = list(np.ravel(results_calc_datetemps))
    session.close()
    return jsonify(all_calcs)
#    return jsonify(all_calc_datetemps)

if __name__ == '__main__':
    app.run(debug=True)
