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

verdi import --non-interactive ${REPO_DIR}/docs/pages/2020_Intro_Week/notebooks/tutorial_perovskites_v0.1.aiida

pg_ctl stop
