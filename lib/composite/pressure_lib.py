import Ngl
from wrf import getvar, smooth2d

# function to retrieve the sea level pressure from the input data
def get_sea_level_pressure(wrf_data):
  slp = getvar(wrf_data,"slp")                    # sea level pressure (2D)
  slp = smooth2d(slp, 3)                          # Smooth sea level pressure
  return slp

# function to create the plot resource for the air pressure plot of the composites
def get_pressure_resource(lat, lon):
  p_res = Ngl.Resources()
  p_res.nglDraw             =  False                 # don't draw plot
  p_res.nglFrame            =  False                 # don't advance frame
  
  p_res.cnHighLabelsOn      = True                   # Set labels
  p_res.cnLowLabelsOn       = True
  p_res.cnLineThicknessF    = 5
  p_res.cnMonoLineColor     = True                     
  p_res.cnLineColor         = "black"
  p_res.cnLineLabelInterval = 4
  p_res.cnInfoLabelString   = "pressure (hPa) from $CMN$ to $CMX$ by $CIU$ hPa"
  
  p_res.sfXArray            =  lon
  p_res.sfYArray            =  lat
  return p_res
