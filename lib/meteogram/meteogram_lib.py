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

  head = next(file).split(" ") # split string at whitespace
  head = " ".join(head).split() # remove whitespace elements
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

# function to create the bars for the 3hour rain sums
def create_rain_bar_plot(wks, rain3h_time, rain3h_sum, rain3h_res):
  rainhist  = Ngl.xy(wks, rain3h_time, rain3h_sum, rain3h_res)
  dummy = rain3h_res.trYMinF * numpy.ones([len(rain3h_sum)], rain3h_sum.dtype.char)

  # check for bars for the first and last value on the x axis
  dx                 = min(rain3h_time[1:-1] - rain3h_time[0:-2])
  rain3h_res.trXMinF = min(rain3h_time) - dx/2.
  rain3h_res.trXMaxF = max(rain3h_time) + dx/2.
  rainhist  = Ngl.xy(wks, rain3h_time, dummy, rain3h_res)

  # check where the rain sum is > 0 and craw a bar for it
  above_zero     = numpy.greater(rain3h_sum, 0.0)
  ind_above_zero = numpy.nonzero(above_zero)
  num_above = len(ind_above_zero[0])

  px = numpy.zeros(5 * num_above, rain3h_time.dtype.char)
  py = numpy.zeros(5 * num_above, rain3h_sum.dtype.char)

  # bar resource
  pgres             = Ngl.Resources()
  pgres.gsFillColor = "green"
  pgres.gsFillOpacityF = 0.75

  taus_above_zero = numpy.take(rain3h_time, ind_above_zero)
  # create bar rectangle
  taus_plus = (taus_above_zero + dx/2.).astype(rain3h_time.dtype.char)
  taus_minus = (taus_above_zero - dx/2.).astype(rain3h_time.dtype.char)
  px[0::5] = taus_minus
  px[1::5] = taus_minus
  px[2::5] = taus_plus
  px[3::5] = taus_plus
  px[4::5] = taus_minus
  py[0::5] = rain3h_res.trYMinF
  py[1::5] = numpy.take(rain3h_sum, ind_above_zero)
  py[2::5] = numpy.take(rain3h_sum, ind_above_zero)
  py[3::5] = rain3h_res.trYMinF
  py[4::5] = rain3h_res.trYMinF
  Ngl.add_polygon(wks, rainhist, px, py, pgres)
  return rainhist

# function to add axis labels, major and minor tickmarks to the x axis
def config_xaxis_legend(res, main_hours, sec_hours, labels):
  res.tmXBValues = numpy.array(main_hours)
  res.tmXBMinorValues = numpy.array(sec_hours)
  res.tmXBLabels = labels
  return res

# function to replace supporting characters and special characters in the head string
def format_title(head, timestamp):
  head = head.replace("_", " ")
  head = head.replace("ö", "oe")
  head = head.replace("ä", "ae")
  head = head.replace("ü", "ue")
  head = head.replace("ß", "ss")
  return head + " (%s)" % timestamp.strftime("%b %d %Y %HUTC")

# function to create the meteogram for the given location
def create_meteogram_for(filepath, filename, timestamp):
  with open(filepath + filename) as f:
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

  # set up a color map and open an output workstation.
  colors = numpy.array([                                                \
                           [255,255,255], [255,255,255], [255,255,255], \
                           [240,255,240], [220,255,220], [190,255,190], \
                           [120,255,120], [ 80,255, 80], [ 50,200, 50], \
                           [ 20,150, 20]                                \
                         ],'f') / 255.
  wks_type = "png"
  output_file = filepath + timestamp.strftime("%m_%d_%H") + "_meteogram_" + filename.split(".")[0]
  wks = Ngl.open_wks(wks_type, output_file)

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
  sealevel_pressure = pressure_lib.reduce_pressure_to_sealevel(pressure, cdf[:, 5], float(head[13]))
  pres_res = pressure_lib.get_pressure_resource(count_xdata, sealevel_pressure)
  pres_res.tiMainString = format_title(head[0] ,timestamp)
  pres_res = config_xaxis_legend(pres_res, main_hours, sec_hours, labels)
  
  # relative humidity
  relhum_res = humidity_lib.get_relhumidity_resource(count_xdata)
  relhum_res = config_xaxis_legend(relhum_res, main_hours, sec_hours, labels)

  # wind speed recource
  wind_res = wind_lib.get_windspeed_resource(count_xdata, wind_speed)
  wind_res= config_xaxis_legend(wind_res, main_hours, sec_hours, labels)
  
  # wind direction recource
  direction_res = wind_lib.get_winddirection_resource(count_xdata, wind_speed)
  direction_res = config_xaxis_legend(direction_res, main_hours, sec_hours, labels)

  # rain sum resources
  rainsum_res = rain_lib.get_rainsum_resource(count_xdata)
  rainsum_res = config_xaxis_legend(rainsum_res, main_hours, sec_hours, labels)

  # 3 hour rain sum bar charts
  rain3h_res = rain_lib.get_3hrain_resource(rain3h_time)
  rainhist  = create_rain_bar_plot(wks, rain3h_time, rain3h_sum, rain3h_res)
  
  # ground temperature resource
  tempsfc_res = temperature_lib.get_temperature_resource(count_xdata, tempht, dew_point)
  tempsfc_res = config_xaxis_legend(tempsfc_res, main_hours, sec_hours, labels)

  # generate plot results
  pressmsz  = Ngl.xy(wks,taus,sealevel_pressure,pres_res)
  relhummsz = Ngl.xy(wks,taus,rel_hum,relhum_res)
  windmsz   = Ngl.xy(wks,taus,wind_speed,wind_res)
  dirmsz    = Ngl.xy(wks,taus,wind_direction,direction_res)
  rainsum   = Ngl.xy(wks,taus,rain_sum,rainsum_res)
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
