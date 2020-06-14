from __future__ import print_function
import numpy, Nio, Ngl, os, sys

# function to set coastlines for the given resource with the given contour line color
def initialize_geography(resource, contour_color):
  resource.mpGeophysicalLineColor = contour_color
  resource.mpGeophysicalLineThicknessF = 5
  resource.mpNationalLineColor = "gray75"
  resource.mpNationalLineThicknessF = 5
  resource.mpDataBaseVersion   = "HighRes"
  resource.pmLabelBarHeightF   = 0.08
  resource.pmLabelBarWidthF    = 0.65
  return resource