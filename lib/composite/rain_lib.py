from __future__ import print_function
import numpy, Nio, Ngl, os, sys
from wrf import getvar, get_pyngl, smooth2d, latlon_coords, to_np
import pressure_lib, geography_lib

# function to get and add the rain data layers
def get_cumulated_rain_sum(wrf_data):
  rain_exp = getvar(wrf_data,"RAINNC")
  rain_con = getvar(wrf_data,"RAINC")
  return rain_exp + rain_con, rain_con

# function to initialize and return the rain resource
def initialize_rain_resource(rain_con):
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
  
  rr_res = geography_lib.initialize_geography(rr_res, "gray50")
  return rr_res

# function to generate the total rain sum output image
def print_total_rainsum_for_timestamp(wrf_data, timestamp, filepath):
  slp = pressure_lib.get_sea_level_pressure(wrf_data)
  rain_sum, rain_con = get_cumulated_rain_sum(wrf_data)
  
  lat, lon = latlon_coords(rain_con)
  lat_normal = to_np(lat)
  lon_normal = to_np(lon)

  # rain sum
  rr_res = initialize_rain_resource(rain_con)
  
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
  output_path = "%srain_total_%s" % (filepath, timestamp.strftime("%Y_%m_%d_%H"))
  wks_comp = Ngl.open_wks("png", output_path, wk_res)
  
  # creating plots for the measurands
  rrplot = Ngl.contour_map(wks_comp,rain_sum,rr_res)
  pplot = Ngl.contour(wks_comp,slp,p_res)
  
  Ngl.overlay(rrplot, pplot)
  Ngl.maximize_plot(wks_comp, rrplot)
  Ngl.draw(rrplot)
  Ngl.frame(wks_comp)
  Ngl.delete_wks(wks_comp) # delete currently used workstation

# function to generate the 3h rain sum output image
def get_3h_rainsum(previous_data, current_data, timestamp, filepath):
  slp = pressure_lib.get_sea_level_pressure(current_data)
  previous_sum, rain_con = get_cumulated_rain_sum(previous_data)
  current_sum, rain_con = get_cumulated_rain_sum(current_data)
  rain_sum = current_sum - previous_sum

  lat, lon = latlon_coords(rain_con)
  lat_normal = to_np(lat)
  lon_normal = to_np(lon)

  # rain sum
  rr_res = initialize_rain_resource(rain_con)
  
  rr_res.lbTitleString       = "3h rainsum in (mm)"
  rr_res.lbOrientation       = "horizontal"
  rr_res.lbTitleFontHeightF  = 0.015
  rr_res.lbLabelFontHeightF  = 0.015                  
  
  rr_res.tiMainString        = "3h rainsum (%s)" % timestamp.strftime("%b %d %Y %HUTC")
  rr_res.trGridType          = "TriangularMesh"       # can speed up plotting.
  rr_res.tfDoNDCOverlay      = True                   # required for native projection

  # pressure
  p_res = pressure_lib.get_pressure_resource(lat_normal, lon_normal)

  wk_res = Ngl.Resources()
  wk_res.wkWidth = 2500
  wk_res.wkHeight = 2500
  output_path = "%srain_3h_%s" % (filepath, timestamp.strftime("%Y_%m_%d_%H"))
  wks_comp = Ngl.open_wks("png", output_path, wk_res)
  
  # creating plots for the measurands
  rrplot = Ngl.contour_map(wks_comp,rain_sum,rr_res)
  pplot = Ngl.contour(wks_comp,slp,p_res)
  
  Ngl.overlay(rrplot, pplot)
  Ngl.maximize_plot(wks_comp, rrplot)
  Ngl.draw(rrplot)
  Ngl.frame(wks_comp)
  Ngl.delete_wks(wks_comp) # delete currently used workstation
