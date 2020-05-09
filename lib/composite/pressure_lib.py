import Ngl

# function to create the plot resource for the air pressure plot of the composites
def get_pressure_resource(lat, lon):
  p_res = Ngl.Resources()
  p_res.nglDraw             =  False                 # don't draw plot
  p_res.nglFrame            =  False                 # don't advance frame
  
  p_res.cnHighLabelsOn      = True                   # Set labels
  p_res.cnLowLabelsOn       = True
  p_res.cnLineThicknessF    = 2
  p_res.cnMonoLineColor     = True                     
  p_res.cnLineColor         = "gray50"
  p_res.cnLineLabelInterval = 4
  p_res.cnInfoLabelString   = "pressure (hPa) from $CMN$ to $CMX$ by $CIU$ hPa"
  
  p_res.sfXArray            =  lon
  p_res.sfYArray            =  lat
  return p_res
