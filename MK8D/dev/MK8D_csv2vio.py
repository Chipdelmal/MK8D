
import time 
from datetime import datetime
import pandas as pd
import plotly.express as px
import MK8D as mk


PT_PL = './data/MK8D_runs.csv'
tracksFltr = mk.TRACKS

runsCTimesC = pd.read_csv(PT_PL)