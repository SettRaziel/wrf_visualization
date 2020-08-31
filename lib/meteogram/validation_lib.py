# function to perform a sanity check for an upper boundary value
def check_upper_boundary(value, boundary, unit_string):
  if (value > boundary):
    raise ValueError("%s is higher than the current max boundary: %s%s" % (value, boundary, unit_string))

# function to perform a sanity check for an lower boundary value
def check_lower_boundary(value, boundary, unit_string):
  if (value < boundary):
    raise ValueError("%s is lower than the current min boundary: %s%s" % (value, boundary, unit_string))
