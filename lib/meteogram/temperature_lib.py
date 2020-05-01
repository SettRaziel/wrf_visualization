import Ngl
import math
import numpy

# function to create the plot resource for the temperature plot of the meteogram
def get_temperature_resource(tempht, dew_point):
  tempsfc_res = Ngl.Resources()
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
  tempsfc_res.trYMaxF         = math.ceil(numpy.amax(tempht))
  tempsfc_res.trYMinF         = math.floor(numpy.amin(dew_point))

  tempsfc_res.xyLineThicknesses  = 2
  tempsfc_res.xyLineColor        =  "red"

  tempsfc_res.nglDraw         = False     # Don't draw individual plot.
  tempsfc_res.nglFrame        = False     # Don't advance frame.
  tempsfc_res.nglMaximize     = False     # Do not maximize plot in frame
  return tempsfc_res