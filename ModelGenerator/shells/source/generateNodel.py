import os
import StructureSoilModelGenerator
import StructureSoilFoundationModelGenerator

if __name__=='__main__':

    # soil_size_x = 80.0
    # soil_size_y = 24.0
    # soil_size_z = 32.0
    # soil_module_x = 40
    # soil_module_y = 6
    # soil_module_z = 16

    # struct_size_z = 50
    # struct_module_z = 10

    # module_count_x = 1
    # module_count_y = 1

    # space = 24

    # generator = StructureSoilFoundationModelGenerator.StructureSoilFoundationModelGenerator()

    soil_size_x = 64.0
    soil_size_y = 64.0
    soil_size_z = 24.0
    soil_module_x = 16
    soil_module_y = 16
    soil_module_z = 6

    struct_size_z = 50
    struct_module_z = 10

    module_count_x = 1
    module_count_y = 1

    space = 20

    generator = StructureSoilModelGenerator.StructSoilModelGenerator()

    generator._InitSoil(
        soil_size_x,
        soil_size_y,
        soil_size_z,
        soil_module_x,
        soil_module_y,
        soil_module_z,
        module_count_x,
        module_count_y,
        space)

    generator._InitStructure(
        struct_size_z,
        struct_module_z)

    # generator._InitSoilLoad(pressure,bodyload)

    generator.GenerateModel()

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fileName = "D:\FPM\FSI\overall_space_%d.fpmt" % (space)
    # fileName = "D:\FPM\FSI\SFS\%d_%d_foundation.fpmt" % (module_count_x, module_count_y)
    filePath = os.path.join(fileDir, fileName)
    generator.WriteFile(fileName)

    # real = 1
    # generator._SetWriteReal(real)
    # fileName = "D:\FPM\FSI\overall_space_%d_%d.fpmt" % (space, real)
    # # fileName = "D:\FPM\FSI\SFS\%d_%d_foundation.fpmt" % (module_count_x, module_count_y)
    # filePath = os.path.join(fileDir, fileName)
    # generator.WriteFile(fileName)

    # real = 2
    # generator._SetWriteReal(real)
    # fileName = "D:\FPM\FSI\overall_space_%d_%d.fpmt" % (space, real)
    # # fileName = "D:\FPM\FSI\SFS\%d_%d_foundation.fpmt" % (module_count_x, module_count_y)
    # filePath = os.path.join(fileDir, fileName)
    # generator.WriteFile(fileName)

    # real = 3
    # generator._SetWriteReal(real)
    # fileName = "D:\FPM\FSI\overall_space_%d_%d.fpmt" % (space, real)
    # # fileName = "D:\FPM\FSI\SFS\%d_%d_foundation.fpmt" % (module_count_x, module_count_y)
    # filePath = os.path.join(fileDir, fileName)
    # generator.WriteFile(fileName)