#!/bin/bash

# NOTIFY_URL="https://hc-ping.com/<uuid>"
# can/should be set via ENV
## see: https://healthchecks.io

[[ -z "$NOTIFY_URL" ]] && exit 0

LOGFILE="/vdirsyncer/lastsync.log"
STATUS=${1:-0}

curl -sS -m10 --retry 5 --data-binary @$LOGFILE $NOTIFY_URL/$STATUS