#!/bin/sh
# @Author: Benjamin Held
# @Date:   2020-02-03 21:14:09
# @Last Modified by:   Benjamin Held
# @Last Modified time: 2020-10-15 20:26:31

# define terminal colors
. ./terminal_color.sh

# prepare folders
SCRIPT_PATH=$(pwd)
mkdir "${HOME}/aur_packages"
cd "${HOME}/aur_packages" || exit 1

# getting yay and install if necessary
git clone https://aur.archlinux.org/yay.git
cd yay || exit 1
git pull
makepkg -si --noconfirm --needed
cd .. || exit 1

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
  cat "${FILE_PATH}" | grep "miniconda"
fi

# package clean up
sudo pacman --noconfirm -Rsn "$(sudo pacman -Qdtq)"

# returning to script path
cd "${SCRIPT_PATH}" || exit 1
