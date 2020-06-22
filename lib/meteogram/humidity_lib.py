import Ngl
import math
import numpy

# function to create the plot resource for the relative humidity plot of the meteogram
def get_relhumidity_resource(count_xdata):
  relhum_res = Ngl.Resources()
  relhum_res.vpXF            = 0.15   # The left side of the box
  relhum_res.vpYF            = 0.75   # The top side of the plot box
  relhum_res.vpWidthF        = 0.75   # The Width of the plot box
  relhum_res.vpHeightF       = 0.10   # The height of the plot box
  
  relhum_res.gsnYRefLine = 0.1
  relhum_res.gsnAboveYRefLineColor = "dark green"

  relhum_res.tiXAxisString      = ""             # X axes label.
  relhum_res.tiYAxisFontHeightF = 0.015          # Y axes font height.
  relhum_res.tiYAxisString      = "rel. humidity"   # Y axis label.

  relhum_res.tmXBMode           = "Explicit"     # Define own tick mark labels.
  relhum_res.tmXMajorGrid       = True
  relhum_res.tmXMajorGridLineDashPattern = 2
  relhum_res.tmYMajorGrid = True
  relhum_res.tmYLMaxTicks = 6
  relhum_res.tmXTOn             = False          # turn off the top tickmarks

  relhum_res.trXMaxF         = count_xdata   # max value on x-axis
  relhum_res.trYMaxF         = 100
  relhum_res.trYMinF         = 0.0
  relhum_res.tmYLMajorThicknessF = 0.1

  relhum_res.xyLineThicknesses  = 3
  relhum_res.xyLineColor        =  "dark green"

  relhum_res.nglDraw         = False     # Don't draw individual plot.
  relhum_res.nglFrame        = False     # Don't advance frame.
  relhum_res.nglMaximize     = False     # Do not maximize plot in frame
  
  return relhum_res

# function to calculate the relative humidity from the meteorological data
def calculate_relative_humidity(humidity, temperature, pressure, data_size):
  rel_hum = numpy.empty(data_size)

  for i in range(data_size):
    saturation_pressure = 6.1094 * math.exp((17.685 * temperature[i]) / (temperature[i] + 243.04))
    partial_pressure = 0.622 * saturation_pressure / pressure[i]
    rel_hum_pre = humidity[i] * 100 / partial_pressure
    rel_hum[i] = min(rel_hum_pre, 100.)
  return rel_hum
