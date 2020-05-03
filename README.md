# WRF Forecast output visualization

Scripts and documentation to create visual output for a WRF model run.
Moving away from the ncar command language as announced [here](http://www.ncl.ucar.edu/Document/Pivot_to_Python/september_2019_update.shtml)
the main focus now stands on the usage of the corresponding python implementation for creating output from the WRF output results.

Current version: --

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

## Usage
Before using the python libraries the need to be installed by the package manager. This can be done the shell script
```
init/<shell_script>.sh
```
After that the main script can be found in the bin folder, whereas the subsequent scripts are stored in the lib directory.
When running the scripts or implementing new code the corresponding profile, that was created with the init scripts, should be activated:
```
conda activate wrf_env
```

## License
see LICENSE

created by: Benjamin Held, December 2019
