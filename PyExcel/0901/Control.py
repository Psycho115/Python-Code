import sys
sys.dont_write_bytecode = True

import pandas as pd
from datetime import datetime, timedelta, time
import types

from Param import ControlParam

from TH import ProcessTH
from AC_WH import ProcessAC_WH
from W import ProcessW
from A import ProcessA
from CR import CrossRef

def ProcessControl(filePath, param):

    print "Loading excel file ", filePath

    xl = pd.ExcelFile(filePath)
    sheetNamesSortByB = {}
    sheetNamesProcessedResults = {}

    for sheet in xl.sheet_names:
        sheetNamesProcessedResults.setdefault(sheet, [])
        if sheet[2] == "B" and len(sheet) <= 4:
            sheetNamesSortByB.setdefault(sheet,[])

    for BSheet in sheetNamesSortByB:
        pos = BSheet[1]
        for sheet in xl.sheet_names:
            if sheet[1] == pos and BSheet != sheet:
                sheetNamesSortByB[BSheet].append(sheet)

    print "Successfully parsed excel file!"
    print " "

    #############################
    ## processing

    for BSheet in sheetNamesSortByB:

        print "Processing Position ", BSheet[1]
        print " "

        print "    Processing ", BSheet
        [T, H] = ProcessTH(xl, BSheet, param)
        sheetNamesProcessedResults[BSheet] = [T, H]
        print "    Finished processing ", BSheet
        print " "

        CTResult = {}
        CHResult = {}
        AResult = {}
        FTResult = {}
        FHResult = {}

        for sheet in sheetNamesSortByB[BSheet]:
            print "        Processing ", sheet
            if sheet[2] == "C":
                [CTResult, CHResult] = ProcessW(xl, sheet, param, T, H)
                sheetNamesProcessedResults[sheet] = [CTResult, CHResult]
            elif sheet[2] == "D":
                [AResult] = ProcessA(xl, sheet, param)
                sheetNamesProcessedResults[sheet] = [AResult]
            elif sheet[2] == "F":
                [FTResult, FHResult] = ProcessAC_WH(xl, sheet, param, T, H)
                sheetNamesProcessedResults[sheet] = [FTResult, FHResult]
            print "        Finished processing ", sheet
            print " "

        CRResult = {}
        if len(AResult) > 0 and len(FTResult) > 0 and len(CTResult) > 0:
            [CRResult] = CrossRef(xl, param, AResult, FTResult, CTResult)
            sheetNamesProcessedResults[BSheet[1]] = [CRResult]

        print "Finished Processing Position ", BSheet[1]
        print " "

    ### writer

    newFilePath = "NEW_" + filePath
    writer = pd.ExcelWriter(newFilePath)

    print "Writing to excel file ", newFilePath

    for (sheet, result_list) in sheetNamesProcessedResults.items():
        idx = 0
        for result_dict in result_list:
            if type(result_dict) is types.DictionaryType:
                sheetName = sheet + '_' + str(idx)
                dT = pd.DataFrame.from_dict(result_dict).transpose()
                dT.to_excel(writer, sheet_name=sheetName)
                idx += 1

    writer.save()

    print "File saved!"
