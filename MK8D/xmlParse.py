
import pandas as pd
from xmltodict import parse
from datetime import datetime
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


def getRIDFromFile(file, prependID='', zfill=5):
    doc = getDictFromXMLFile(file)
    history = doc['Run']['AttemptHistory']['Attempt']
    getAttemptsDates = [
        (i['@id'], datetime.strptime(i['@started'][:-3], '%m/%d/%Y %H:%M')) 
        for i in history
    ]
    strFmt = '%-y/%m/%d'
    ids = {
        i[0]: '{} ({}:{})'.format(
            i[1].strftime(strFmt),
            prependID, str(i[0]).zfill(zfill)
        ) 
        for i in getAttemptsDates
    }
    return ids


###############################################################################
# Dataframe
###############################################################################
def getTrackList(runs, tracks, rid, name, prependID='', zfill=5):
    # Constant data and track info
    (spd, itm, cat, ver) = (
        runs['speed'], runs['items'], runs['category'], runs['version']
    )
    track = tracks[name]
    # Run ID with timings
    (ids, times) = (list(track.keys()), list(track.values()))
    # If key, add date from dictionary, else just add the normal
    trackList = []
    for (key, time) in zip(ids, times):
        if str(key) in rid:
            entry = (rid[str(key)], name, time, ver, itm, spd, cat)
        else:
            entry = (
                '({}:{})'.format(prependID, str(key).zfill(zfill)),
                name, time, ver, itm, spd, cat
            )
        trackList.append(entry)
    return trackList


def getRunsDataframe(runs, tracks, rid, prependID='', zfill=5):
    tracksNames = list(tracks.keys())
    tracksList = []
    for i in tracksNames:
        tracksList.extend(
            getTrackList(runs, tracks, rid, i, prependID=prependID, zfill=zfill)
        )
    columns = ['ID', 'Track', 'Time', 'Version', 'Items', 'Speed', 'Category']
    runsDataframe = pd.DataFrame(tracksList, columns=columns)
    return runsDataframe


def getRunsDataframeFromFile(file, metadata=True, prependID='', zfill=5):
    runs = parseRunsFromFile(file, metadata=metadata)
    rid = getRIDFromFile(file, prependID=prependID, zfill=zfill)
    trks = getRunsDict(runs)
    data = getRunsDataframe(runs, trks, rid, prependID=prependID, zfill=zfill)
    return data


def compileRunsDataframeFromFiles(filesList, metadata=True, prependID=True, zfill=3):
    if prependID:
        dfs = [
            getRunsDataframeFromFile(
                file, 
                metadata=metadata, 
                prependID=str(i+1).zfill(2),
                zfill=3
            ) 
            for (i, file) in enumerate(filesList)
        ]
    else:
        dfs = [
            getRunsDataframeFromFile(
                file, metadata=metadata, prependID='', zfill=3
            ) 
            for (i, file) in enumerate(filesList)
        ]
    df = pd.concat(dfs)
    return df