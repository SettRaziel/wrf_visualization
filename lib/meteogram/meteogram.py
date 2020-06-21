from __future__ import print_function
import os, sys
import Ngl
import datetime
import meteogram_lib

if (len(sys.argv) != 2):
  raise ValueError("Incorrect number of arguments, 1 argument required")

# read timestamp from the first script argument
timestamp = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d %H:%M")

# iterate over all files in the directory an print meteogram for each *.TS file
filepath = "../../files/"
for filename in os.listdir(filepath):
  if filename.endswith(".TS"):  
    meteogram_lib.create_meteogram_for(filepath, filename, timestamp)

Ngl.end()
