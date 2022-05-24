#!/bin/sh

set -e

# define terminal colors
. ./terminal_color.sh

load_zipfile () {
  FILE_NAME=${1}
  wget "https://www.io-warnemuende.de/tl_files/staff/rfeistel/download/${FILE_NAME}.zip"
  unzip "${FILE_NAME}.zip"
  rm "${FILE_NAME}.zip"
}

# safe current script path
SCRIPT_PATH=$(pwd)

# Issue 23: Since the environment is newly created there should be only one python folder
# therefor the command should directly expand to the one python version present
cd ${HOME}/.conda/envs/wrf_env/lib/python*/site-packages/ngl/ncarg/
mkdir "rangs"
cd "rangs"

# Downloading detailed coastlines
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

# return to script path
cd "${SCRIPT_PATH}"
