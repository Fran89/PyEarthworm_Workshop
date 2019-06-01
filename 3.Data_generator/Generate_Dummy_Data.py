## Let's import some basic libraries
import logging, sys, sched, time
import PyEW
import numpy as np
from datetime import datetime
from threading import Thread

## Let's setup logging to the console
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

## Let's set the sample rate
SRate = 100

## Let's setup the PyEW Module
dataGenMod = PyEW.EWModule(1000, 10, 141, 30.0, False)
dataGenMod.add_ring(1000)

## Let's create a function that creates a packet of data from 0 to 1024
xdat = 0
def gen_data(samprate):
  global xdat ## This allows the use of the global var inside a function
  resarr = []
  for num in range (0, samprate):
      if xdat > 1024:
        xdat = 0
      resarr.append(xdat)
      xdat = xdat + 1
  return np.array(resarr, dtype=np.dtype(np.int16))

## Test our generator
#for num in range(0, 9):
#  test=gen_data(SRate)
#  print(test)
#  print(test.size)


## Setup high precision timing:
sec_arg = 1.000 # Delay
cptr = 0        # Control pointer
time_start = time.time() # Started time
time_init = time.time()  # Initial time

while (1):
  ## Let's check in to how our module is doing in Earthworm, if .mod_sta() is False something went wrong!
  if dataGenMod.mod_sta() is False:
    break
  
  ## Continue high precision timing code
  cptr += 1
  time_start = time.time()
  
	## Let's create an artificial wave object.
  TestWave = {
    'station': 'Test',
    'network': 'NC',
    'channel': 'BHZ',
    'location': '--',
    'nsamp': SRate,
    'samprate': SRate,
    'startt': datetime.timestamp(datetime.now()), ## Grab out current time as a timestamp.
    #'endt': myTime+(1/SRate), This can be used but It's also auto calculated
    'datatype': 'i2',
    'data': gen_data(SRate)
  }
  
  ## Put this wave into the ring
  dataGenMod.put_wave(0,TestWave)
	
	## Wait for one seconds (using high precision ~1ms) since we're at 100 sps and a 100 sample packet
	## For higher resolution you can use python ctypes and Linux's nanosleep, in a sub-process to bypass GIL Lock or use C/C++ ;)
  try:
    time.sleep(((time_init + (sec_arg * cptr)) - time_start ))
  except KeyboardInterrupt:
    print('\n =============')
    print('Exit Main Loop...')
    break

## Clean Exit
dataGenMod.goodbye()
print("\nSTATUS: Stopping, you hit ctl+C. ")
