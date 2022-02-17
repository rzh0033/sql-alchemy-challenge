
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

# Db setup
engine = create_engine('sqlite://Resources/hawaii.sqlite')

last_year = dt.date(2017,8,23) - dt.timedelta(days = 365)

Base = automap_base()
Base.prepare(engine, reflect = True)

# Save table as reference
measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return(
        f'Climate Analysis: <br/>'
        f'Available Paths: <br/>'
        f'/api/v1.0/precipitation <br/>'
        f'/api/v1.0/stations <br/>'
        f'/api/v1.0/tobs <br/>'
        f'/api/v1.0/<start> <br/>'
        f'/api/v1.0/<start>/<end> <br/>'
        
    )
    
@app.route('/api/v1.0/precipitation <br/>')
def precipation():
    session = Session(engine)
    precip_vals = session.query(measurement.date, measurement.prcp).all()
    
    session.close()
    
    level = []
    for date, prcp in precip_vals:
        measurement_dict = {}
        measurement_dict['date'] = date
        measurement_dict['precip'] = prcp
        level.append(measurement_dict)
        
    return jsonify(level)

@app.route('/api/v1.0/stations <br/>')
def stations():
    session = Session(engine)
    station_vals = session.query(Station.station).all()
    
    session.close()
    
    station_names = list(np.ravel(station_vals))
    
    return jsonify(station_names)

@app.route('api/v1.0/tobs')
def tobs():
    session = Session(engine)
    active_station = session.query(measurement.station, func.count(measurement.tobs)).group_by(measurement.station),order_by(func.count(measurement.tobs).desc()).first()[0]
    
    tobs_vals = session.query(measurement.date, measurement.station, measurement.tobs).filter(measurement.station == active_station).filter(measurement.date >= last_year).all()
    
    session.close()
    
    tobs_active = []
    for date, station, tobs in tobs_vals:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['station'] = station
        tobs_dict['tobs'] = tobs
        tobs_active.append(tobs_dict)
        
    return jsonify(tobs_active)

@app.route('api.v1.0/<start>')
def stat1(start):
    session = Session(engine)
    
    stats_1 = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    
    session.close()
    
    stats_start = []
    for min, avg, max in stats_1:
        stats_start_dict = {}
        stats_start_dict['min'] = min
        stats_start_dict['avg'] = avg
        stats_start_dict['max'] = max
        stats_start.append(stats_start_dict)
        
    return jsonify(stats_start)

@app.route('api.v1.0/<start>/<end>')
def stat2(start, end):
    session = Session(engine)
    
    stats_2 = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    session.close()
    
    stats_start_end = []
    for min, avg, max in stats_2:
        stats_start_end_dict = {}
        stats_start_end_dict['min'] = min
        stats_start_end_dict['avg'] = avg
        stats_start_end_dict['max'] = max
        stats_start_end.append(stats_start_end_dict)
        
    return jsonify(stats_start_end)

if __name__  == '__main__':
    app.run(debug=True)
