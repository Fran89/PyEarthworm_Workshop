# Conda!

Conda is an interactive manager for python environments and packages, here we will download 
and install conda and setup the environment needed to compile PyEarthworm

## Install conda

First install conda by visiting: 

https://www.anaconda.com/distribution/

or 

https://docs.conda.io/en/latest/miniconda.html

Miniconda is a more lightweight version of the full anaconda distribution

## Create a virtual environment

The second step is once the distribution has been installed we should create a 
virtual environment on which to deploy PyEW, or we can always install it at the
base level but this is not always recommended as it may interfere with other 
pakages

    conda create --name pyew

This will create a virtual environment on which we can install multiple libaries.
We can also create this virtual environment in different versions with different
versions of python.

    conda create --name pyew python=x.x
    
You can also add all packages already associated with a particular environment
such as anaconda

    conda create --name pyew python=x.x anaconda
    
After this we should proceed to activate this environment in order to be able to
install the necesary packages in this virtual environment which helps isolate
packages from system packages.

    conda activate pyew
    
## Install necessary packages

Conda is a package manager that in this virtual environment allows for the 
installation of many Python, C/C++, R, etc... dependencies and packages. In this
case we will be installing python packages. In this tutorial we will be using 
the folllowing:

    conda install cython jupyter numpy flask configparser pillow scipy matplotlib
    
These are just some of the ones we may use, but there are many many more. One 
notable lib would be Obspy. In the event you don't have git you can install it 
with conda:

    conda install git

## Compile PyEW

Just about the last thing we need to do is download and compile PyEarthworm the
library we can use to read and write directly to the earthworm ring. Remember to
source the environment file for earthworm prior to these next steps. To do this
we first download the source from here using git:

    git clone https://github.com/Boritech-Solutions/PyEarthWorm.git
    
Then we 'cd' into the src directory:

    cd PyEarthWorm/src/
    
We run the compile line:

    python setup.py build_ext -i

If all went well you should have a PyEW.cpython-37m-x86_64-linux-gnu.so which we
can move to the folders or install in the python path.

*N.B If you are on Windows, you should use the Windows EW_NT.cmd and have it 
properly configured. Aditionally you should use the windows branch of PyEarthworm
It will create a PyEW.dll if I'm not mistaken. Ask me for this file if you do 
not have it.*

## Install to python path

First we find where to install it, with our environment activated run:

    python
    import sys
    print(sys.path)

it should output a list like this:

    ['', '/home/francisco/.anaconda3/envs/pyew/lib/python37.zip', 
    '/home/francisco/.anaconda3/envs/pyew/lib/python3.7', 
    '/home/francisco/.anaconda3/envs/pyew/lib/python3.7/lib-dynload', 
    '/home/francisco/.anaconda3/envs/pyew/lib/python3.7/site-packages']
    
We're looking for the lib-dynload folder. Copy the PyEW.cpython-37m-x86_64-linux-gnu.so
to the /envs/pyew/lib/python3.7/lib-dynload. Once done close the python with 
'exit()'. To test this worked:

    python
    import PyEW
    
If there was no error it sucessfully opened.

### We are done setting up the environment and are ready to develop.
