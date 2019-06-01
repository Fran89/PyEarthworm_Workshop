#!/bin/bash
#
#       Shell_script.sh
#       
#       Copyright 2019 Francisco Hernandez <FJHernandez89@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       

# Setup our environment
CurDir="$( cd "$( dirname "$0" )" && pwd )"
cd $CurDir
export PATH=$PATH:$CurDir/ew-node/bin
export ThisDir=$CurDir
source $CurDir/ew-node/params/ew_linux.bash
conda activate pyew

# Check data input
sniffwave WAVE_RING

