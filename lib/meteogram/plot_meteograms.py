from __future__ import print_function
import os, sys
import Ngl
import datetime
import meteogram_lib

# main run script for plotting meteograms based on the *.TS data of a model run
# version: v0.1.8
# created by Benjamin Held, December 2019

if (len(sys.argv) != 2):
  raise ValueError("Incorrect number of arguments, 1 argument required")

# read timestamp from the first script argument
timestamp = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d %H:%M")

# iterate over all files in the directory an print meteogram for each *.TS file
filepath = "../../files/"
for filename in os.listdir(filepath):
  if filename.endswith(".TS"):
    print("Creating output for: %s" % filename)  
    meteogram_lib.create_meteogram_for(filepath, filename, timestamp)

Ngl.end()
