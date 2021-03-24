import sys
sys.dont_write_bytecode = True

import pandas as pd
from datetime import datetime, timedelta, time
import types
import xlsxwriter

from Reader import Read


def ProcessControl(filePath):

    xl = pd.ExcelFile(filePath)

    for sheet in xl.sheet_names:
        if sheet == "B_0":
            [D, TS, E] = Read(xl, sheet)
        if sheet == "8BB1_0":
            [D, TS, T] = Read(xl, sheet)
        if sheet == "8BB1_1":
            [D, TS, H] = Read(xl, sheet)
        if sheet == "8BB1_2":
            [D, TS, C] = Read(xl, sheet)
        if sheet == "8BB1_3":
            [D, TS, W] = Read(xl, sheet)
        if sheet == "8BD1_0":
            [D, TS, S] = Read(xl, sheet)

    idx = range(0, len(D))

    result = {"date": pd.Series(D, index=idx),
              "time": pd.Series(TS, index=idx),
              "temp": pd.Series(T, index=idx),
              "hum": pd.Series(H, index=idx),
              "conf": pd.Series(C, index=idx),
              "indoor": pd.Series(S, index=idx),
              "energy": pd.Series(E, index=idx),
              "wind": pd.Series(W, index=idx)}

    dResult = pd.DataFrame.from_dict(result)

    try:
        dResult.to_excel("output.xlsx", sheet_name="output", engine='xlsxwriter')
    except KeyError as e:
        print(e)
