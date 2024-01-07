#!/bin/bash

DIR="/vdirsyncer/calendars/upsync"

[[ -z "$1" ]] && echo "Kein Dateiname angegeben!" && exit 1

FILNAM=$(basename -- $1)

rm $DIR/$FILNAM && echo "pre_deletion_hook: $DIR/$FILNAM gelöscht" && exit 0

## in der Datei pre_del.err finden wir die IDs aller Events, die Fehler produziert haben
echo "ERR pre_deletion $@" >>$DIR/pre_del.err

echo "pre_deletion_hook: FEHLER beim Löschen von $DIR/$FILNAM"
exit 1