#    Ring2Ring is an example of how to use PyEW to interface a Python Program to the EW Transport system
#    Copyright (C) 2018  Francisco J Hernandez Ramirez
#    You may contact me at FJHernandez89@gmail.com, FHernandez@boritechsolutions.com
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
import time, configparser, logging
from threading import Thread
import PyEW

# If we need we can add a logger here too!
logger = logging.getLogger(__name__)

# This is the ring2ring Class
class Ring2Ring():

  def __init__(self, ConfFile, mainRing, modID, instID, hbRate, Debug):
    
    # Say hello to logger
    logger.info("Starting r2rMod")
    
    # Create a thread for self
    self.myThread = Thread(target=self.run)
    
    # Start an EW Module with parent ring 1000, mod_id 8, inst_id 141, heartbeat 30s, debug = False (MODIFY THIS!)
    self.ring2ring = PyEW.EWModule(mainRing, modID, instID, hbRate, Debug)
    
    # Re-read our configuration file
    config = configparser.ConfigParser()
    config.read(ConfFile)
    
    # Add our Input ring as Ring 0
    logger.info('Set input ring as %s', config.get('Rings','RING_IN'))
    self.ring2ring.add_ring(int(config.get('Rings','RING_IN')))
    
    # Add our Output ring as Ring 1
    logger.info('Set output ring as %s', config.get('Rings','RING_OUT'))
    self.ring2ring.add_ring(int(config.get('Rings','RING_OUT')))
    
    # Allow it to run
    self.runs = True
    
  def copy_wave(self):
    
    # Fetch a wave from Ring 0
    wave = self.ring2ring.get_wave(0) 
    
    # if wave is empty return
    if wave == {}: 
      return
    
    # Put into Ring 1 the fetched wave
    self.ring2ring.put_wave(1, wave) 
    
  def run(self):
    
    # The main loop
    while self.runs:
      if self.ring2ring.mod_sta() is False:
        break
      time.sleep(0.001)
      self.copy_wave()
    logger.info("Exiting from r2rMod")
    self.ring2ring.goodbye()
      
  def start(self):
    self.myThread.start()
    
  def stop(self):
    self.runs = False
 
