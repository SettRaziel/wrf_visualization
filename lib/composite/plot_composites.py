from __future__ import print_function
import numpy, Nio, Ngl, os, sys
from wrf import getvar, get_pyngl
import comp_lib, rain_lib, thunderstorm_lib
import datetime

# main run script for plotting composite plots based on the *.nc data of a model run
# version: v0.1.7
# created by Benjamin Held, December 2019

filepath = "../../files/"
previous_data = None
data_list = os.listdir(filepath) # return an arbitrary sorted list of files in the directory
data_list.sort() # sort list regain the lexicographic order for the output by its timestamps
for filename in data_list:
  if filename.startswith("wrfout"):
    print("Creating output for: %s" % filename)
    wrf_data = Nio.open_file(filepath + filename + ".nc")  # Must add ".nc" suffix for Nio.open_file
    timestamp = datetime.datetime.strptime(filename.split("d01_")[1], "%Y-%m-%d_%H:%M:%S")
    
    # plot composite with temperature, pressure and wind                              
    comp_lib.print_comp_for_timestamp(wrf_data, timestamp, filepath)

    # plot cape and pressure
    thunderstorm_lib.print_cape_for_timestamp(wrf_data, timestamp, filepath)

    if (previous_data is not None):
      # plot total rainsum and pressure
      rain_lib.print_total_rainsum_for_timestamp(wrf_data, timestamp, filepath)

      # plot 3h rainsum and pressure
      rain_lib.get_3h_rainsum(previous_data, wrf_data, timestamp, filepath)
      
    previous_data = wrf_data

Ngl.end()
