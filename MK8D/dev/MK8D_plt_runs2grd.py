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


(PT_DT, PT_DV, PT_PL) = (
    './data/MK8D_runs.csv',
    './data/MK8D_trks.csv',
    './plots/Times.html'
)
centered = True
TRACKS = mk.TRACKS
###############################################################################
# Read data
###############################################################################
(runs, trks) = (pd.read_csv(PT_DT), pd.read_csv(PT_DV))
(dfT, dfH, dfR) = [pd.DataFrame() for i in range(3)]
# Filtered finished runs ------------------------------------------------------
rids = list(runs['ID'].unique())
dfT['ID'] = dfH['ID'] = dfR['ID'] = rids
###############################################################################
# Re-arrange DataFrames
###############################################################################
df = trks[trks['ID'].isin(set(rids))]
for trk in TRACKS:
    dfT[trk] = list(df[df['Track']==trk]['Time'])
###############################################################################
# Human-Readable
###############################################################################
for trk in TRACKS:
    dfH[trk] = dfT[trk].apply(lambda x: str(round(x, 1)).zfill(5))
###############################################################################
# Ranked
###############################################################################
for trk in TRACKS:
    dfR[trk] = dfH[trk].rank().apply(lambda x: int(x)) 
###############################################################################
# Colprs
###############################################################################
colorSwatch = mk.generateColorSwatch(
    '#233090', len(rids), alphaOffset=(.1, 1), lumaOffset=(.35, 1)
)
highlight = list(Color('#FF4294').get_rgb())
bc = 'rgb({},{},{})'.format(*[i*255 for i in highlight])
colors = np.array([
    'rgb({},{},{})'.format(i[0]*255, i[1]*255, i[2]*255) for i in colorSwatch
])
colors[0] = bc
###############################################################################
# Table
###############################################################################
fig = go.Figure(data=[go.Table(
    columnwidth=[100] + [100] * len(TRACKS),
    header=dict(
        values=rids,
        align='center', font=dict(color='black', size=8),
        line_color='black'
    ),
    cells=dict(
        values=np.array([dfH[trk] for trk in (list(TRACKS))]).T,
        align='center', font=dict(color='black', size=12),
        line_color='black', height=12*2
    ))
])
fig.show()
fig.write_html(PT_PL)