import sys
sys.dont_write_bytecode = True

from Control import ProcessControl
from Param import ControlParam
from datetime import datetime

import os

if __name__=='__main__':

    param = ControlParam()

    ########################################
    ## change here

    param.startDate = datetime(2018,12,1)
    param.endDate = datetime(2018,12,31)
    param.bReverse = False

    ########################################

    curr_dir = os.path.dirname(os.path.realpath(__file__))

    for filePath in os.listdir(curr_dir):
        if os.path.splitext(filePath)[1] == '.xlsx' and filePath[0:3] != 'NEW':
            ProcessControl(filePath, param)

