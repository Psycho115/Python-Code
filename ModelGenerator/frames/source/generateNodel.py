from modelInfo import NodeItem
from modelInfo import ElementItem
from modelInfo import ModelGenerator

import math

if __name__=='__main__':

    length = 5.0
    height = 3.0
    module_x = 5
    module_y = 3
    module_z = 20
    
    generator = ModelGenerator(length, height, module_x, module_y, module_z)

    generator.GenerateModel()
    generator.WriteFile("single.fpm")