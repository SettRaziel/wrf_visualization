import Ngl
import math
import numpy

# function to create the plot resource for the rain sum plot of the meteogram
def get_rainsum_resource(taus):
  rainsum_res = Ngl.Resources()
  rainsum_res.vpXF            = 0.15   # The left side of the box
  rainsum_res.vpYF            = 0.3   # The top side of the plot box
  rainsum_res.vpWidthF        = 0.75   # The Width of the plot box
  rainsum_res.vpHeightF       = 0.10   # The height of the plot box
  rainsum_res.trYAxisType     = "IrregularAxis"
  rainsum_res.xyYIrregularPoints = [ 0, 1, 2, 3, 4, 8, 16, 35 ]
  rainsum_res.trYAxisType     = 0.0    # min value on y-axis
  rainsum_res.trYMaxF         = 35    # max value on y-axis
  rainsum_res.trXMinF         = 0.0
  rainsum_res.trXMaxF         = taus[-1]   # max value on x-axis

  rainsum_res.tiXAxisString   = ""            # X axes label.
  rainsum_res.tiYAxisFontHeightF = 0.015          # Y axes font height.
  rainsum_res.tiYAxisString   = "3hr rain total"  # Y axis label.
  rainsum_res.tmXTOn          = False      # turn off the top tickmarks
  rainsum_res.tmXBMode        = "Explicit"    # Define own tick mark labels.
  #rainsum_res.tmXBValues      = taus
  #rainsum_res.tmXBLabels      = taus
  rainsum_res.tmXBMinorOn     = False      # No minor tick marks.

  rainsum_res.tmXMajorGrid    = True
  rainsum_res.tmXMajorGridLineDashPattern = 2
  rainsum_res.tmYLMode        = "Explicit"
  rainsum_res.tmYLValues      = [ 0, 2, 4, 10, 30 ]
  rainsum_res.tmYLLabels      = [ 0, 2, 4, 10, 30 ]
  rainsum_res.tmYLMinorValues = [ 1, 3, 5, 20 ]

  rainsum_res.tmYMajorGrid   = True
  rainsum_res.xyLineThicknesses = 2          # increase line thickness
  rainsum_res.nglYRefLine     = 0.0             # create a reference line
  rainsum_res.xyLineColor     =  "blue"       # set line color

  rainsum_res.nglDraw         = False     # Don't draw individual plot.
  rainsum_res.nglFrame        = False     # Don't advance frame.
  rainsum_res.nglMaximize     = False     # Do not maximize plot in frame
  return rainsum_res

# function to create the plot resource for the 3h rain plot of the meteogram
def get_3hrain_resource(rain3h_time):
  rain3h_res  = Ngl.Resources()
  rain3h_res.trXMinF         = 0.0
  rain3h_res.trXMaxF         = len(rain3h_time)
  rain3h_res.trYMinF         = 0.0
  rain3h_res.trYMaxF         = 35
  rain3h_res.trYAxisType     = "IrregularAxis"
  rain3h_res.xyYIrregularPoints = [ 0, 1, 2, 3, 4, 8, 16, 35 ]
  rain3h_res.tmXBMode        = "Explicit"    # Define own tick mark labels.
  rain3h_res.tmXBValues      = rain3h_time
  rain3h_res.tmXBLabels      = rain3h_time

  rain3h_res.tiXAxisString  = ""            # turn off x-axis string
  rain3h_res.tmXTOn         = False         # turn off the top tickmarks
  rain3h_res.xyLineThicknesses = 2          # increase line thickness
  rain3h_res.gsnAboveYRefLineColor = "green"    # above ref line fill green
  rain3h_res.gsnXYBarChart   = True             # turn on bar chart
  rain3h_res.tmYLMaxTicks = 6

  rain3h_res.nglDraw         = False     # Don't draw individual plot.
  rain3h_res.nglFrame        = False     # Don't advance frame.
  rain3h_res.nglMaximize     = False     # Do not maximize plot in frame
  return rain3h_res

# function to calculate the values and time stamps for the 3 hour rain sums
def calculate_3hrain_data(rain_sum, taus):
  rain3h_time = numpy.empty(int(taus[-1] / 3))
  rain3h_time[0] = 3
  rain3h_sum = numpy.empty(len(rain3h_time))

  j = 0
  rain_prev = 0.0
  rain_act = rain_sum[0]
  for i in range(len(taus)):
    if (taus[i] > rain3h_time[j]):
        rain_prev = rain_act
        rain_act = rain_sum[i]
        rain3h_sum[j] = rain_act - rain_prev
        j = j + 1
        rain3h_time[j] = rain3h_time[j-1] + 3
  rain3h_sum[-1] = rain_act - rain_prev

  return rain3h_sum, rain3h_time