#!/bin/bash -l
# lightest possible entrypoint that ensures that
# we use a login shell to get a fully configured shell environment
# (e.g. sourcing /etc/profile.d, ~/.bashrc, and friends)

set -e

export PGDATA=$HOME/pgsql/data
export AIIDA_PATH=$HOME/.aiida

pg_ctl start -l pglog

exec "$@"
