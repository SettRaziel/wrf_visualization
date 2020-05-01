from __future__ import print_function
import copy
#  Import Nio.
import Nio
#  Import numpy, sys, os.
import numpy, sys, os
#  Import the PyNGL module names.
import Ngl
import math
import temperature_lib, rain_lib, pressure_lib

#  Read in the data variables from the TS file
file = "Han.d01.TS"
input = []

with open(file) as f:
  head = next(f)
  for line in f:
    values = []
    for value in line.split():
      values.append(float(value))
    input.append(values)

# Create numpy 2D array
cdf = numpy.array(input)

# Collect meteorological data
pressure   = cdf[:, 9] / 100
rain_cum   = cdf[:, 16]
rain_expl  = cdf[:, 17]
tempht     = cdf[:, 5] - 273.15
hum        = cdf[:, 6]
taus       = cdf[:, 1]
u          = cdf[:, 7]
v          = cdf[:, 8]
rain_sum   = numpy.add(rain_cum, rain_expl)

#  Set up a color map and open an output workstation.
colors = numpy.array([                                                \
                         [255,255,255], [255,255,255], [255,255,255], \
                         [240,255,240], [220,255,220], [190,255,190], \
                         [120,255,120], [ 80,255, 80], [ 50,200, 50], \
                         [ 20,150, 20]                                \
                       ],'f') / 255.
wks_type = "png"
wks = Ngl.open_wks(wks_type,"meteogram")

# calculate secondary data
# dew points data and relative humidity
dew_point = numpy.empty(len(taus))
rel_hum = numpy.empty(len(taus))

for i in range(len(taus)):
  saturation_pressure = 6.1094 * math.exp((17.685 * tempht[i]) / (tempht[i] + 243.04))
  partial_pressure = 0.622 * saturation_pressure / pressure[i]
  rel_hum_pre = hum[i] * 100 / partial_pressure
  rel_hum[i] = min(rel_hum_pre, 100.)
  if (rel_hum[i] == 100.):
    dew_point[i] = tempht[i]
  else:
    dew_point[i] = tempht[i] - ((100. - rel_hum[i])/ 5.0)

# 3 hour rain sums
rain3h_time = numpy.empty(int(taus[-1] / 3))
rain3h_time[0] = 3
rain3h_sum = numpy.empty(len(rain3h_time))

j = 0
rain_prev = 0.0
rain_act = rain_sum[0]
for i in range(len(taus) - 1):
  if (taus[i] > rain3h_time[j]):
      rain_prev = rain_act
      rain_act = rain_sum[i]
      rain3h_sum[j] = rain_act - rain_prev
      j = j + 1
      rain3h_time[j] = rain3h_time[j-1] + 3
rain3h_sum[-1] = rain_act - rain_prev

# pressure resource
pres_res = pressure_lib.get_pressure_resource(taus, pressure)

# rain sum resources
rainsum_res = rain_lib.get_rainsum_resource(taus)

# 3 hour rain sum bar charts
rain3h_res = rain_lib.get_3hrain_resource(rain3h_time)

# ground temperature resource
tempsfc_res = temperature_lib.get_temperature_resource(tempht, dew_point)

# generate plot results
pressmsz  = Ngl.xy(wks,taus,pressure,pres_res)
rainsum   = Ngl.xy(wks,taus,rain_sum,rainsum_res)
rainhist  = Ngl.xy(wks,rain3h_time,rain3h_sum,rain3h_res)
temptmsz  = Ngl.xy(wks,taus,tempht,tempsfc_res)
tempsfc_res.xyLineColor     =  "blue"        # line color for dew point
dewpmsz   = Ngl.xy(wks,taus,dew_point,tempsfc_res)

Ngl.draw(pressmsz)
Ngl.overlay(rainsum, rainhist)
Ngl.draw(rainsum)
Ngl.overlay(temptmsz, dewpmsz)
Ngl.draw(temptmsz)
Ngl.frame(wks)

Ngl.end()
