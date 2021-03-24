import pandas as pd
from Param import ControlParam
from datetime import datetime, timedelta, time
import types
import math

import sys
sys.dont_write_bytecode = True

def ProcessW(xl, sheet, param, T, H):

    resultDic = {}

    currentDate = param.startDate
    while currentDate <= param.endDate:
        if not resultDic.has_key(currentDate.date()):
            resultDic.setdefault(currentDate.date(),set())
        currentDate = currentDate + timedelta(days=1)

    df = xl.parse(
        sheet_name=sheet, 
        header=0, 
        usecols=','.join([param.timeColName_W, param.statusColName_W]),
        names=["time", "status"],
        skiprows=[0])

    for idx in range(0,len(df)):

        timeRcd = df.at[idx,"time"]
        if type(timeRcd) is types.UnicodeType:
            timeRcd = datetime.strptime(timeRcd, param.timeFormat)
        dateStamp = timeRcd.date()
        timeStamp = timeRcd - datetime.combine(dateStamp,time(0,0,0,0))
        timeStamp = int(math.floor(timeStamp.total_seconds()/param.accuracyInMinutes/60))

        status = -1 if df.at[idx,"status"] == param.statusOpenName else 1

        if not resultDic.has_key(timeRcd.date()):
            resultDic.setdefault(timeRcd.date(),set())
        if isinstance(resultDic[timeRcd.date()], set):
            resultDic[timeRcd.date()].add((timeStamp,status))

    #########
    ## process data

    dataLength = param.GetDataLength()

    keys = resultDic.keys()
    keys.sort()

    for key in keys:
        newVec = [0 for x in range(0, dataLength)]
        if isinstance(resultDic[key], set):
            for item in resultDic[key]:
                newVec[item[0]] += item[1]
        resultDic[key] = newVec

    # for key in keys:   
    #     if type(resultDic[key]) is types.ListType:
    #         if resultDic[key][0] == 1:
    #             resultDic[key][0] = 0
    #         if resultDic[key][-1] == -1:
    #             resultDic[key][-1] = 0    
    #         for idx in range(0,dataLength):
    #             if resultDic[key][idx] != 0:
    #                 if resultDic[key][idx] == 1:
    #                     resultDic[key][0] = -1
    #                 break
    #         for idx in range(-1,-dataLength-1,-1):
    #             if resultDic[key][idx] != 0:
    #                 if resultDic[key][idx] == -1:
    #                     resultDic[key][-1] = 1
    #                 break

    currentState = 0

    for idx in range(0, dataLength * len(keys)):
        dataidx = keys[int(idx / dataLength)]
        timeidx = idx % dataLength
        
        if resultDic[dataidx][timeidx] == -1:
            currentState = 1
        if resultDic[dataidx][timeidx] == 1:
            currentState = 0

        resultDic[dataidx][timeidx] = currentState


    # for key in keys:
    #     newVec = [0 for x in range(0, dataLength)]
    #     if type(resultDic[key]) is types.ListType:        
    #         currentIdx = 0
    #         while currentIdx < dataLength:
    #             if resultDic[key][currentIdx] == -1:
    #                 while resultDic[key][currentIdx] != 1 and currentIdx < dataLength:
    #                     newVec[currentIdx] = 1
    #                     currentIdx += 1
    #                     continue
    #                 newVec[currentIdx] = 1
    #                 currentIdx += 1
    #                 continue
    #             else:
    #                 currentIdx += 1
    #                 continue
    #         resultDic[key] = newVec

    TResultDic = {}
    HResultDic = {}
    
    for key in keys:
        TResultDic[key] = [0 for x in range(0, dataLength)]
        HResultDic[key] = [0 for x in range(0, dataLength)]

    keys.sort()
    for key in keys:
        for idx in range(0, dataLength):
            t = T[key][idx] if T.has_key(key) else 1
            h = H[key][idx] if H.has_key(key) else 1
            if param.bReverse is True:
                isOpen = 0 if resultDic[key][idx]==1 else 1
            else:
                isOpen = 1 if resultDic[key][idx]==1 else 0
            TResultDic[key][idx] = isOpen * t
            HResultDic[key][idx] = isOpen * h

    # for key in TResultDic:
    #     print key, TResultDic[key]

    return [TResultDic, HResultDic]