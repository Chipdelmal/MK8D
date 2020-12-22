
  
import time 
from datetime import datetime
import MK8D as mk
import numpy as np
from os import path
import pandas as pd
from colour import Color
import plotly.express as px
import plotly.graph_objects as go


###############################################################################
# Generate and export one dataframe
###############################################################################
(PT_FL, FILENAME, OUT) = (
    './data/',
    'Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss',
    'MK8D.csv'
)
# FILEPATH = path.join(PT_FL, FILENAME)
# data = mk.getRunsDataframeFromFile(FILEPATH, metadata=True)
# data.to_csv(path.join(PT_FL, OUT), index=False)

###############################################################################
# Concatenate and export one dataframe from files list
###############################################################################
FILENAMES = (
    'Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss', 
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

data['ID'].unique()

###############################################################################
# Traces plot
###############################################################################
fig = px.line(
    mk.convertTimeFromSec(runsCTimes, timeTarget='Hours'),
    x="Track", y="Time", color='ID'
)
fig

###############################################################################
# Center CTimes around value
###############################################################################
cFun = np.mean
runsCTimesC = mk.centerRunsCTimes(runsCTimes, centerFunction=cFun)

###############################################################################
# Fastest/Slowest segments
###############################################################################
(fst, slw) = (
    {track: np.min(data[data['Track'] == track]['Time']) for track in tracksFltr},
    {track: np.max(data[data['Track'] == track]['Time']) for track in tracksFltr}
)

###############################################################################
# Traces Plot
###############################################################################
colorSwatch = mk.generateColorSwatch(
    '#233090', len(fshdRunsIDs), alphaOffset=.1, lumaOffset=.05
)
runsCTimesC = mk.convertTimeFromSec(runsCTimesC, timeTarget='Minutes')
runsCTimesC['Total'] = [time.strftime("%H:%M:%S", time.gmtime(i)) for i in runsCTimes['Time']]
fig = px.line(
    runsCTimesC, x="Track", y=cFun.__name__+' offset', color='ID',
    color_discrete_sequence=['rgba' + str(i) for i in colorSwatch],
    hover_data=['Total']
)
fig.update_traces(line=dict(width=0.5))
fig.update_xaxes(
    range=[-1, 60], tickvals=tracksFltr, tickfont_size=8
)
finalCoord = runsCTimesC[runsCTimesC['Track'] == tracksFltr[-1]][cFun.__name__ + ' offset']
finalTime = runsCTimesC[runsCTimesC['Track'] == tracksFltr[-1]]['Total']
fig.add_trace(go.Scatter(
    x=[1+len(tracksFltr)] * len(fshdRunsIDs),
    y=finalCoord,
    mode="text",
    name="Final Times",
    text=finalTime,
    textfont={'size': 8},
    textposition="middle right"
))

###############################################################################
# Violin Plot
###############################################################################
fig = go.Figure()
fig.add_trace(
    go.Violin(
        x=data['Track'][data['Version']=='Digital'],
        y=data['Time'][data['Version']=='Digital'],
        legendgroup='Digital', scalegroup='Digital', name='Digital',
        side='negative', points=False, line_color='blue'
    )
)
fig.add_trace(
    go.Violin(
        x=data['Track'][data['Version']=='Cartridge'],
        y=data['Time'][data['Version']=='Cartridge'],
        legendgroup='Cartridge', scalegroup='Cartridge', name='Cartridge',
        side='positive', points=False, line_color='red'
    )
)
fig.update_traces(meanline_visible=True)
fig.update_layout(violingap=0, violinmode='overlay')