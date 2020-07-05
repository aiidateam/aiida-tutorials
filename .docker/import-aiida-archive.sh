#!/bin/bash

# This script is executed whenever the docker container is (re)started.
# after the aiida profile has been setup

# Debugging.
set -x

if [ -f "/tmp/mount_folder/archive.aiida" ]; then
    verdi import --non-interactive --migration /tmp/mount_folder/archive.aiida
fi
