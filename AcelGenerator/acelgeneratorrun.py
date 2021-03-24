from acelgenerator import AcelGenerator
import math

if __name__=='__main__':
    
    acelGenerator = AcelGenerator(10, 0.005)

    def AcelX(time):
        return 0.0

    def AcelY(time):
        return 0.0

    def AcelZ(time):
        #return 0.25*math.sin(2.0*math.pi*time/0.3)
        return 0.0

    acelGenerator.SetFuncAcel(AcelX, AcelY, AcelZ)
    acelGenerator.GenerateAcel()
    acelGenerator.WriteFile("MyAcel.txt")