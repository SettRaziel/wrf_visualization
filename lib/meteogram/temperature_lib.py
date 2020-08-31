import Ngl
import math
import numpy
import validation_lib

# function to perform a sanity check for the extreme values of the air temperature
def check_tempreature_boundaries(lower, upper):
  maximum = 60.0 # since highest measured temperature: 56.7°C, California; 1913
  minimum = -90.0 # since lowest measured temperature: -89.2°C, Antartica; 1983

  validation_lib.check_upper_boundary(upper, maximum, "°C")
  validation_lib.check_lower_boundary(lower, minimum, "°C")

# function to create the plot resource for the temperature plot of the meteogram
def get_temperature_resource(count_xdata, tempht, dew_point):

  # sanity check for temperature range
  upper_boundary = numpy.amax(tempht)
  lower_boundary = numpy.amin(dew_point)
  check_tempreature_boundaries(lower_boundary, upper_boundary)

  tempsfc_res = Ngl.Resources()
  tempsfc_res.vpXF            = 0.15   # The left side of the box
  tempsfc_res.vpYF            = 0.15   # The top side of the plot box
  tempsfc_res.vpWidthF        = 0.75   # The Width of the plot box
  tempsfc_res.vpHeightF       = 0.10   # The height of the plot box

  tempsfc_res.tiXAxisString      = ""             # X axes label.
  tempsfc_res.tiYAxisFontHeightF = 0.015          # Y axes font height.
  tempsfc_res.tiYAxisString      = "T / Td [*C]"   # Y axis label.

  tempsfc_res.tmXBMode           = "Explicit"     # Define own tick mark labels.
  tempsfc_res.tmXMajorGrid       = True
  tempsfc_res.tmXMajorGridLineDashPattern = 2
  tempsfc_res.tmYMajorGrid = True
  tempsfc_res.tmYLMaxTicks = 6
  tempsfc_res.tmXTOn             = False          # turn off the top tickmarks

  tempsfc_res.trXMaxF         = count_xdata   # max value on x-axis
  tempsfc_res.trYMaxF         = math.ceil(upper_boundary)
  tempsfc_res.trYMinF         = math.floor(lower_boundary)
  tempsfc_res.tmYLMajorThicknessF = 0.1

  tempsfc_res.xyLineThicknesses  = 2
  tempsfc_res.xyLineColor        =  "red"

  tempsfc_res.nglDraw         = False     # Don't draw individual plot.
  tempsfc_res.nglFrame        = False     # Don't advance frame.
  tempsfc_res.nglMaximize     = False     # Do not maximize plot in frame
  return tempsfc_res

# function to calculate the dewpoint from the meteogram data
def calculate_dewpoint(temperature, relative_humidity, data_size):
  dew_point = numpy.empty(data_size)

  for i in range(data_size):
    if (relative_humidity[i] == 100.):
      dew_point[i] = temperature[i]
    else:
      dew_point[i] = temperature[i] - ((100. - relative_humidity[i])/ 5.0)
  return dew_point
