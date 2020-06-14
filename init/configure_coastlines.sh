#!/bin/sh
# @Author: Benjamin Held
# @Date:   2020-06-13 11:29:03
# @Last Modified by:   Benjamin Held
# @Last Modified time: 2020-06-14 09:13:29

# define terminal colors
. ./terminal_color.sh

load_zipfile () {
	FILE_NAME=${1}
	wget "https://www.io-warnemuende.de/tl_files/staff/rfeistel/download/${FILE_NAME}.zip"
	unzip "${FILE_NAME}.zip"
	rm "${FILE_NAME}.zip"
}

# Downloading detailed coastlines
NGL_PATH="${HOME}/.conda/envs/pyn_env/lib/python3.7/site-packages/ngl/ncarg/rangs"
mkdir "${NGL_PATH}"
cd "${NGL_PATH}"

load_zipfile "rangs(0)"
load_zipfile "rangs(1)"
load_zipfile "rangs(2)"
load_zipfile "rangs(3)"
load_zipfile "rangs(4)"
load_zipfile "gshhs(0)"
load_zipfile "gshhs(1)"
load_zipfile "gshhs(2)"
load_zipfile "gshhs(3)"
load_zipfile "gshhs(4)"
