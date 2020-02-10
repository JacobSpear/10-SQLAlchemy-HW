from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, Column, Integer, String, Float
import datetime as dt
import numpy as np

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine,reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to a Weather API"

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    data = session.query(Measurement.date,func.avg(Measurement.prcp)).\
        group_by(Measurement.date).all()
    session.close()

    prcp_dict = {}
    for item in data:
        prcp_dict[item[0]] =item[1]
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    data = session.query(Station.name).all()
    session.close()

    output = list(np.ravel(data))
    return jsonify(output)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    dates = [dt.datetime.strptime(x[0],'%Y-%m-%d') for x in session.query(Measurement.date).all()]
    start_date = max(dates) - dt.timedelta(days=365)
    start_date_str = dt.datetime.strftime(start_date,'%Y-%m-%d')
    session.close()

    session = Session(engine)
    data = session.query(Measurement.tobs).\
        filter(Measurement.date >= start_date_str).all()
    session.close()
    return jsonify(list(np.ravel(data)))

@app.route("/api/v1.0/<start>")
def start_fcn(start):
    session = Session(engine)
    data = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date>=start).all()
    session.close()

    return jsonify(list(np.ravel(data)))


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)
    data = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date>=start).\
        filter(Measurement.date<=end).\
        all()
    session.close()

    return jsonify(list(np.ravel(data)))


if __name__ == "__main__":
    app.run(debug=True)