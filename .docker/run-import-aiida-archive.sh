#!/bin/bash

# This script is executed whenever the docker container is (re)started.
# after the aiida profile has been setup

# Debugging.
set -em

su -c /opt/import-aiida-archive.sh ${SYSTEM_USER}
