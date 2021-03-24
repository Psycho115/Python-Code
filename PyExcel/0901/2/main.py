import sys
sys.dont_write_bytecode = True

from ProcessSingleFile import ProcessControl
from datetime import datetime

import os

if __name__=='__main__':

    ########################################

    curr_dir = os.path.dirname(os.path.realpath(__file__))

    for filePath in os.listdir(curr_dir):
        if os.path.splitext(filePath)[1] == '.xlsx':
            ProcessControl(curr_dir+"/"+filePath)

