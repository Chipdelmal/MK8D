
import MK8D as mk
from os import path
import pandas as pd

(PT_FL, FILENAME) = (
    '/home/chipdelmal/Documents/GitHub/mk8dLivesplit/dta/',
    'Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss'
)
FILEPATH = path.join(PT_FL, FILENAME)
data = mk.getRunsDataframeFromFile(FILEPATH, metadata=True)
data.tail()