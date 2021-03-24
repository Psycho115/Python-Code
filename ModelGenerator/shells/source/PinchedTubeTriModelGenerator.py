from utility.UtilityBase import FPMFeed, NodeItem, ElementBaseItem, SupportItem, LoadItem, NodeSetItem
from utility.ModelGeneratorBase import LineElement, TriElement, TetraElement, ModelGeneratorBase
import math

class FunnelModelGenerator(ModelGeneratorBase):

    def __init__(self, length, r0, r1, module_number_l, module_number_c, force):
        ModelGeneratorBase.__init__(self)
        self._length = length
        self._r0 = r0
        self._r1 = r1
        self._module_number_l = module_number_l
        self._module_number_c = module_number_c
        self._force = force

    def _GenerateNode(self):
        cons_set = NodeSetItem("cons_set")
        load_set = NodeSetItem("load_set")
        count = 1
        dTheta = 360.0 / self._module_number_c
        for jdx in range(0, self._module_number_l+1):
            dr = (self._r1 - self._r0) / self._module_number_l
            dh = self._length / self._module_number_l
            for idx in range(0, self._module_number_c):
                no = count
                r = self._r0 + jdx * dr
                x = r * math.cos(math.radians(idx*dTheta))
                y = r * math.sin(math.radians(idx*dTheta))
                z = self._length - jdx * dh        
                self._nodes.append(NodeItem(no, x, y, z))
                if jdx == 0:
                    cons_set.AddNode(no)
                if jdx == self._module_number_l:
                    if idx == 0 or idx == self._module_number_c / 2:
                        load_set.AddNode(no)
                count += 1
        self._nodesets.append(cons_set)
        self._nodesets.append(load_set)

    def _GenerateElement(self):
        count = 1
        for jdx in range(0, self._module_number_l):
            for idx in range(0, self._module_number_c):
                if idx != self._module_number_c-1:
                    node_1 = jdx*(self._module_number_c) + idx + 1
                    node_2 = jdx*(self._module_number_c) + idx + 2
                    node_3 = (jdx+1)*(self._module_number_c) + idx + 1
                    self._elements.append(TriElement("SHELL", count, node_1, node_2, node_3, 0, 1, 1))
                    count += 1

                    node_1 = jdx*(self._module_number_c) + idx + 2
                    node_2 = (jdx+1)*(self._module_number_c) + idx + 1
                    node_3 = (jdx+1)*(self._module_number_c) + idx + 2
                    self._elements.append(TriElement("SHELL", count, node_1, node_2, node_3, 0, 1, 1))
                    count += 1
                else:
                    node_1 = jdx*(self._module_number_c) + idx + 1
                    node_2 = (jdx-1)*(self._module_number_c) + idx + 2
                    node_3 = (jdx+1)*(self._module_number_c) + idx + 1
                    self._elements.append(TriElement("SHELL", count, node_1, node_2, node_3, 0, 1, 1))
                    count += 1

                    node_1 = (jdx-1)*(self._module_number_c) + idx + 2
                    node_2 = (jdx+1)*(self._module_number_c) + idx + 1
                    node_3 = jdx*(self._module_number_c) + idx + 2
                    self._elements.append(TriElement("SHELL", count, node_1, node_2, node_3, 0, 1, 1))
                    count += 1                     

    def _GenerateSupport(self):
        self._constraints.append(SupportItem("CONS", "cons_set", True, True))

    def _GenerateLoad(self):
        nodes = self._nodesets[1]
        self._loads.append(LoadItem('pinched_force', nodes.GetNode(0), -force, 0.0, 0.0))
        self._loads.append(LoadItem('pinched_force', nodes.GetNode(1), force, 0.0, 0.0))
        # force_seg = self._force*self._height / self._module_number_l / 2
        # for jdx in range(0, self._module_number_l+1):
        #     for idx in range(0, self._module_number_c):
        #         if idx == 0:
        #             no = jdx * (self._module_number_c) + idx + 1
        #             if jdx == 0 or jdx == self._module_number_l:
        #                 self._loads.append(LoadItem('Load_1',no,force_seg,0.0,0.0))
        #             else:
        #                 self._loads.append(LoadItem('Load_1',no,force_seg*2,0.0,0.0))

    def _WriteBegin(self, txtfile):
        #material
        txtfile.Write("/MATERIAL/\r\n")
        txtfile.Write("1, mat1, LE, 1000, 2.065e7, 0.3\r\n")
        txtfile.Write("##\r\n")
        #section
        txtfile.Write("/SECTION/\r\n")
        txtfile.Write("1, shell, THICK, 0.03\r\n")
        txtfile.Write("##\r\n")

    def _WriteEnd(self, txtfile):
        #material
        txtfile.Write("/STEP_INIT/\r\n")
        txtfile.Write("CONSTRAINT, CONS\r\n")
        txtfile.Write("##\r\n")
        #section
        txtfile.Write("/STEP/\r\n")
        txtfile.Write("step_1_static, GENERAL, STATIC, 1e-4, 1, 100, 20\r\n")
        txtfile.Write("step_1_static, LOAD, pinched_force\r\n")
        txtfile.Write("##\r\n")

import os
import FrameModelGenerator

if __name__=='__main__':

    length = 3.048
    r0 = 1.016
    r1 = 1.016
    module_number_l = 150
    module_number_c = 300
    force = 800

    generator = FunnelModelGenerator(
        length,
        r0,
        r1,
        module_number_l,
        module_number_c,
        force)

    generator.GenerateModel()

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fileName = "C:\\Users\\Tang\\Desktop\\pinched_.fpmt"
    filePath = os.path.join(fileDir, fileName)
    generator.WriteFile(fileName)