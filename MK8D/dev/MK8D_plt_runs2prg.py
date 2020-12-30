#!/usr/bin/env python

import time 
from datetime import datetime
import pandas as pd
import plotly.express as px
import MK8D as mk


(PT_DT, PT_PL) = ('./data/MK8D_runs.csv', './plots/Progress.html')
TRACKS = mk.TRACKS
###############################################################################
# Read data
###############################################################################
run = pd.read_csv(PT_DT)
###############################################################################
# Get final times with dates
###############################################################################
run = mk.convertTimeFromSec(run, timeTarget='Minutes')
finalEntries = run[run['Track'] == TRACKS[-1]].copy()
finalIDs = list(finalEntries['ID'])
dates = [datetime.strptime(i.split(' ')[0], '%y/%m/%d') for i in finalIDs]
finalEntries['Date'] = dates
###############################################################################
# Plot
###############################################################################
fig = px.line(
    finalEntries, 
    x='Date', y='Time', 
    hover_data=['Split'], line_shape='linear',
    color_discrete_sequence=['#FF006E']
)
fig.data[0].update(mode='markers+lines')
fig.update_layout(
    # title='Runs Progress',
    font=dict(size=20),
    xaxis=dict(title_text='Date', titlefont=dict(size=30)),
    yaxis=dict(title_text='Time (minutes)', titlefont=dict(size=30))
)
# Add annotation --------------------------------------------------------------
# for (i, time) in enumerate(list(finalEntries['Split'])):
#     fig.add_annotation(
#         x=dates[i], y=.01,
#         text=time[:-4],
#         font={'size': 10, 'color': '#233090', 'family': 'monospace'},
#         showarrow=False,
#         yref="paper",
#         textangle=90
#     )
fig.show()
###############################################################################
# Export
###############################################################################
fig.write_html(PT_PL)