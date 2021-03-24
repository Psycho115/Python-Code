import sys
sys.dont_write_bytecode = True

from datetime import datetime, timedelta, time

class ControlParam:

    startDate = datetime(2018,7,1)
    endDate = datetime(2018,7,31)

    accuracyInMinutes = 60

    timeFormat = "%Y-%m-%d %H:%M:%S"

    bReverse = False

    ### TH
    baselineDataValueForT = 0
    baselineDataValueForH = 0
    timeColName_TH = u"C"
    typeColName_TH = u"D"
    valueColName_TH = u"E"
    TTypeColName = u"temperature"
    HTypeColName = u"humidity"

    ### AC/WH
    powerLimitForAC = 200
    powerLimitForWH = 20
    timeColName_ACWH = u"F"
    powerColName_ACWH = u"G"

    ### W
    timeColName_W = u"F"
    statusColName_W = u"G"
    statusOpenName = u"open"
    statusCloseName = u"close"

    def GetDataLength(self):
        return int(24*60/self.accuracyInMinutes)

