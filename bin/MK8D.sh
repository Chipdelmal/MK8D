#!/bin/bash

CNTR="max"
FNAME="MK8D"
PT_IN="/home/chipdelmal/Documents/GitHub/MK8D/MK8D/dev/data"
PT_OT="/home/chipdelmal/Documents/GitHub/MK8D/MK8D/dev/data"
PT_PL="/home/chipdelmal/Documents/GitHub/MK8D/MK8D/dev/data"

MK8D_trk2csv $PT_IN $PT_OT "${FNAME}_trks.csv"
MK8D_run2csv "${PT_IN}/${FNAME}_trks.csv" $PT_OT "${FNAME}_runs.csv" $CNTR