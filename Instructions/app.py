import numpy as np
	

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import session
from sqlalchemy import create_engine, func
import datetime as dt 
from flask import Flask, jsonify
	
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
	
Base = automap_base()
	
Base.prepare(autoload_with=engine)
	
Measurement = Base.classes.measurement
Station = Base.classes.station
	
# Flask Setup
app = Flask(__name__)
	
@app.route("/")
def home():
	    #home page
	return (
	        f"<h3>Available routes</h3><br/>"
	        f"/api/v1.0/precipitation<br/>"
	        f"/api/v1.0/stations<br/>"
	        f"/api/v1.0/tobs<br/>"
	        f"/api/v1.0/2014-05-01  - please enter a date between <strong>2010-01-01  and 2017-08-23</strong> in that format<br/>"
	        f"/api/v1.0/2014-05-01/2015-04-30 - please enter a <strong>start date and end date</strong> between <strong>2010-01-01 and 2017-08-23</strong> in that format "
	)
	

@app.route("/api/v1.0/precipitation")
def precipitation():
	   
	lastdate = session.query(func.max(Measurement.date)).scalar()
	dt_lastdate= dt.datetime.strptime(lastdate,"%Y-%m-%d").date()
	dt_startdate = dt_lastdate - dt.timedelta(days=365)
	startdate = dt_startdate.strftime("%Y-%m-%d")
	results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between(startdate,lastdate)).all()
	    
	session.close()
	

@app.route("/api/v1.0/stations")
def stations():
	    
	session = session(engine)
	

	results = session.query(Station.name).all()
	

	session.close()
	

	all_stations = list(np.ravel(results))
	return jsonify(all_stations)
	

@app.route("/api/v1.0/tobs")
def tobs():
	    
	session = session(engine)
	top_station = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).subquery()
	

	lastdate = session.query(func.max(Measurement.date)).scalar()
	dt_lastdate= dt.datetime.strptime(lastdate,"%Y-%m-%d").date()
	dt_startdate = dt_lastdate - dt.timedelta(days=365)
	startdate = dt_startdate.strftime("%Y-%m-%d")
	    
	results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date.between(startdate,lastdate)).filter(Measurement.station.in_(top_station)).all()
	session.close()

