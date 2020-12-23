
  
import time 
from datetime import datetime
from datetime import timedelta
import MK8D as mk
import numpy as np
from os import path
import pandas as pd
from colour import Color
import plotly.express as px
import plotly.graph_objects as go


###############################################################################
# Concatenate and export one dataframe from files list
###############################################################################
(PT_FL, PT_PL) = ('./data/', './plots')
FILENAMES = (
    # 'Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss', 
    'Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss', 
)
OUT = 'MK8D.csv'
FILEPATHS = [path.join(PT_FL, i) for i in FILENAMES]
data = mk.compileRunsDataframeFromFiles(FILEPATHS, prependID=True)
data.to_csv(path.join(PT_FL, OUT), index=False)

###############################################################################
# Filter for finished runs
###############################################################################
tracksFltr = mk.TRACKS
fshdRunsIDs = sorted(list(mk.getFinishedRunsID(data, tracksFltr)))
fshdRuns = mk.getFinishedRuns(data, tracksFltr)
runsCTimes = mk.convertFinishedRunsToCTimes(fshdRuns, fshdRunsIDs, tracksFltr)

###############################################################################
# Traces plot
###############################################################################
colorSwatch = mk.generateColorSwatch(
    '#233090', len(fshdRunsIDs), alphaOffset=(.1, 1), lumaOffset=(.05, 1)
)
fig = px.line(
    mk.convertTimeFromSec(runsCTimes, timeTarget='Hours'),
    x="Track", y="Time", color='ID',
    color_discrete_sequence=['rgba' + str(i) for i in colorSwatch],
)
fig.write_html(path.join(PT_PL, 'Traces.html'))

###############################################################################
# Center CTimes around value
###############################################################################
cFun = np.mean
runsCTimesC = mk.centerRunsCTimes(runsCTimes, centerFunction=cFun)

###############################################################################
# Fastest/Slowest segments
###############################################################################
(fst, men, slw) = (
    {track: np.min(data[data['Track'] == track]['Time']) for track in tracksFltr},
    {track: np.mean(data[data['Track'] == track]['Time']) for track in tracksFltr},
    {track: np.max(data[data['Track'] == track]['Time']) for track in tracksFltr}
)

###############################################################################
# Traces Plot
###############################################################################
colorSwatch = mk.generateColorSwatch(
    '#233090', len(fshdRunsIDs), alphaOffset=(.1, .8), lumaOffset=(.05, 1)
)
runsCTimesC = mk.convertTimeFromSec(runsCTimesC, timeTarget='Minutes')
runsCTimesC['Total'] = [time.strftime("%H:%M:%S", time.gmtime(i)) for i in runsCTimes['Time']]
fig = px.line(
    runsCTimesC, x="Track", y=cFun.__name__+' offset', color='ID',
    color_discrete_sequence=['rgba' + str(i) for i in colorSwatch],
    hover_data=['Total']
)
fig.update_traces(line=dict(width=2))
fig.update_xaxes(
    range=[-1, 50], tickvals=tracksFltr, tickfont_size=20, tickangle = 90
)
fig.update_yaxes(tickfont_size=20, tickangle = 0)
finalCoord = runsCTimesC[runsCTimesC['Track'] == tracksFltr[-1]][cFun.__name__ + ' offset']
finalTime = runsCTimesC[runsCTimesC['Track'] == tracksFltr[-1]]['Total']
fig.add_trace(
        go.Scatter(
        x=[len(tracksFltr)+1] * len(fshdRunsIDs),
        y=finalCoord,
        mode="text", showlegend=False,
        name="Final Times",
        text=finalTime,
        textfont={'size': 12},
        textposition="middle right"
    )
)
fig.write_html(path.join(PT_PL, 'TracesCentered.html'))

###############################################################################
# Violin Plot (Full)
###############################################################################
fig = go.Figure()
fig.add_trace(
    go.Violin(
        x=data['Track'],
        y=data['Time'],
    points=False, line_color='blue', spanmode='hard',
        line={'width': .75}
    )
)
fig.update_traces(meanline_visible=True)
fig.update_layout(violingap=0, violinmode='overlay')
fig.write_html(path.join(PT_PL, 'ViolinsSingle.html'))

###############################################################################
# Violin Plot (Digital/Cartridge)
###############################################################################
fig = go.Figure()
fig.add_trace(
    go.Violin(
        x=data['Track'][data['Version']=='Digital'],
        y=data['Time'][data['Version']=='Digital'],
        legendgroup='Digital', scalegroup='Digital', name='Digital',
        side='negative', points=False, line_color='blue', spanmode='hard',
        line={'width': .75}
    )
)
fig.add_trace(
    go.Violin(
        x=data['Track'][data['Version']=='Cartridge'],
        y=data['Time'][data['Version']=='Cartridge'],
        legendgroup='Cartridge', scalegroup='Cartridge', name='Cartridge',
        side='positive', points=False, line_color='red', spanmode='hard',
        line={'width': .75}
    )
)
fig.update_traces(meanline_visible=True)
fig.update_layout(violingap=0, violinmode='overlay')
fig.write_html(path.join(PT_PL, 'ViolinsDual.html'))