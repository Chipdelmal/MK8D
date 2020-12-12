
from datetime import datetime
from datetime import timedelta


###############################################################################
# Timing
###############################################################################
REFT = datetime(1900, 1, 1, 0, 0, 0, 0)


def tdeltaToSec(tDelta, microSec=1000000):
    """Converts a timedelta object to a seconds equivalent

    Args:
        tDelta (timedelta): Timedelta object to convert to seconds
        microSec (int, optional): Microseconds fractional. Defaults to 1000000.

    Returns:
        float: Equivalent time in seconds.
    """
    tm = (tDelta.seconds) + (tDelta.microseconds / microSec)
    return tm


def tStrToSecs(tStr, refTime=REFT):
    """Converts a time string into a seconds float

    Args:
        tStr (string): Time string in the form H:M:S.ms
        refTime ([datetime], optional): Internal constant to convert times. Defaults to REFT.

    Returns:
        float: Equivalent time in seconds.
    """
    trackTiming = datetime.strptime(tStr[:-1], '%H:%M:%S.%f')
    tDiff = tdeltaToSec(trackTiming - REFT)
    return tDiff


def secToMin(sec, prec=-4):
    return timedelta(seconds=sec)


def minsToHr(mins, prec=-4):
    return timedelta(minutes=mins)


def scaleDevs(x, tDevs):
    return (x - min(tDevs)) / (max(tDevs) - min(tDevs))
