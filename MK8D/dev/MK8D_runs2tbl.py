#!/usr/bin/env python

import time 
from datetime import datetime
import pandas as pd
import plotly.express as px
from colour import Color
import plotly.graph_objects as go
import MK8D as mk

# https://plotly.com/python/table/

(PT_DT, PT_PL) = ('./data/MK8D_runs.csv', './plots/Traces.html')
centered = True
TRACKS = mk.TRACKS
###############################################################################
# Read data
###############################################################################
runs = pd.read_csv(PT_DT)


tracks = mk.CATEGORIES['Bonus']
(start, stop) = (tracks[0], tracks[-1])

runs[runs['Track'] == start]



ids = list(runs['ID'].unique())
times = {
    cat: list(runs[runs['Track'] == mk.CATEGORIES[cat][-1]]['Split'])
    for cat in mk.CATEGORIES.keys()
}
keys = list(times.keys())
keys.append('ID')
cells = [[t[:-4] for t in times[cat]] for cat in list(times.keys())]
cells.append(ids)
fig = go.Figure(
    data=[go.Table(
        header=dict(
            values=keys, 
            fill_color='snow', align='center'
        ),
        cells=dict(
            values=cells,
            fill_color='lavender', align='center'
        )
    )]
)
fig.show()