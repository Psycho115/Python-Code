import os
import TriModelGenerator
import TetraModelGenerator
import StructureSoilModelGenerator
import PoStructureSoilModelGenerator
import PlaneModelGenerator

import SlideSoilModelGenerator

if __name__=='__main__':

    size_x = 540.0
    size_y = 180.0
    size_z = 180.0
    module_x = 30
    module_y = 10
    module_z = 10

    pressure = -0.001
    bodyload = -0.001

    generator = SlideSoilModelGenerator.SlideSoilModelGenerator()
    generator._InitSoil(size_x,size_y,size_z,module_x,module_y,module_z)
    generator.GenerateModel()

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fileName = u"D:\FPM\Slide\slide.fpmt"
    filePath = os.path.join(fileDir, fileName)
    generator.WriteFile(fileName)