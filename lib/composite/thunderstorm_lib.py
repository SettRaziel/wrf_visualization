from __future__ import print_function
import numpy, Nio, Ngl, os, sys
from wrf import getvar, get_pyngl, smooth2d, latlon_coords, to_np
import pressure_lib

# function to generate the output image for the given timestep
def print_cape_for_timestamp(wrf_data, timestamp):
  slp = pressure_lib.get_sea_level_pressure(wrf_data)
  cinfo = getvar(wrf_data,"cape_2d", missing=0.0)
  cape = cinfo[0,:,:].fillna(0)
  
  lat, lon = latlon_coords(slp)
  lat_normal = to_np(lat)
  lon_normal = to_np(lon)

  # rain sum
  cape_res = get_pyngl(cinfo)
  cape_res.nglDraw             = False                  # don't draw plot
  cape_res.nglFrame            = False                  # don't advance frame
  
  cape_res.cnFillOn            = True                   # turn on contour fill
  cape_res.cnLinesOn           = False                  # turn off contour lines
  cape_res.cnLineLabelsOn      = False                  # turn off line labels
  cape_res.cnFillMode          = "RasterFill"           # These two resources
  cape_res.cnLevelSelectionMode = "ExplicitLevels"
  cape_res.cnFillColors        = numpy.array([ [255,255,255], [  0,255,  0], [  0,128,  0], \
                                               [240,230,140], [255,255,  0], [255,140,  0], \
                                               [255,  0,  0], [139,  0,  0], [186, 85,211],\
                                               [153, 50,204], [139,  0,139], ],'f') / 255.
  cape_res.cnLevels            = numpy.array( [.1, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500 ])
  
  cape_res.mpGeophysicalLineColor = "black"
  cape_res.mpGeophysicalLineThicknessF = 5
  cape_res.mpNationalLineColor = "gray75"
  cape_res.mpNationalLineThicknessF = 5
  cape_res.mpDataBaseVersion   = "MediumRes"
  cape_res.pmLabelBarHeightF   = 0.08
  cape_res.pmLabelBarWidthF    = 0.65
  
  cape_res.lbTitleString       = "Convective available potential energy [CAPE] in (J/kg)"
  cape_res.lbOrientation       = "horizontal"
  cape_res.lbTitleFontHeightF  = 0.015
  cape_res.lbLabelFontHeightF  = 0.015                  
  
  cape_res.tiMainString        = "Thunderstorm probability (%s)" % timestamp.strftime("%b %d %Y %HUTC")
  cape_res.trGridType          = "TriangularMesh"       # can speed up plotting.
  cape_res.tfDoNDCOverlay      = True                   # required for native projection

  # pressure
  p_res = pressure_lib.get_pressure_resource(lat_normal, lon_normal)

  wk_res = Ngl.Resources()
  wk_res.wkWidth = 2500
  wk_res.wkHeight = 2500
  wks_comp = Ngl.open_wks("png","cape_%s" % timestamp.strftime("%Y_%m_%d_%H"), wk_res)

  # creating plots for the measurands
  capeplot = Ngl.contour_map(wks_comp,cape,cape_res)
  pplot = Ngl.contour(wks_comp,slp,p_res)
  
  Ngl.overlay(capeplot, pplot)
  Ngl.maximize_plot(wks_comp, capeplot)
  Ngl.draw(capeplot)
  Ngl.frame(wks_comp)
  Ngl.delete_wks(wks_comp) # delete currently used workstation
