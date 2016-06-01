#!/usr/bin/env bash

# exit on any error
set -Ee

if [ $(id -u) -eq 0 ]; then
  echo "This script should not be run as root or with sudo."
  exit 1
fi

TOP=$(cd $(dirname $0) && pwd -L)
VIRTUALENV_ROOT=${VIRTUALENV_ROOT:-"${HOME}/.virtualenvs/mycroft-media-skills"}

# create virtualenv, consistent with virtualenv-wrapper conventions
if [ ! -d ${VIRTUALENV_ROOT} ]; then
  mkdir -p $(dirname ${VIRTUALENV_ROOT})
  virtualenv ${VIRTUALENV_ROOT}
fi
source ${VIRTUALENV_ROOT}/bin/activate
cd ${TOP}

pip install mycroft_skills_sdk --extra-index-url=http://pypi.mycroft.team --trusted-host pypi.mycroft.team

pip install -r requirements.txt
