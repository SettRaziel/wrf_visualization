from __future__ import print_function
import numpy, Nio, Ngl, os, sys
from wrf import getvar, get_pyngl, smooth2d, latlon_coords, to_np
import pressure_lib

# function to generate the output image for the given timestep
def print_total_rainsum_for_timestamp(wrf_data, timestamp):
  slp = pressure_lib.get_sea_level_pressure(wrf_data)
  rain_exp = getvar(wrf_data,"RAINNC")
  rain_con = getvar(wrf_data,"RAINC")
  rain_sum = rain_exp + rain_con
  
  lat, lon = latlon_coords(rain_con)
  lat_normal = to_np(lat)
  lon_normal = to_np(lon)

  # rain sum
  rr_res = get_pyngl(rain_con)
  rr_res.nglDraw             = False                  # don't draw plot
  rr_res.nglFrame            = False                  # don't advance frame
  
  rr_res.cnFillOn            = True                   # turn on contour fill
  rr_res.cnLinesOn           = False                  # turn off contour lines
  rr_res.cnLineLabelsOn      = False                  # turn off line labels
  rr_res.cnFillMode          = "RasterFill"           # These two resources
  rr_res.cnLevelSelectionMode = "ExplicitLevels"
  rr_res.cnFillColors        = numpy.array([ [255,255,255], [255,255,255], [152,251,152], \
                                             [127,255,  0], [ 50,205, 50], [  0,255,  0], \
                                             [  0,128,  0], [  0,100,  0], [255,255,  0], \
                                             [255,165,  0], [255, 69,  0], [139,  0,139], \
                                             [  0,  0, 255] ],'f') / 255.
  rr_res.cnLevels            = numpy.array( [ .1, .2, .4, .8, 1.6, 3.2, 6.4,  \
                                              12.8, 25.6, 51.2, 102.4, 204.8 ])
  
  rr_res.mpGeophysicalLineColor = "black"
  rr_res.mpGeophysicalLineThicknessF = 5
  rr_res.mpNationalLineColor = "gray75"
  rr_res.mpNationalLineThicknessF = 5
  rr_res.mpDataBaseVersion   = "MediumRes"
  rr_res.pmLabelBarHeightF   = 0.08
  rr_res.pmLabelBarWidthF    = 0.65
  
  rr_res.lbTitleString       = "Total rainsum in (mm)"
  rr_res.lbOrientation       = "horizontal"
  rr_res.lbTitleFontHeightF  = 0.015
  rr_res.lbLabelFontHeightF  = 0.015                  
  
  rr_res.tiMainString        = "Total rainsum (%s)" % timestamp.strftime("%b %d %Y %HUTC")
  rr_res.trGridType          = "TriangularMesh"       # can speed up plotting.
  rr_res.tfDoNDCOverlay      = True                   # required for native projection

  # pressure
  p_res = pressure_lib.get_pressure_resource(lat_normal, lon_normal)

  wk_res = Ngl.Resources()
  wk_res.wkWidth = 2500
  wk_res.wkHeight = 2500
  wks_comp = Ngl.open_wks("png","rainsum_%s" % timestamp.strftime("%Y_%m_%d_%H"), wk_res)

  # creating plots for the measurands
  rrplot = Ngl.contour_map(wks_comp,rain_sum,rr_res)
  pplot = Ngl.contour(wks_comp,slp,p_res)
  
  Ngl.overlay(rrplot, pplot)
  Ngl.maximize_plot(wks_comp, rrplot)
  Ngl.draw(rrplot)
  Ngl.frame(wks_comp)
  Ngl.delete_wks(wks_comp) # delete currently used workstation
