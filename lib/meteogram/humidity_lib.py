import Ngl
import math
import numpy

# function to calculate the relative humidity from the meteorological data
def calculate_relative_humidity(humidity, temperature, pressure, data_size):
  rel_hum = numpy.empty(data_size)

  for i in range(data_size):
    saturation_pressure = 6.1094 * math.exp((17.685 * temperature[i]) / (temperature[i] + 243.04))
    partial_pressure = 0.622 * saturation_pressure / pressure[i]
    rel_hum_pre = humidity[i] * 100 / partial_pressure
    rel_hum[i] = min(rel_hum_pre, 100.)
  return rel_hum