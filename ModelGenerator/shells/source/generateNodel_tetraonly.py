import os
import TetraModelGenerator

if __name__=='__main__':

    size_x = 50.0
    size_y = 50.0
    size_z = 50.0
    module_x = 60
    module_y = 60
    module_z = 60

    pressure = -0.001
    bodyload = -0.001

    generator = TetraModelGenerator.CubeModelGenerator(size_x,size_y,size_z,module_x,module_y,module_z,pressure,bodyload)
    generator.GenerateModel()

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fileName = u"D:\FPM\Test\Tetra\cube60.fpmt"
    filePath = os.path.join(fileDir, fileName)
    generator.WriteFile(fileName)