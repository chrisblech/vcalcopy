#!/bin/bash

## Um das Event im Ziel-Kalender eine Stunde früher und eine Stunde länger zu speichern,
## nutzen wir den (optionalen) Parameter `--vor_minuten 60`.
## Da vdirsyncer für den `post_hook` keine Parameter akzeptiert, nutzen wir dieses Skript als Wrapper.

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

[[ ! -f "$1" ]] && echo "file not found: $1" && exit 1

$DIR/posthook.sh --vor_minuten 60 $1