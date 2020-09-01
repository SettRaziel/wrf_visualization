import numpy

# function to determine the extreme values of a data set and check if they are inside the given interval
def get_and_check_boundaries(measurand, upper_boundary, lower_boundary, unit_string):
  data_maximum = numpy.amax(measurand)
  data_minimum = numpy.amin(measurand)

  check_upper_boundary(data_maximum, upper_boundary, unit_string)
  check_lower_boundary(data_minimum, lower_boundary, unit_string)
  return data_minimum, data_maximum

# function to perform a sanity check for an upper boundary value
def check_upper_boundary(value, boundary, unit_string):
  if (value > boundary):
    raise ValueError("%s is higher than the current max boundary: %s%s" % (value, boundary, unit_string))

# function to perform a sanity check for an lower boundary value
def check_lower_boundary(value, boundary, unit_string):
  if (value < boundary):
    raise ValueError("%s is lower than the current min boundary: %s%s" % (value, boundary, unit_string))
