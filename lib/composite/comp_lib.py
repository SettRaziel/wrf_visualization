from __future__ import print_function
import numpy, Nio, Ngl, os, sys
from wrf import getvar, get_pyngl, smooth2d, latlon_coords, to_np
import pressure_lib

# function to retrieve the latitude wind component from the input data
def get_latitude_wind(wrf_data):
  u10 = getvar(wrf_data,"U10")                    # Get 10m u component
  return u10

# function to retrieve the longitude wind component from the input data
def get_longitude_wind(wrf_data):
  v10 = getvar(wrf_data,"V10")                    # Get 10m v component
  return v10

# function to generate the output image for the given timestep
def print_comp_for_timestamp(wrf_data, timestring):
  slp = pressure_lib.get_sea_level_pressure(wrf_data)
  temperature = getvar(wrf_data,"tc")
  u = get_latitude_wind(wrf_data)
  v = get_longitude_wind(wrf_data)

  lat, lon = latlon_coords(temperature)
  lat_normal = to_np(lat)
  lon_normal = to_np(lon)
  
  # temperature
  t_res = get_pyngl(temperature)
  t_res.nglDraw             = False                  # don't draw plot
  t_res.nglFrame            = False                  # don't advance frame
  
  t_res.cnFillOn            = True                   # turn on contour fill
  t_res.cnLinesOn           = False                  # turn off contour lines
  t_res.cnLineLabelsOn      = False                  # turn off line labels
  t_res.cnFillMode          = "RasterFill"           # These two resources
  #t_res.cnFillPalette       = "ncl_default"
  t_res.cnFillPalette       = "BlAqGrYeOrReVi200"
  
  t_res.mpGeophysicalLineColor = "black"
  t_res.mpGeophysicalLineThicknessF = 5
  t_res.mpNationalLineColor = "gray75"
  t_res.mpNationalLineThicknessF = 5
  t_res.mpDataBaseVersion   = "MediumRes"
  t_res.pmLabelBarHeightF   = 0.08
  t_res.pmLabelBarWidthF    = 0.65
  
  t_res.lbTitleString       = "%s in (%s)" % (temperature.description,temperature.units)
  t_res.lbOrientation       = "horizontal"
  t_res.lbTitleFontHeightF  = 0.015
  t_res.lbLabelFontHeightF  = 0.015                  
  
  t_res.tiMainString        = "Composite (%s)" % timestring
  t_res.trGridType          = "TriangularMesh"       # can speed up plotting.
  t_res.tfDoNDCOverlay      = True                   # required for native projection

  # pressure
  p_res = pressure_lib.get_pressure_resource(lat_normal, lon_normal)
  
  # wind
  uv_res = Ngl.Resources()
  uv_res.nglDraw            =  False                # don't draw plot
  uv_res.nglFrame           =  False                # don't advance frame
  
  uv_res.vcFillArrowsOn     = True
  uv_res.vcRefMagnitudeF    = 15.0
  uv_res.vcRefLengthF       = 0.03
  uv_res.vcMinDistanceF     = 0.02
  uv_res.vcRefAnnoFontHeightF = 0.01
  uv_res.vcRefAnnoString1 = "$VMG$ m/s"
  uv_res.vcRefAnnoString2 = "ground windspeed (m/s) reference"
  
  uv_res.vfXArray           =  lon_normal
  uv_res.vfYArray           =  lat_normal

  wk_res = Ngl.Resources()
  wk_res.wkWidth = 2500
  wk_res.wkHeight = 2500
  wks_comp = Ngl.open_wks("png","comp_test", wk_res)

  # creating plots for the measurands
  tplot = Ngl.contour_map(wks_comp,temperature[0,:,:],t_res)
  pplot = Ngl.contour(wks_comp,slp,p_res)
  vector = Ngl.vector(wks_comp,u,v,uv_res)

  Ngl.overlay(tplot, pplot)
  Ngl.overlay(tplot, vector)
  Ngl.maximize_plot(wks_comp, tplot)
  Ngl.draw(tplot)
  Ngl.frame(wks_comp)
  Ngl.delete_wks(wks_comp) # delete currently used workstation