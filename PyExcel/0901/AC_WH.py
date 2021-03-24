import pandas as pd
from Param import ControlParam
from datetime import datetime, timedelta, time
import types
import math
import copy

import sys
sys.dont_write_bytecode = True

def ProcessAC_WH(xl, sheet, param, T, H):

    resultDic = {}

    currentDate = param.startDate
    while currentDate <= param.endDate:
        if not resultDic.has_key(currentDate.date()):
            resultDic.setdefault(currentDate.date(),{})
        currentDate = currentDate + timedelta(days=1)

    powerLimit = 0
    if sheet[2] == "F":
        powerLimit = param.powerLimitForAC
    if sheet[2] == "E":
        powerLimit = param.powerLimitForWH

    df = xl.parse(
        sheet_name=sheet, 
        header=0, 
        usecols=','.join([param.timeColName_ACWH, param.powerColName_ACWH]),
        names=["time", "value"],
        skiprows=[0])

    for idx in range(0, len(df)):
        timeRcd = df.at[idx,"time"]
        power = df.at[idx,"value"]
        if type(timeRcd) is types.UnicodeType:
            timeRcd = datetime.strptime(timeRcd, param.timeFormat)
        dateStamp = timeRcd.date()
        timeStamp = timeRcd - datetime.combine(dateStamp,time(0,0,0,0))
        timeStamp = int(math.floor(timeStamp.total_seconds()/param.accuracyInMinutes/60))
        if not resultDic.has_key(dateStamp):
            resultDic.setdefault(dateStamp,{})
        if isinstance(resultDic[dateStamp], dict):
            if not resultDic[dateStamp].has_key(timeStamp):
                resultDic[dateStamp].setdefault(timeStamp,[])
            if isinstance(resultDic[dateStamp][timeStamp],list):
                resultDic[dateStamp][timeStamp].append(power)

    #########
    ## process data

    dataLength = param.GetDataLength()

    dateStamps = resultDic.keys()

    for dateStamp in dateStamps:
        newVec = [0 for x in range(0, dataLength)]
        if isinstance(resultDic[dateStamp],dict):
            for timeStamp in resultDic[dateStamp].keys():
                if isinstance(resultDic[dateStamp][timeStamp],list):
                    avgPower = sum(resultDic[dateStamp][timeStamp]) / len(resultDic[dateStamp][timeStamp])
                    if param.bReverse is True:
                        newVec[timeStamp] = 1 if avgPower<=powerLimit else 0
                    else:
                        newVec[timeStamp] = 1 if avgPower>=powerLimit else 0
        resultDic[dateStamp] = newVec

    TResultDic = {}
    HResultDic = {}
    
    for dateStamp in dateStamps:
        TResultDic[dateStamp] = [0 for x in range(0, dataLength)]
        HResultDic[dateStamp] = [0 for x in range(0, dataLength)]

    dateStamps.sort()
    for dateStamp in dateStamps:
        for idx in range(0, dataLength):
            t = T[dateStamp][idx] if T.has_key(dateStamp) else 1
            h = H[dateStamp][idx] if H.has_key(dateStamp) else 1
            v = resultDic[dateStamp][idx]
            TResultDic[dateStamp][idx] = v * t
            HResultDic[dateStamp][idx] = v * h

    # for key in TResultDic:
    #     print key, TResultDic[key]

    return [TResultDic, HResultDic]