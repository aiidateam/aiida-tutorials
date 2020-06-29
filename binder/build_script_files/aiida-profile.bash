#!/bin/bash
set -e

# set data directory and initialize
export PGDATA=$HOME/pgsql/data
mkdir -p "$PGDATA"
pg_ctl initdb

pg_ctl start -l pglog

# Create AiiDA profile.
reentry scan
export AIIDA_PATH=$HOME/.aiida
verdi quicksetup                           \
    --non-interactive                      \
    --profile "default"                    \
    --email "ringo@starr.com"              \
    --first-name "Ringo"                   \
    --last-name "Starr"                    \
    --institution "The Beatles"            \

verdi import --non-interactive /tmp/data.aiida

pg_ctl stop
