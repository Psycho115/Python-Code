import pandas as pd
from Param import ControlParam
from datetime import datetime, timedelta, time
import types

import sys
sys.dont_write_bytecode = True

def CrossRef(xl, param, A, F, C):

    resultDic = {}

    currentDate = param.startDate
    while currentDate <= param.endDate:
        if not resultDic.has_key(currentDate.date()):
            resultDic.setdefault(currentDate.date(),[0 for x in range(0, 24)])
        currentDate = currentDate + timedelta(days=1)

    keys = resultDic.keys()
    keys.sort()

    dataLength = param.GetDataLength()

    for key in keys:
        for idx in range(0, dataLength):
            f = F[key][idx]
            c = C[key][idx]
            v = 0
            if c > 0 and f == 0:
                v = 1
            elif c == 0 and f > 0:
                v = 2
            elif c > 0 and f > 0:
                v = 3
            a = A[key][idx]
            if a == 0:
                a = 2
            elif a == 2:
                a = 0
            resultDic[key][idx] = v + 4 * a + 1

    # for key in keys:
    #     print key, resultDic[key]

    return [resultDic]