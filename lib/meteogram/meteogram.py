from __future__ import print_function
import copy
#  Import Nio.
import Nio
#  Import numpy, sys, os.
import numpy, sys, os
#  Import the PyNGL module names.
import Ngl

#  Main program.

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

# Create a different resource list for every plot created.
rainsum_res = Ngl.Resources()
tempsfc_res = Ngl.Resources()

# rain sum resources
rainsum_res.nglFrame        = False
rainsum_res.vpXF            = 0.15   # The left side of the box
rainsum_res.vpYF            = 0.3   # The top side of the plot box
rainsum_res.vpWidthF        = 0.75   # The Width of the plot box
rainsum_res.vpHeightF       = 0.10   # The height of the plot box
rainsum_res.trYAxisType     = "IrregularAxis"
rainsum_res.xyYIrregularPoints = [ 0, 1, 2, 3, 4, 8, 16, 35 ]
rainsum_res.trYAxisType     = 0.0    # min value on y-axis
rainsum_res.trYMaxF         = 35    # max value on y-axis
rainsum_res.trXMinF         = 0.0
#rainsum_res.trXMaxF         = taus(dimsizes(taus) - 1)   ; max value on x-axis

rainsum_res.tiXAxisString   = ""            # X axes label.
rainsum_res.tiYAxisFontHeightF = 0.015          # Y axes font height.
rainsum_res.tiYAxisString   = "3hr rain total"  # Y axis label.
rainsum_res.tmXTOn          = False      # turn off the top tickmarks
rainsum_res.tmXBMode        = "Explicit"    # Define own tick mark labels.
#rainsum_res.tmXBValues     = taus
#rainsum_res.tmXBLabels     = taus
rainsum_res.tmXBLabelFont   = "Times-Bold"  # Change the font.
rainsum_res.tmYLLabelFont   = "Times-Bold"  # Change the font.
rainsum_res.tmXBMinorOn     = False      # No minor tick marks.

rainsum_res.tmXMajorGrid    = True
rainsum_res.tmXMajorGridLineDashPattern = 2
rainsum_res.tmYLMode        = "Explicit"
rainsum_res.tmYLValues      = [ 0, 2, 4, 10, 30 ]
rainsum_res.tmYLLabels      = [ 0, 2, 4, 10, 30 ]
rainsum_res.tmYLMinorValues = [ 1, 3, 5, 20 ]

rainsum_res.tmYMajorGrid   = True
rainsum_res.xyLineThicknesses = 2          # increase line thickness
rainsum_res.gsnDraw         = False        # Don't draw individual plot.
rainsum_res.gsnFrame        = False        # Don't advance frame.
rainsum_res.gsnYRefLine     = 0.0             # create a reference line
rainsum_res.xyLineColor     =  "blue"       # set line color

rainsum_res.nglMaximize     = False     # Do not maximize plot in frame

# ground temperature resource
tempsfc_res.vpXF            = 0.15   # The left side of the box
tempsfc_res.vpYF            = 0.15   # The top side of the plot box
tempsfc_res.vpWidthF        = 0.75   # The Width of the plot box
tempsfc_res.vpHeightF       = 0.10   # The height of the plot box

tempsfc_res.tiXAxisString      = ""             # X axes label.
tempsfc_res.tiYAxisFontHeightF = 0.015          # Y axes font height.
tempsfc_res.tiYAxisString      = "Temp at 2m"   # Y axis label.

tempsfc_res.tmXBMode           = "Explicit"     # Define own tick mark labels.
tempsfc_res.tmXBLabelFont      = "Times-Bold"   # Change the font.
tempsfc_res.tmYLLabelFont      = "Times-Bold"   # Change the font.
#tempsfc_res.tmXBValues         = taus
#tempsfc_res.tmXBLabels         = taus
#tempsfc_res@tmXBValues     = ticks TODO
#tempsfc_res@tmXBLabels     = time_array TODO
tempsfc_res.tmXMajorGrid       = True
tempsfc_res.tmXMajorGridLineDashPattern = 2
#tempsfc_res@tmXBMinorValues = sticks TODO
tempsfc_res.tmYMajorGrid = True
tempsfc_res.tmYLMaxTicks = 6
tempsfc_res.tmXTOn             = False          # turn off the top tickmarks

#tempsfc_res@trXMaxF         = taus(dimsizes(taus) - 1)   ; max value on x-axis
#tempsfc_res.trYMaxF         = numpy.amax(tempht)+0.5
#tempsfc_res.trYMinF         = numpy.amin(tempht)-0.5

tempsfc_res.xyLineThicknesses  = 2
tempsfc_res.xyLineColor        =  "red"

tempsfc_res.nglDraw         = False     # Don't draw individual plot.
tempsfc_res.nglFrame        = False     # Don't advance frame.
tempsfc_res.nglMaximize     = False     # Do not maximize plot in frame 

# generate plot results
rainsum   = Ngl.xy(wks,taus,rain_sum,rainsum_res)
temptmsz  = Ngl.xy(wks,taus,tempht,tempsfc_res)

Ngl.draw(rainsum)
Ngl.draw(temptmsz)
Ngl.frame(wks)

Ngl.end()
