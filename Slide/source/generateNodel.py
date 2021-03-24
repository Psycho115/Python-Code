import os
import TriModelGenerator
import TetraModelGenerator
import StructureSoilModelGenerator
import PoStructureSoilModelGenerator
import PlaneModelGenerator

if __name__=='__main__':

    soil_size_x = 64.0
    soil_size_y = 64.0
    soil_size_z = 24.0
    soil_module_x = 16
    soil_module_y = 16
    soil_module_z = 6

    # struct_size_x = 16.0
    # struct_size_y = 16.0
    struct_size_z = 50
    # struct_module_x = 4
    # struct_module_y = 4
    struct_module_z = 10

    module_count_x = 4
    module_count_y = 2

    pressure = -0.001
    bodyload = -0.001

    generator = StructureSoilModelGenerator.StructSoilModelGenerator()

    generator._InitSoil(
        soil_size_x,
        soil_size_y,
        soil_size_z,
        soil_module_x,
        soil_module_y,
        soil_module_z,
        module_count_x,
        module_count_y)

    generator._InitStructure(
        struct_size_z,
        struct_module_z)

    generator._InitSoilLoad(pressure,bodyload)

    # size_x = 0.5
    # size_y = 0.1
    # size_z = 0.1
    # module_x = 40
    # module_y = 20
    # module_z = 4

    # R = 1
    # t = 0.5
    # pi = 1000000.0
    # po = -1000000.0

    # generator = PlaneModelGenerator.PlaneTubeModelGenerator(R, t, module_x, module_y, pi, po)

    generator.GenerateModel()

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fileName = "D:\FPM\Soil\overall_8.fpmt"
    filePath = os.path.join(fileDir, fileName)
    generator.WriteFile(fileName)