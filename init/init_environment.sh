#!/bin/sh
# @Author: Benjamin Held
# @Date:   2020-04-26 11:29:03
# @Last Modified by:   Benjamin Held
# @Last Modified time: 2020-04-26 11:31:37

sh ./install_packages.sh

sudo conda init bash
sh ./install_geocat.sh
