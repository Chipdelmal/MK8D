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

# https://plotly.com/python/table/

(PT_DT, PT_PL) = ('./data/MK8D_runs.csv', './plots/Table.html')
CATS = ('Nitro', 'Retro', 'Bonus', '32', '48')
BCOL = 'rgb(255, 255, 255)'
###############################################################################
# Read data
###############################################################################
runs = pd.read_csv(PT_DT)
# Empty dataframe to hold times -----------------------------------------------
(dfT, dfH, dfR) = [pd.DataFrame() for i in range(3)]
dfT['ID'] = dfH['ID'] = dfR['ID'] = runs['ID'].unique()
# Go through categories populating times list ---------------------------------
for cat in CATS:
    tracks = mk.CATEGORIES[cat]
    (start, end) = (tracks[0], tracks[-1])
    dfT[cat] = mk.runsCategoryTimes(runs, start, end) 
###############################################################################
# Human-Readable
###############################################################################
for cat in CATS:
    dfH[cat] = dfT[cat].apply(lambda x: (str(timedelta(seconds=x))[:mk.TPREC]))
###############################################################################
# Table
###############################################################################
colorSwatch = mk.generateColorSwatch(
    '#233090', len(dfT['ID']), alphaOffset=(.1, 1), lumaOffset=(.35, 1)
)
highlight = list(Color('#EE006E').get_rgb()) + [.9]
colors = np.array([
    'rgb({},{},{})'.format(i[0]*255, i[1]*255, i[2]*255) for i in colorSwatch
])
# Rank Order ------------------------------------------------------------------
for cat in CATS:
    dfR[cat] = dfH[cat].rank().apply(lambda x: int(x)) 
# Plot table ------------------------------------------------------------------
fills = [
    colors[dfR[cat]-1] if (cat is not 'ID') else np.array([BCOL]*len(dfT['ID'])) 
    for cat in (['ID'] + list(CATS))
]
fig = go.Figure(data=[go.Table(
    columnwidth=[100] + [200] * len(CATS),
    header=dict(
        values=list(dfH.columns),
        align='center', font=dict(color='black', size=16),
        line_color='black'
    ),
    cells=dict(
        values=[dfH[cat] for cat in (['ID'] + list(CATS))],
        align='center', font=dict(color='black', size=12),
        line_color='black', fill_color=fills
    ))
])
fig.show()
fig.write_html(PT_PL)
