import pandas as pd
from Param import ControlParam
from datetime import datetime, timedelta, time
import types

import sys
sys.dont_write_bytecode = True

def ProcessA(xl, sheet, param):

    resultDic = {}

    currentDate = param.startDate
    while currentDate <= param.endDate:
        if not resultDic.has_key(currentDate.date()):
            resultDic.setdefault(currentDate.date(),[0 for x in range(0, 24)])
        currentDate = currentDate + timedelta(days=1)

    df = xl.parse(
        sheet_name=sheet, 
        header=0, 
        usecols="A,C:Z")

    for idx, row in df.iterrows():

        timeRcd = idx
        if type(timeRcd) is types.UnicodeType:
            timeRcd = datetime.strptime(timeRcd, param.timeFormat)
        dateStamp = timeRcd.date()

        if not resultDic.has_key(dateStamp):
            continue
        if isinstance(resultDic[dateStamp], list):
            resultDic[dateStamp] = row.tolist()

    # keys = resultDic.keys()
    # keys.sort()
    # for key in keys:
    #     print key, resultDic[key]

    return [resultDic]