
import pandas as pd
from xmltodict import parse
from collections import OrderedDict
import MK8D.auxiliary as aux


###############################################################################
# XML Dictionary 
###############################################################################
def getDictFromXMLFile(filePath):
    with open(filePath) as fd:
        doc = parse(fd.read())
    return doc


def getSegments(doc):
    return doc['Run']['Segments']['Segment']


def getSpeed(doc):
    sp = doc['Run']['Metadata']['SpeedrunComVariables']['Variable'][0]['#text']
    return sp


def getVersion(doc):
    vs = doc['Run']['Metadata']['SpeedrunComVariables']['Variable'][1]['#text']
    return vs


def getItems(doc):
    it = doc['Run']['Metadata']['SpeedrunComVariables']['Variable'][2]['#text']
    return it


def getCategory(doc):
    ct = doc['Run']['CategoryName']
    return ct


###############################################################################
# Runs dictionary
###############################################################################
def parseRunsFromFile(filePath, metadata=True):
    # Load file into dictionary and get segments
    doc = getDictFromXMLFile(filePath)
    segments = getSegments(doc)
    # Get metadata
    (speed, version, category, items) = [None] * 4
    if metadata:
        (speed, version, items, category) = (
            getSpeed(doc), getVersion(doc),
            getItems(doc), getCategory(doc)
        )
    # Assemble output dictionary
    runs = {
        'category': category,
        'version': version,
        'speed': speed,
        'items': items,
        'segments': segments
    }
    return runs


def getSegmentsNames(segments):
    return [i['Name'] for i in segments]


def getRunsDict(runs):
    (nms, tracks) = (getSegmentsNames(runs['segments']), OrderedDict())
    for (ix, track) in enumerate(runs['segments']):
        tHist = track['SegmentHistory']['Time']
        tEntry = {int(i['@id']): aux.tStrToSecs(i['RealTime']) for i in tHist}
        tracks.update({nms[ix]: tEntry})
    return tracks


###############################################################################
# Dataframe
###############################################################################
def getTrackList(runs, tracks, name, prependID='', zfill=5):
    # Constant data and track info
    (spd, itm, cat, ver) = (
        runs['speed'], runs['items'], runs['category'], runs['version']
    )
    track = tracks[name]
    # Run ID with timings
    (ids, times) = (list(track.keys()), list(track.values()))
    trackList = [
        (
            prependID+'_'+str(key).zfill(zfill), 
            name, time, ver, itm, spd, cat
        )
        for (key, time) in zip(ids, times)
    ] 
    return trackList


def getRunsDataframe(runs, tracks, prependID=''):
    tracksNames = list(tracks.keys())
    tracksList = []
    for i in tracksNames:
        tracksList.extend(getTrackList(runs, tracks, i, prependID=prependID))
    columns = ['ID', 'Track', 'Time', 'Version', 'Items', 'Speed', 'Category']
    runsDataframe = pd.DataFrame(tracksList, columns=columns)
    return runsDataframe


def getRunsDataframeFromFile(file, metadata=True, prependID=''):
    runs = parseRunsFromFile(file, metadata=metadata)
    trks = getRunsDict(runs)
    data = getRunsDataframe(runs, trks, prependID=prependID)
    return data


def compileRunsDataframeFromFiles(filesList, metadata=True, prependID=True):
    if prependID:
        dfs = [
            getRunsDataframeFromFile(file, metadata=metadata, prependID=str(i)) 
            for (i, file) in enumerate(filesList)
        ]
    else:
        dfs = [
            getRunsDataframeFromFile(file, metadata=metadata, prependID='') 
            for (i, file) in enumerate(filesList)
        ]
    df = pd.concat(dfs)
    return df