#!/bin/bash

echo "Pre-Start: installing python iCalendar extension..."
pip install icalendar

## ensure vdirsyncer is capable of pre_deletion_hook
GH_SRC="https://github.com/pimutils/vdirsyncer/raw/ab3c379b10a2df6346754a4b27463317d4887d48/vdirsyncer/storage/filesystem.py"
VDS_LOC="/opt/pipx/venvs/vdirsyncer/lib/python3.11/site-packages/vdirsyncer/storage/filesystem.py"

echo "Pre-Start: ensure vdirsyncer is capable of pre_deletion_hook..."
grep -q pre_deletion_hook $VDS_LOC || wget -O $VDS_LOC $GH_SRC

[[ -f /vdirsyncer/cronfile ]] \
&& echo "Pre-Start: found own cronfile - copy to $CRON_FILE..." \
&& cat /vdirsyncer/cronfile >$CRON_FILE ## cp doesnt work: only root has write permission to destination dir

echo "Now changing to upstream start.sh ..."
exec /files/scripts/start.sh "$@"