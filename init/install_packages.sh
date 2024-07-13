#!/bin/sh

set -e

# define terminal colors
. ./terminal_color.sh

# prepare folders
SCRIPT_PATH=$(pwd)
# check if directory already exists and create if necessary
if ! [ -d "${HOME}/aur_packages" ]; then
  mkdir "${HOME}/aur_packages"
fi
cd "${HOME}/aur_packages"

# getting yay and install if necessary
git clone https://aur.archlinux.org/yay.git
cd yay
git pull
makepkg -si --noconfirm --needed
cd ..

# installing additional packeges
printf "%b\\nInstalling required packages: %b\\n" "${YELLOW}" "${NC}"
yay -S --noconfirm --needed wget unzip

# installing package manager
printf "%b\\nInstalling required python package manager: %b\\n" "${YELLOW}" "${NC}"
yay -S --noconfirm --needed miniconda3

CONDA_PATH="/opt/miniconda3/etc/profile.d/conda.sh"
FILE_PATH="${HOME}/.bashrc"
ENV_VARIABLE="[ -f ${CONDA_PATH} ] && source ${CONDA_PATH}"
RET=$(grep -Fx "${ENV_VARIABLE}" "${FILE_PATH}")

# check if conda variable already is set in .bashrc
if [[ ${RET} == "" ]]; then
  echo "${ENV_VARIABLE}" >> "${FILE_PATH}"
  # check .bashrc
  grep -F "miniconda" "${FILE_PATH}"
fi

# package clean up
sudo pacman --noconfirm -Rsn $(sudo pacman -Qdtq)

# returning to script path
cd "${SCRIPT_PATH}"
