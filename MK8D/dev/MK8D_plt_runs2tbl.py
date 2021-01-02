#!/usr/bin/env python

import time 
from datetime import datetime
from datetime import timedelta
import pandas as pd
import plotly.express as px
from colour import Color
import plotly.graph_objects as go
import MK8D as mk

# https://plotly.com/python/table/

(PT_DT, PT_PL) = ('./data/MK8D_runs.csv', './plots/Traces.html')
CATS = ('Nitro', 'Retro', 'Bonus', '32', '48')
###############################################################################
# Read data
###############################################################################
runs = pd.read_csv(PT_DT)
# Empty dataframe to hold times -----------------------------------------------
(dfT, dfH) = (pd.DataFrame(), pd.DataFrame())
(dfT['ID'], dfH['ID']) = (runs['ID'].unique(), runs['ID'].unique())
# Go through categories populating times list ---------------------------------
for cat in CATS:
    tracks = mk.CATEGORIES[cat]
    (start, end) = (tracks[0], tracks[-1])
    dfT[cat] = mk.runsCategoryTimes(runs, start, end) 
###############################################################################
# Human-Readable
###############################################################################
for cat in CATS:
    dfH[cat] = dfT[cat].apply(lambda x: (str(timedelta(seconds=x))[:-4]))
