#!/usr/bin/env python
#    ring2ring.py is an example module that copies from one ring to another as
#    an example of read and write.
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

## Import logging, configuration parsers, and  EWMod libraries.
from logging.handlers import TimedRotatingFileHandler
import configparser, argparse, logging, os, sys
from r2rMod import Ring2Ring
import time

DEBUG = False

## Lets get the parameter file
parser = argparse.ArgumentParser(description='This is an example ring to ring module with PyEW')
parser.add_argument('-f', action="store", dest="ConfFile",   default="ring2ring.d", type=str)

## Example of other arguments
#parser.add_argument('-r1', action="store", dest="RING1", default=1000, type=int) # a flag '-r1' argument
#parser.add_argument('-r2', action="store", dest="RING2", default=1005, type=int) # a flag '-r2' argument
#parser.add_argument("ConfFile") # A positional argument, such as a config file

## Read arguments and fetch the parameter file.
results = parser.parse_args()

## Actually parse the configuration file.
Config = configparser.ConfigParser()
Config.read(results.ConfFile)

## Setup the module logfile
# Get log path.
log_path = os.environ['EW_LOG']
# Create log filename from configuration file like EW.
log_name = results.ConfFile.split(".")[0] + ".log"
# Create a format that is adequate.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Rotate files, like Earthworm but using only 3 backup logs.
fh = TimedRotatingFileHandler(filename=log_path + log_name, when='midnight', interval=1, backupCount=3)
# Set level to debug.
fh.setLevel(logging.DEBUG)
# Set the formatter
fh.setFormatter(formatter)
# Add the handler to root logger
logging.getLogger().addHandler(fh)
# Set the logging level for root logger
logging.getLogger().setLevel(logging.DEBUG)


## Use a logger for this scope! We'll see how this works in the log file.
logger = logging.getLogger("ring2ring.py")
logger.info("Hello from ring2ring.py")

## Debug Flag (can be placed in .d file eventually)
logger.info("We are not using long debug")
DEBUG=False

# Start the Earthworm Module
logger.info("Setting up the module")
r2rModule = Ring2Ring (results.ConfFile, \
                       int(Config.get('Earthworm','RING_ID')), \
                       int(Config.get('Earthworm','MOD_ID')), \
                       int(Config.get('Earthworm','INST_ID')), \
                       int(Config.get('Earthworm','HB')), DEBUG)
logger.info("We are ok to start")

# Main program start
if __name__ == '__main__':
  try:
    r2rModule.start()
  except KeyboardInterrupt:
    print("\nSTATUS: Stopping, you hit ctl+C. ")
    r2rModule.stop()

