# WRF Forecast output visualization
[![Code Climate](https://codeclimate.com/github/SettRaziel/wrf_visualization/badges/gpa.svg)](https://codeclimate.com/github/SettRaziel/wrf_visualization)

Scripts and documentation to create visual output for a WRF model run.
Moving away from the ncar command language as announced [here](http://www.ncl.ucar.edu/Document/Pivot_to_Python/september_2019_update.shtml)
the main focus now stands on the usage of the corresponding python implementation for creating output from the WRF output results.

Current version: v0.1.8

## Sources
* [geocat](https://geocat.ucar.edu/pages/software.html)

## Components
As stated on the geocat home the new visualizations modules for getting wrf output are:
* [geocat-comp](https://github.com/NCAR/geocat-comp)
* [pyngl](https://github.com/NCAR/pyngl)
* [pynio](https://github.com/NCAR/pynio)
* [wrf-python](https://github.com/NCAR/wrf-python)

To install and use this modules in python the suggested way from the ncar is the [conda](https://conda.io/en/latest/)
package manager. The best way to install that on arch linux is via the package `miniconda3`, which installs a minimal conda
for local usage.

## Setup
Before using the python libraries the need to be installed by the package manager. This can be done the shell script
```
init/<shell_script>.sh
```
After that the main script can be found in the bin folder, whereas the subsequent scripts are stored in the lib directory.
When running the scripts or implementing new code the corresponding profile, that was created with the init scripts, should be activated:
```
conda activate wrf_env
```

## Usage
The project is splitted in two parts:
* The creation of composite plots that need the output data from a wrf model run for the defined timesteps, on default the model
  creates an output file `wrfout_dnn_yyyy_mm_dd_hh:mm:ss.nc` every three hours of model time. These files serves as input for the composite plots.
  By executing `python plot_composites.py` the script looks up every nc file in the `files` directory and uses them - as they are automatically sorted
  by their timestamp - to generate composites for:
    * composite with 2m temperature, wind speed and direction and ground pressure
    * composite with 3 hour rain sums and ground pressure
    * composite with total rain sum since model start and ground pressure
    * composite with convective available potential energy [CAPE] and ground pressure
* The creation of stationary plot for a given location that needs the result data for a location that can be specified before a model run starts.
  The model stores several text files for a set location, the relevant ground data is stored in `location.TS` and serves as input data for a 
  meteogram plot. By executing `python plot_meteograms.py <"yyyy-mm-dd hh:mm">` the script looks up every TS file in the `files` directory and uses 
  them to generate a meteogram for the given location with:
    * station pressure reduced to sea level in [hPa]
    * relative humidity in [%]
    * wind direction 10 m above ground in [degree]
    * wind speed 10 m above ground in [m/s]
    * precipitation as total sum since model start and 3 hour sum in [mm]
    * air temperature and dew point 2 m above ground in [degree Celsius]

## Troubleshooting
### Initialization
* running the command to set up the conda environment takes time due to the 
  [package enviroment](https://www.anaconda.com/blog/understanding-and-improving-condas-performance).
  Current test runs require roughly half an hour on a single core virtual machine. If the command takes more
  then two hours try to use the debug option `--verbose` twice to check for issues with the command

### Output generation
* creating meteograms for model output with less then 24 hours of forecast time leads to segmentation fault.
  With [#26](https://github.com/SettRaziel/wrf_visualization/issues/26) it needs to be checked where this error
  comes from and how to resolve it. Until that make sure the forecast time of your model is greater than 24 hours

## License
see LICENSE

## Contributing
* Fork it
* Create your feature branch (git checkout -b my-new-feature)
* Commit your changes (git commit -am 'add some feature')
* Push to the branch (git push origin my-new-feature)
* Create an issue describing your work
* Create a new pull request


## Todos and Issues
check [issues](https://github.com/SettRaziel/wrf_visualization/issues)

created by: Benjamin Held, December 2019
