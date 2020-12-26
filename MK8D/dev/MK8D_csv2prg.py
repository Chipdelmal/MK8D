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
    hover_data=['Split'], line_shape='linear'
)
fig.show()
###############################################################################
# Export
###############################################################################
fig.write_html(PT_PL)