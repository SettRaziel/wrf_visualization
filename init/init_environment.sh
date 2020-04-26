#!/bin/sh
# @Author: Benjamin Held
# @Date:   2020-04-26 11:29:03
# @Last Modified by:   Benjamin Held
# @Last Modified time: 2020-04-26 16:45:21

# installs the required linux packages
sh ./install_packages.sh

# installs and configs the required python packages and environments
sh ./install_geocat.sh
