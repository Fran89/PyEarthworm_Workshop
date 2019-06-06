#!/usr/bin/env python
#    PyEWPlot.py is a EW Module that creates a WebServer that plots traces and 
#    serves them via web browser.
#    Copyright (C) 2019  Francisco J Hernandez Ramirez
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>

# Import Flask and EWMod libraries
from flask import Flask, render_template, Response, request, jsonify
from logging.handlers import TimedRotatingFileHandler
import configparser, argparse, logging, os, sys
from EWMod import EWPyPlotter
import time

DEBUG = False

# Lets get the parameter file
Config = configparser.ConfigParser()
parser = argparse.ArgumentParser(description='This is a Earthworm Real Time Trace Viewer for web browsers')
#parser.add_argument('-i', action="store", dest="IP",   default="localhost", type=str)
#parser.add_argument('-p', action="store", dest="PORT", default=5000,        type=int)
    
parser.add_argument('-f', action="store", dest="ConfFile",   default="gsof2ring.d", type=str)
    
results = parser.parse_args()
Config.read(results.ConfFile)

# Setup the module logfile
log_path = os.environ['EW_LOG']
log_name = results.ConfFile.split(".")[0] + ".log"
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = TimedRotatingFileHandler(filename=log_path + log_name, when='midnight', interval=1, backupCount=3)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logging.getLogger().addHandler(fh)
logging.getLogger().setLevel(logging.DEBUG)

# Start the Earthworm Module
Plotter = EWPyPlotter(results.ConfFile, int(Config.get('Plot','Time')), int(Config.get('Earthworm','RING_ID')), \
                      int(Config.get('Earthworm','MOD_ID')), int(Config.get('Earthworm','INST_ID')),\
                      int(Config.get('Earthworm','HB')), DEBUG)
Plotter.start()

# Start the web server
app = Flask(__name__,static_url_path = "/tmp", static_folder = "tmp")

# Generate image stream
def gen(station):
  while True:
    time.sleep(0.3)
    frame = Plotter.get_frame(station)
    last_frame = 0
    if len(frame) is not 0:
      yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Homepage should display the list of station/channels
@app.route('/')
def index():
  stations = list(Plotter.get_menu())
  stations.sort()
  individualsta = []
  for station in stations:
    thissta = station.split('.')[0]
    individualsta.append(thissta)
  matching = set(individualsta)
  matching = sorted(matching)
  return render_template('index.html', results=stations, results2 = matching)
  
# Station Graph stream page
@app.route('/Station/<Stat>')
def STAgraph(Stat):
  # Get stations and sort
  stations = list(Plotter.get_menu())
  stations.sort()
  # Get matching channels and sort
  matching = [s for s in stations if Stat in s]
  matching.sort()
  # Check for correct station
  if not matching:
    Status = "Incorrect Station or Station not ready"
    exts = False
  else:
    Status = "Graphs for Station: " + Stat
    exts = True
  chls = []
  # Convert to tuple to sort by key (loc code)
  for chs in matching:
    chtp = tuple(chs.split('.'))
    chls.append(chtp)
  sorted(chls, key=lambda location: location[3])
  # Convert back to string list to send to webpage
  chsr = []
  for ch in chls:
    st = '.'.join(map(str, ch))
    chsr.append(st)
  # Render webpage
  return render_template('station.html', exist = exts, value=Status, stations=chsr)

# SCNL Graph stream page
@app.route('/SCNL/<Stat>')
def SCNLgraph(Stat):
  if Plotter.get_frame(Stat) is None:
    Status = "Incorrect Station or Station not ready"
    exts = False
  else: 
    Status = "Graph for Station/Component: " + Stat
    exts = True
  return render_template('graph.html', exist = exts, value=Status, station=Stat)

# Graph stream video URL
@app.route('/graph_feed/<StaStr>')
def graph_feed(StaStr):
  return Response(gen(StaStr),
                  mimetype='multipart/x-mixed-replace; boundary=frame')

# Menu should return a json file with all channels              
@app.route('/menu/')
def menu_api():
  stations = list(Plotter.get_menu())
  stations.sort()
  return jsonify(stations)

# Main program start
if __name__ == '__main__':
  try:
    app.run(host=Config.get('Server','IP'), port=Config.get('Server','PORT'), debug=DEBUG)
  except KeyboardInterrupt:
    print("\nSTATUS: Stopping, you hit ctl+C. ")
    Plotter.stop()
