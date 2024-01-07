#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

## $@ = [--vor_minuten xx] <filename>
CMD="python $DIR/posthook.py $@ $DIR/calendars/upsync"

$CMD && exit 0

## in der Datei posthook.err finden wir die IDs aller Events, die Fehler produziert haben
echo "ERR posthook.py $@" >>$DIR/posthook.err

exit 1