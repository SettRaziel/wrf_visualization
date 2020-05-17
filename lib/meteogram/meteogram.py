from __future__ import print_function
import os
#  Import the PyNGL module names.
import Ngl
import meteogram_lib

#  Iterate over all files in the directory an print meteogram for each *.TS file
for filename in os.listdir("."):
  if filename.endswith(".TS"):  
    meteogram_lib.create_meteogram_for(filename)

Ngl.end()
