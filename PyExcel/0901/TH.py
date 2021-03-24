import pandas as pd
from Param import ControlParam
from datetime import datetime, timedelta, time
import types
import math

import sys
sys.dont_write_bytecode = True

def ProcessTH(xl, sheet, param):

    TResultDic = {}
    HResultDic = {}

    currentDate = param.startDate
    while currentDate <= param.endDate:
        if not TResultDic.has_key(currentDate.date()):
            TResultDic.setdefault(currentDate.date(),{})
        if not HResultDic.has_key(currentDate.date()):
            HResultDic.setdefault(currentDate.date(),{})
        currentDate = currentDate + timedelta(days=1)

    df = xl.parse(
        sheet_name=sheet, 
        header=0, 
        usecols=','.join([param.timeColName_TH, param.typeColName_TH, param.valueColName_TH]),
        names=["time", "type", "value"],
        skiprows=[0])

    for idx in range(0, len(df)):

        timeRcd = df.at[idx,"time"]
        if type(timeRcd) is types.UnicodeType:
            timeRcd = datetime.strptime(timeRcd, param.timeFormat)
        dateStamp = timeRcd.date()
        timeStamp = timeRcd - datetime.combine(dateStamp,time(0,0,0,0))
        timeStamp = int(math.floor(timeStamp.total_seconds()/param.accuracyInMinutes/60))

        vType = df.at[idx,"type"]
        value = df.at[idx,"value"]

        if vType == param.TTypeColName:
            if not TResultDic.has_key(dateStamp):
                TResultDic.setdefault(dateStamp,{})
            if isinstance(TResultDic[dateStamp], dict):
                if not TResultDic[dateStamp].has_key(timeStamp):
                    TResultDic[dateStamp].setdefault(timeStamp,[])
                if isinstance(TResultDic[dateStamp][timeStamp],list):
                    TResultDic[dateStamp][timeStamp].append(value)
        if vType == param.HTypeColName:
            if not HResultDic.has_key(dateStamp):
                HResultDic.setdefault(dateStamp,{})
            if isinstance(HResultDic[dateStamp], dict):
                if not HResultDic[dateStamp].has_key(timeStamp):
                    HResultDic[dateStamp].setdefault(timeStamp,[])
                if isinstance(HResultDic[dateStamp][timeStamp],list):
                    HResultDic[dateStamp][timeStamp].append(value)

    #########
    ## process data

    dateStamps = TResultDic.keys()
    for dateStamp in dateStamps:
        newVec = [param.baselineDataValueForT for x in range(0, param.GetDataLength())]
        if isinstance(TResultDic[dateStamp],dict):
            for timeStamp in TResultDic[dateStamp].keys():
                if isinstance(TResultDic[dateStamp][timeStamp],list):
                    avgT = sum(TResultDic[dateStamp][timeStamp]) / len(TResultDic[dateStamp][timeStamp])
                    newVec[timeStamp] = avgT
        TResultDic[dateStamp] = newVec

    dateStamps = HResultDic.keys()
    for dateStamp in dateStamps:
        newVec = [param.baselineDataValueForH for x in range(0, param.GetDataLength())]
        if isinstance(HResultDic[dateStamp],dict):
            for timeStamp in HResultDic[dateStamp].keys():
                if isinstance(HResultDic[dateStamp][timeStamp],list):
                    avgH = sum(HResultDic[dateStamp][timeStamp]) / len(HResultDic[dateStamp][timeStamp])
                    newVec[timeStamp] = avgH
        HResultDic[dateStamp] = newVec

    # for key in TResultDic:
    #     print key, TResultDic[key]

    return [TResultDic, HResultDic]