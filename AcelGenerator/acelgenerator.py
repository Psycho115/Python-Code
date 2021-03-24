class AcelGenerator(object):

    def __init__(self, totalTime, timeStep):
        self.m_totalTime = totalTime
        self.m_timeStep = timeStep
        self.m_acelList = []

    def SetFuncAcel(self, funcAcelX, funcAcelY, funcAcelZ):
        self.m_funcAcelX = funcAcelX
        self.m_funcAcelY = funcAcelY
        self.m_funcAcelZ = funcAcelZ

    def GenerateAcel(self):
        currentTime = 0
        ID = 1
        while currentTime <= self.m_totalTime:
            self.m_acelList.append(AcelItem(ID, self.m_timeStep, self.m_funcAcelX, self.m_funcAcelY, self.m_funcAcelZ))
            currentTime += self.m_timeStep
            ID += 1

    def WriteFile(self, filename):
        txtfile = TXTFeed(filename)
        txtfile.WriteTXT(self.m_totalTime, self.m_timeStep, self.m_acelList)
        txtfile.Finished()

class TXTFeed(object):    
    
    def __init__(self, filename):        
        self.txtfile = open(filename, "wb")

    def Finished(self):        
        self.txtfile.close()

    def __del__(self):        
        if not self.txtfile.closed:
            self.txtfile.close()

    def WriteTXT(self, totalTime, timeStep, acelList):        
        self.txtfile.write("/ACEL_INFO/\r\n")
        self.txtfile.write("%.10f %.10f\r\n" % (totalTime, timeStep))
        self.txtfile.write("/ACEL_INFO_END/\r\n/ACEL/\r\n")
        for acelItem in acelList:
            acelItem.LogToTxt(self.txtfile)
        self.txtfile.write("/ACEL_END/\r\n")

class AcelItem(object):
    
    def __init__(self, ID, timeStep, funcX, funcY, funcZ):
        self.ID = ID
        self.time = (ID-1.0)*timeStep
        self.acelX = funcX(self.time)
        self.acelY = funcY(self.time)
        self.acelZ = funcZ(self.time)

    def LogToTxt(self, txtFile):

        txtFile.write("%d  %.10f  %.10f  %.10f  %.10f \r\n" % (self.ID, self.time, self.acelX, self.acelY, self.acelZ))
        

