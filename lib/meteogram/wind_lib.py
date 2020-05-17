import Ngl
import math
import numpy

# function to create the plot resource for the wind speed plot of the meteogram
def get_windspeed_resource(count_xdata, wind_speed):
  wind_res = Ngl.Resources()
  wind_res.vpXF            = 0.15       # The left side of the box location
  wind_res.vpYF            = 0.45       # The top side of the plot box loc
  wind_res.vpWidthF        = 0.75       # The Width of the plot box
  wind_res.vpHeightF       = 0.10       # The height of the plot box
  wind_res.trXMaxF         = count_xdata  # max value on x-axis
  wind_res.trYMaxF         = math.ceil(numpy.amax(wind_speed))   # max value on y-axis
  wind_res.trYMinF         = 0.0                     # min value on y-axis

  wind_res.tiXAxisString  = ""            # turn off x-axis string
  wind_res.tiYAxisString  = "wind sp. (m/s)"  # set y-axis string
  wind_res.tiYAxisFontHeightF = 0.015          # Y axes font height.
  wind_res.tmXTOn         = False         # turn off the top tickmarks
  wind_res.tmXBMode       = "Explicit"
  #wind_res.tmXBValues     = ticks
  #wind_res.tmXBLabels     = time_array
  #wind_res.tmXBMinorValues = sticks
  wind_res.tmXMajorGrid = True
  wind_res.tmXMajorGridLineDashPattern = 2
  wind_res.tmYLMaxTicks = 6

  wind_res.xyLineThicknesses = 2          # increase line thickness
  wind_res.xyLineColor    =  "green"      # set line color

  wind_res.nglDraw         = False     # Don't draw individual plot.
  wind_res.nglFrame        = False     # Don't advance frame.
  wind_res.nglMaximize     = False     # Do not maximize plot in frame
  return wind_res

# function to calculate the wind speed from the two dimensional components u and v
def calculate_windspeed(u, v, data_size):
  wind_speed = numpy.empty(data_size)

  for i in range(data_size):
    wind_speed[i] = math.sqrt(u[i]**2 + v[i]**2)
  return wind_speed