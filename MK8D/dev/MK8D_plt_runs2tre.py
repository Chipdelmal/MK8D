#!/usr/bin/env python

import time 
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import plotly.express as px
from colour import Color
import plotly.graph_objects as go
import MK8D as mk


(PT_DT, PT_DV, PT_PL) = (
    './data/MK8D_runs.csv',
    './data/MK8D_trks.csv',
    './plots/Traces.html'
)
centered = True
TRACKS = mk.TRACKS
###############################################################################
# Read data
###############################################################################
(runs, trks) = (pd.read_csv(PT_DT), pd.read_csv(PT_DV))
###############################################################################
# Fastest/Slowest segments
###############################################################################
ops = (np.min, np.median, np.mean, np.max)
ts = [
    [op(trks[trks['Track'] == track]['Time']) for track in TRACKS] 
    for op in ops
]
stats = [np.sum(i) for i in ts]
statsStr = [
    '[{}{}]'.format(i[0].ljust(1), str(timedelta(seconds=i[1]))[:-4].ljust(1))
    for i in zip(('min ', 'μ ', 'M ', 'max '), stats)
]
###############################################################################
# Traces plot
###############################################################################
runIDs = list(runs['ID'].unique())
colorSwatch = mk.generateColorSwatch(
    '#233090', len(runIDs), alphaOffset=(.1, 1), lumaOffset=(.05, 1)
)
highlight = list(Color('#EE006E').get_rgb())
highlight.append(.9)
# Calculate fastest run -------------------------------------------------------
fshdRunsIDs = list(runs['ID'].unique())
endTimes = runs[runs['Track'] == TRACKS[-1]]
(fastest, slowest) = (min(endTimes['Time']), max(endTimes['Time']))
(fastestC, slowestC) = (min(endTimes['Center offset']), max(endTimes['Center offset']))
fid = endTimes[endTimes['Time'] == fastest]['ID'].values[0]
fPos = runIDs.index(fid)
colorSwatch[fPos] = tuple(highlight)
pbSplits = list(runs[runs['ID']==fid]['Split'])
# Main plot -------------------------------------------------------------------
if centered:
    fig = px.line(
        runs, 
        x="Track", y='Center offset', color='ID',
        color_discrete_sequence=['rgba' + str(i) for i in colorSwatch],
        hover_data=['Split'], line_shape='linear'
    )
    fig.update_traces(line=dict(width=2))
    fig.update_xaxes(
        range=[0, 5], tickvals=TRACKS, tickfont_size=20, tickangle = 90
    )
    finalCoord = runs[runs['Track'] == TRACKS[-1]]['Center offset']
    finalTime = runs[runs['Track'] == TRACKS[-1]]['Split']
    yTitle = 'Offset (seconds)'
    yRange = [fastestC-40, slowestC+10]
    for i in range(len(finalCoord)):
        if i == fPos:
            fig.add_trace(
                    go.Scatter(
                    x=[len(TRACKS)] * len(fshdRunsIDs),
                    y=[list(finalCoord)[i]],
                    mode="text", showlegend=False,
                    name="Final Times",
                    text=[list(finalTime)[i][:mk.TPREC]],
                    textfont={
                        'size': 15, 
                        'color': ['rgba' + str(i) for i in colorSwatch][i]
                    },
                    textposition="middle right"
                )
            )
else:
    fig = px.line(
        mk.convertTimeFromSec(runs, timeTarget='Hours'),
        x="Track", y="Time", color='ID',
        color_discrete_sequence=['rgba' + str(i) for i in colorSwatch],
        hover_data=['Split']
    )
    yTitle = 'Time (hours)'
    yRange = [0, fastest/(60*60)+.1]
# Update axes -----------------------------------------------------------------
vLines = [
    dict(
        type= 'line',
        yref= 'paper', y0= 0, y1= 1,
        xref= 'x', x0=i+.5, x1=i+.5,
        line=dict(color='#233090', width=.75, dash='dot')
    ) for i in range(0, len(TRACKS)+1, 4)
]
fig.update_layout(shapes=vLines)
fig.update_layout(violingap=0, violinmode='overlay')
fig.update_xaxes(
    range=[-1, len(TRACKS)+5], tickvals=TRACKS,
    tickfont_size=17, tickangle=90
)
fig.update_yaxes(
    range=yRange,
    tickfont_size=20, tickangle=0
)
fig.update_layout(
    title='Sum of Segments: '+' '.join(statsStr),
    font=dict(size=10),
    xaxis=dict(title_text='Track', titlefont=dict(size=30)),
    yaxis=dict(title_text=yTitle, titlefont=dict(size=30)),
    legend=dict(font=dict(size=12))
)
# Add annotation --------------------------------------------------------------
for (i, time) in enumerate(pbSplits[1:]):
    fig.add_annotation(
        x=i+1, y=.01, text=time[:mk.TPREC],
        font={'size': 8, 'color': '#ff006e', 'family': 'monospace'},
        showarrow=False, yref="paper", textangle=90
    )
fig.show()
fig.write_html(PT_PL)