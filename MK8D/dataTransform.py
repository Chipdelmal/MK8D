
import pandas as pd
import MK8D.constants as cnst


def getFinishedRunsID(data, tracks):
    runsIds = []
    for i in cnst.TRACKS:
        filtr = (data['Track']== i)
        runsIds.append(set(data['ID'][filtr]))
    finishedRuns = set.intersection(*runsIds)
    return finishedRuns


def getFinishedRuns(data, tracks):
    fshdRuns = getFinishedRunsID(data, cnst.TRACKS)
    fltr = data['ID'].isin(fshdRuns)
    return data[fltr]