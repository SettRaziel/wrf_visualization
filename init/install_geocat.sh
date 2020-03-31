# @Author: Benjamin Held
# @Date:   2020-03-30 14:54:50
# @Last Modified by:   Benjamin Held
# @Last Modified time: 2020-03-31 11:48:34

conda create -n geocat -c conda-forge -c ncar geocat-comp pyngl matplotlib cartopy jupyter
conda activate geocat

conda create -n pyn_env -c conda-forge pynio pyngl
source activate pyn_env

conda install -c conda-forge wrf-python
