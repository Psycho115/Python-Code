import os
import FrameModelGenerator

if __name__=='__main__':

    size_x = 16.0
    size_y = 16.0
    size_z = 50
    module_x = 4
    module_y = 4
    module_z = 10

    generator = FrameModelGenerator.FrameModelGenerator(
        size_x,
        size_y,
        size_z,
        module_x,
        module_y,
        module_z)

    generator.GenerateModel()

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fileName = "D:\FPM\FSI\%d_frame.fpmt" % (module_z)
    filePath = os.path.join(fileDir, fileName)
    generator.WriteFile(fileName)