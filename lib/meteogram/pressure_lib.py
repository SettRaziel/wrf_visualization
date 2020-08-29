import Ngl
import math
import numpy

# function to reduce the station pressure to sea level using the barometric formula
# with the arithmetic mean of the temperature from the station and reduced to sea level
def reduce_pressure_to_sealevel(pressure, temperature, station_elevation):
  r_0 = 287.05 # J/(kg*K)
  g = 9.80665 # m/s^2
  sealevel_pressure = numpy.empty(len(pressure))

  for i, p in enumerate(pressure):
    t_m = temperature[i] + station_elevation / 200 # approx. dT = 1 K / 100 m
    sealevel_pressure[i] = p * math.exp((g * station_elevation)/(r_0 * t_m))

  return sealevel_pressure

# function to create the plot resource for the air pressure plot of the meteogram
def get_pressure_resource(count_xdata, pressure):
  pres_res = Ngl.Resources()
  pres_res.vpXF            = 0.15   # The left side of the box location
  pres_res.vpYF            = 0.9    # The top side of the plot box loc
  pres_res.vpWidthF        = 0.75   # The Width of the plot box
  pres_res.vpHeightF       = 0.10   # The height of the plot box
  pres_res.trXMaxF         = count_xdata          # max value on x-axis
  pres_res.trYMaxF         = numpy.amax(pressure)+1   # max value on y-axis
  pres_res.trYMinF         = numpy.amin(pressure)-1   # min value on y-axis
  pres_res.tiYAxisFontHeightF = 0.015          # Y axes font height.

  pres_res.tiXAxisString  = ""            # turn off x-axis string
  pres_res.tiYAxisString  = "p [hPa]"     # set y-axis string
  pres_res.tmXTOn         = False         # turn off the top tickmarks
  pres_res.tmXBMode       = "Explicit"
  pres_res.tmXMajorGrid = True
  pres_res.tmXMajorGridLineDashPattern = 2
  pres_res.tmYLMaxTicks = 6

  pres_res.xyLineThicknesses = 3          # increase line thickness
  pres_res.xyLineColor       = "blue"    # set line color
  pres_res.tmYMajorGrid      = True
  pres_res.tmYLMajorThicknessF = 0.1

  pres_res.nglDraw         = False     # Don't draw individual plot.
  pres_res.nglFrame        = False     # Don't advance frame.
  pres_res.nglMaximize     = False     # Do not maximize plot in frame
  return pres_res
