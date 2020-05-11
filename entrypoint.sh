#!/bin/sh
set -e

# while true
# do
/etc/periodic/15min/http_server.sh &
/etc/periodic/daily/ptsooy.sh &
crond -l2 -f
#   sleep 3600*3
# done
