
  
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
    'Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss', 
    # 'Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss'
)
OUT = 'MK8D_Full.csv'
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
# Plot
###############################################################################
colorSwatch = mk.generateColorSwatch(
    '#233090', len(fshdRunsIDs), alphaOffset=.35, lumaOffset=.2
)
runsCTimesC = mk.convertTimeFromSec(runsCTimesC, timeTarget='Minutes')
runsCTimesC['Total'] = [time.strftime("%H:%M:%S", time.gmtime(i)) for i in runsCTimes['Time']]
fig = px.line(
    runsCTimesC, x="Track", y=cFun.__name__+' offset', color='ID',
    color_discrete_sequence=['rgba' + str(i) for i in colorSwatch],
    hover_data=['Total']
)
fig.update_traces(line=dict(width=0.5))
fig.update_xaxes(range=[-2, 48+1])


###############################################################################
# Date
###############################################################################
FILEPATHS = [path.join(PT_FL, i) for i in FILENAMES]
doc = mk.getDictFromXMLFile(FILEPATHS[0])
history = doc['Run']['AttemptHistory']['Attempt']
getAttemptsDates = [
    (i['@id'], datetime.strptime(i['@started'][:-3], '%m/%d/%Y %H:%M')) 
    for i in history
]
strFmt = '%d/%m/%-y'
ids = {
    i[0]: '{} ({})'.format(i[1].strftime(strFmt), str(i[0]).zfill(4)) 
    for i in getAttemptsDates
}