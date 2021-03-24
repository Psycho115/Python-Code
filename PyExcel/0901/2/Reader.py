import pandas as pd
from datetime import datetime, timedelta, time
import types

import sys
sys.dont_write_bytecode = True

def Read(xl, sheet):

    result = []
    dates = []
    timestamps = []

    df = xl.parse(
        sheet_name=sheet, 
        header=0)

    for jdx, row in df.iterrows():
        for idx in range(0,24):
            dates.append(jdx)
            result.append(row[idx])
            timestamps.append(idx)

    return [dates, timestamps, result]