import Ngl
import math
import numpy

# function to create the plot resource for the wind speed plot of the meteogram
def get_windspeed_resource(count_xdata, wind_speed):

  # sanity check for wind speed range
  upper_boundary = numpy.amax(wind_speed)
  check_windspeed_boundaries(upper_boundary)

  wind_res = Ngl.Resources()
  wind_res.vpXF            = 0.15       # The left side of the box location
  wind_res.vpYF            = 0.45       # The top side of the plot box loc
  wind_res.vpWidthF        = 0.75       # The Width of the plot box
  wind_res.vpHeightF       = 0.10       # The height of the plot box
  wind_res.trXMaxF         = count_xdata  # max value on x-axis
  wind_res.trYMaxF         = math.ceil(upper_boundary)   # max value on y-axis
  wind_res.trYMinF         = 0.0                     # min value on y-axis

  wind_res.tiXAxisString  = ""            # turn off x-axis string
  wind_res.tiYAxisString  = "wind sp. [m/s]"  # set y-axis string
  wind_res.tiYAxisFontHeightF = 0.015          # Y axes font height.
  wind_res.tmXTOn         = False         # turn off the top tickmarks
  wind_res.tmXBMode       = "Explicit"
  wind_res.tmXMajorGrid = True
  wind_res.tmXMajorGridLineDashPattern = 2
  wind_res.tmYLMaxTicks = 6

  wind_res.xyLineThicknesses = 2          # increase line thickness
  wind_res.xyLineColor    =  "green"      # set line color

  wind_res.nglDraw         = False     # Don't draw individual plot.
  wind_res.nglFrame        = False     # Don't advance frame.
  wind_res.nglMaximize     = False     # Do not maximize plot in frame
  return wind_res

# function to create the plot resource for the wind speed plot of the meteogram
def get_winddirection_resource(count_xdata, wind_direction):
  direction_res = Ngl.Resources()
  direction_res.vpXF            = 0.15       # The left side of the box location
  direction_res.vpYF            = 0.6        # The top side of the plot box loc
  direction_res.vpWidthF        = 0.75       # The Width of the plot box
  direction_res.vpHeightF       = 0.10       # The height of the plot box
  direction_res.trXMaxF         = count_xdata  # max value on x-axis
  direction_res.trYMaxF         = 360.0   # max value on y-axis
  direction_res.trYMinF         = 0.0                     # min value on y-axis

  direction_res.tiXAxisString  = ""            # turn off x-axis string
  direction_res.tiYAxisString  = "wind dir. [deg.]"  # set y-axis string
  direction_res.tiYAxisFontHeightF = 0.015          # Y axes font height.
  direction_res.tmXTOn         = False         # turn off the top tickmarks
  direction_res.tmXBMode       = "Explicit"
  direction_res.tmXMajorGrid = True
  direction_res.tmXMajorGridLineDashPattern = 2
  direction_res.tmYLMode       = "Explicit"
  direction_res.tmYLValues     = [ 0, 90, 180, 270 ]
  direction_res.tmYLLabels     = ["N", "E", "S", "W"]
  direction_res.tmYLMinorValues = [ 45, 135, 225, 315 ]

  direction_res.xyLineThicknesses = 2          # increase line thickness
  direction_res.xyMarkLineMode = "Markers"
  direction_res.xyMarkers      = 10
  direction_res.xyMarkerColor  = "purple"
  direction_res.xyMarkerSizeF  = 0.001

  direction_res.nglDraw         = False     # Don't draw individual plot.
  direction_res.nglFrame        = False     # Don't advance frame.
  direction_res.nglMaximize     = False     # Do not maximize plot in frame
  return direction_res

# function to perform a sanity check for the extreme values of the wind speed
def check_windspeed_boundaries(upper):
  maximum = 40.0 # since 12 bft is for wind speed > 32 m/s

  if (upper > maximum):
    raise ValueError("%s is higher than the current max boundary: %sm/s" % (upper, maximum))

# function to calculate the wind speed from the two dimensional components u and v
def calculate_windspeed(u, v, data_size):
  wind_speed = numpy.empty(data_size)

  for i in range(data_size):
    wind_speed[i] = math.sqrt(u[i]**2 + v[i]**2)
  return wind_speed

# function to calculate the wind speed from the two dimensional components u and v
def calculate_winddirection(u, v, data_size):
  wind_direction = numpy.empty(data_size)

  for i in range(data_size):
    wind_direction[i] = math.degrees(math.atan2(u[i], v[i])) + 180.

  return wind_direction
