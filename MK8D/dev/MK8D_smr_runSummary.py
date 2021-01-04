#!/usr/bin/env python

import time 
from datetime import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import plotly.express as px
from colour import Color
import plotly.graph_objects as go
import MK8D as mk

(R_POS, V_OFF) = (-1, 10)
(PT_DT, PT_PL) = ('./data/MK8D_runs.csv', './plots/Summary.txt')
CATS = ('Nitro', 'Retro', 'Bonus', '32', '48')
###############################################################################
# Read data
###############################################################################
runs = pd.read_csv(PT_DT)
rids = list(runs['ID'].unique())
rid = rids[-1]
(df, dfH, dfT) = (runs[runs['ID']==rid], pd.DataFrame(), pd.DataFrame())
###############################################################################
# Tracks Timestamps
###############################################################################
df.loc[df['Track'] == 'Start', 'Time'] = V_OFF
(tracks, times) = (list(df['Track']), list(df['Time']))
trackTimeList = [
    '{}: {}'.format(tracks[i+1], str(timedelta(seconds=times[i])).split('.')[0])
    for i in range(len(tracks)-1)
]
###############################################################################
# Categories Times
###############################################################################
for cat in CATS:
    tracks = mk.CATEGORIES[cat]
    (start, end) = (tracks[0], tracks[-1])
    dfT[cat] = mk.runsCategoryTimes(df, start, end)
for cat in CATS:
    dfH[cat] = dfT[cat].apply(lambda x: (str(timedelta(seconds=x))[:mk.TPREC]))
###############################################################################
# Human-Readable
###############################################################################
(head, times) = [list(i) for i in (dfH.columns, dfH.values[0])]
catTimesList = ['{}: {}'.format(i[0], i[1]) for i in zip(head, times)]
###############################################################################
# Title
###############################################################################
title = '[] MK8D {} (200cc, 48 Tracks, No Items, Digital)'.format(times[-1])
###############################################################################
# Export
###############################################################################
f = open(PT_PL, "w")
f.write(title)
f.write('\n\n')
for tSet in (trackTimeList, catTimesList):
    for row in tSet:
        f.write(row)
        f.write('\n')
    f.write('\n')
f.close()