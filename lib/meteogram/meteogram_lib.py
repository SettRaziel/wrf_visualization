from __future__ import print_function
import copy
#  Import Nio.
import Nio
#  Import numpy, sys, os.
import numpy, sys, os
#  Import the PyNGL module names.
import Ngl
import math
import datetime
import temperature_lib, rain_lib, pressure_lib, wind_lib, humidity_lib

# function to read the content of the given *.TS meteogram file
def read_file(file):
  input = []

  head = next(file)
  for line in file:
    values = []
    for value in line.split():
      values.append(float(value))
    input.append(values)

  return head, input

# function to create the x-axis labels with timestamps at midnight
def generate_xlegend(timestamp, forecast_hours):
  # initial with hours to next midnight
  time_offset = 24 - timestamp.hour
  main_hours = []
  sec_hours = []
  labels = []

  while(time_offset <= forecast_hours):
    main_hours.append(time_offset)
    labels.append((timestamp + datetime.timedelta(hours=time_offset)).strftime("%b %d/%H"))
    time_offset += 24

  time_offset = 12 - timestamp.hour
  while(time_offset <= forecast_hours):
    if (time_offset > 0):
      sec_hours.append(time_offset)
    time_offset += 24    

  return main_hours, sec_hours, labels

# function to create the meteogram for the given location
def create_meteogram_for(filename, timestamp):
  with open(filename) as f:
    head, input = read_file(f)

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
  wks = Ngl.open_wks(wks_type,"meteogram_"+filename.split(".")[0])

  # calculate secondary data
  count_xdata = taus[-1]
  main_hours, sec_hours, labels = generate_xlegend(timestamp, count_xdata)
  # dew points data and relative humidity
  rel_hum = humidity_lib.calculate_relative_humidity(hum, tempht, pressure, len(taus))
  dew_point = temperature_lib.calculate_dewpoint(tempht, rel_hum, len(taus))

  # 3 hour rain sums
  rain3h_sum, rain3h_time = rain_lib.calculate_3hrain_data(rain_sum, taus)

  # wind speed
  wind_speed = wind_lib.calculate_windspeed(u, v, len(taus))

  # wind direction
  wind_direction = wind_lib.calculate_winddirection(u, v, len(taus))

  # generate measurand resources
  # pressure resource
  headline = head.split(" ")[0] + " (%s)" % timestamp.strftime("%b %d %Y %HUTC")
  pres_res = pressure_lib.get_pressure_resource(count_xdata, pressure, headline)
  pres_res.tmXBValues = numpy.array(main_hours)
  pres_res.tmXBMinorValues = numpy.array(sec_hours)
  pres_res.tmXBLabels = labels

  # relative humidity
  relhum_res = humidity_lib.get_relhumidity_resource(count_xdata)
  relhum_res.tmXBValues = numpy.array(main_hours)
  relhum_res.tmXBMinorValues = numpy.array(sec_hours)
  relhum_res.tmXBLabels = labels

  # wind speed recource
  wind_res = wind_lib.get_windspeed_resource(count_xdata, wind_speed)
  wind_res.tmXBValues = numpy.array(main_hours)
  wind_res.tmXBMinorValues = numpy.array(sec_hours)
  wind_res.tmXBLabels = labels

  # wind direction recource
  direction_res = wind_lib.get_winddirection_resource(count_xdata, wind_speed)
  direction_res.tmXBValues = numpy.array(main_hours)
  direction_res.tmXBMinorValues = numpy.array(sec_hours)
  direction_res.tmXBLabels = labels

  # rain sum resources
  rainsum_res = rain_lib.get_rainsum_resource(count_xdata)
  rainsum_res.tmXBValues = numpy.array(main_hours)
  rainsum_res.tmXBMinorValues = numpy.array(sec_hours)
  rainsum_res.tmXBLabels = labels

  # 3 hour rain sum bar charts
  rain3h_res = rain_lib.get_3hrain_resource(rain3h_time)

  # ground temperature resource
  tempsfc_res = temperature_lib.get_temperature_resource(count_xdata, tempht, dew_point)
  tempsfc_res.tmXBValues = numpy.array(main_hours)
  tempsfc_res.tmXBMinorValues = numpy.array(sec_hours)
  tempsfc_res.tmXBLabels = labels

  # generate plot results
  pressmsz  = Ngl.xy(wks,taus,pressure,pres_res)
  relhummsz = Ngl.xy(wks,taus,rel_hum,relhum_res)
  windmsz   = Ngl.xy(wks,taus,wind_speed,wind_res)
  dirmsz    = Ngl.xy(wks,taus,wind_direction,direction_res)
  rainsum   = Ngl.xy(wks,taus,rain_sum,rainsum_res)
  rainhist  = Ngl.xy(wks,rain3h_time,rain3h_sum,rain3h_res)
  temptmsz  = Ngl.xy(wks,taus,tempht,tempsfc_res)
  tempsfc_res.xyLineColor     =  "blue"        # line color for dew point
  dewpmsz   = Ngl.xy(wks,taus,dew_point,tempsfc_res)

  Ngl.draw(pressmsz)
  Ngl.draw(relhummsz)
  Ngl.overlay(rainsum, rainhist)
  Ngl.draw(rainsum)
  Ngl.draw(windmsz)
  Ngl.draw(dirmsz)
  Ngl.overlay(temptmsz, dewpmsz)
  Ngl.draw(temptmsz)
  Ngl.frame(wks)
  Ngl.delete_wks(wks) # delete currently used workstation
