from modelInfo import *

if __name__=='__main__':

    bar_length = 1 
    angle = 30 
    module_number = 12
    expanding_force = 500
    
    generator = ModelGenerator(bar_length, angle, module_number, expanding_force)

    generator.GenerateModel()
    generator.WriteFile("12-double.log")