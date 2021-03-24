import os
from UtilityBase import FPMFeed, NodeItem, ElementBaseItem, SupportItem, LoadItem
from ModelGeneratorBase import LineElement, TriElement, ModelGeneratorBase
import math

class PlaneSquareModelGenerator(ModelGeneratorBase):

    left_node = []
    right_node = []
    bottom_node = []

    def __init__(self, length, width, module_number_x, module_number_y, force):
        ModelGeneratorBase.__init__(self)
        self._width = width
        self._length = length
        self._module_number_x = module_number_x
        self._module_number_y = module_number_y
        self._force = force

    def _GenerateNode(self):
        count = 1
        dx = self._width / self._module_number_x
        dy = self._length / self._module_number_y
        for jdx in range(0, self._module_number_y+1):
            for idx in range(0, self._module_number_x+1):
                no = count
                x = idx * dx
                y = jdx * dy
                z = 0.0
                node = NodeItem(no, x, y, z)
                self._nodes.append(node)
                count += 1
                if idx == 0:
                    self.left_node.append(node)
                if idx == self._module_number_x:
                    self.right_node.append(node)
                if jdx == 0:
                    self.bottom_node.append(node)

    def _GenerateElement(self):
        count = 1
        for jdx in range(0, self._module_number_y):
            for idx in range(0, self._module_number_x):
                node_1 = jdx*(self._module_number_x+1) + idx + 1
                node_2 = jdx*(self._module_number_x+1) + idx + 2
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 1
                self._elements.append(TriElement("PLANE", count, node_1, node_2, node_3, 0, 1, 1))
                count += 1

                node_1 = jdx*(self._module_number_x+1) + idx + 2
                node_2 = (jdx+1)*(self._module_number_x+1) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 2
                self._elements.append(TriElement("PLANE", count, node_1, node_2, node_3, 0, 1, 1))
                count += 1

    def _GenerateAddtionalNode(self):
        pass

    def _GenerateAddtionalElement(self):
        comlength = 5
        nodeCount = len(self._nodes) + 1
        elemCount = len(self._elements) + 1
        for node in self.left_node:
            dnode = NodeItem(nodeCount, node._x - comlength, node._y, node._z)
            self._nodes.append(dnode)
            delem = LineElement("COMBIN", elemCount, node._id, dnode._id, 1, 0, 0)
            self._elements.append(delem)
            nodeCount += 1
            elemCount += 1
        for node in self.right_node:
            dnode = NodeItem(nodeCount, node._x + comlength, node._y, node._z)
            self._nodes.append(dnode)
            delem = LineElement("COMBIN", elemCount, node._id, dnode._id, 2, 0, 0)
            self._elements.append(delem)
            nodeCount += 1
            elemCount += 1
        for node in self.bottom_node:
            dnode = NodeItem(nodeCount, node._x, node._y - comlength, node._z)
            self._nodes.append(dnode)
            delem = LineElement("COMBIN", elemCount, node._id, dnode._id, 2, 0, 0)
            self._elements.append(delem)
            nodeCount += 1
            elemCount += 1

    def _GenerateSupport(self):
         for node in self.left_node:
            bc = SupportItem('BC_1', node._id, True, False)
            self._constraints.append(bc)
        for node in self.right_node:
            bc = SupportItem('BC_1', node._id, True, False)
            self._constraints.append(bc)
        for node in self.bottom_node:
            bc = SupportItem('BC_1', node._id, True, False)
            self._constraints.append(bc)

    def _GenerateLoad(self):
        # force = self._force / (self._module_number_y + 1)
        # for jdx in range(0, self._module_number_y+1):
        #     for idx in range(0, self._module_number_x+1):
        #         if idx==self._module_number_x:
        #             no = jdx * (self._module_number_x+1) + idx + 1
        #             self._loads.append(LoadItem('Load_1',no,force,0.0,0.0))
        pass

    def _WriteBegin(self, txtfile):
        rho = 2700
        possion = 0.25
        G = 1.32e10
        cs = 1400
        r = self._length
        k = 1.5 * G / r
        c = rho * cs

        l_kx, l_ky, l_cx, l_cy
        r_kx, r_ky, r_cx, r_cy

        b_kx = k, b_ky = 0, b_cx = c, b_cy = 0
        
        #material
        txtfile.Write("/MATERIAL/\r\n")
        # txtfile.Write("DP 6 1e+7 4.2 2000 0.2 0.0 30 30\r\n")
        txtfile.Write("1, soil, LE, %f, %f, %f, 0, 0 \r\n" % (rho, 2*G*(1+possion), possion))
        txtfile.Write("##\r\n")
        #section
        txtfile.Write("/SECTION/\r\n")
        txtfile.Write("1, THICK, 1\r\n")
        txtfile.Write("##\r\n")
        #real
        txtfile.Write("/REAL_CONSTANT/\r\n")
        txtfile.Write("1, left, SPRG, SPDP, %f, %f, 0, %f, %f, 0\r\n" % (l_kx, l_ky, l_cx, l_cy))
        txtfile.Write("2, right, SPRG, SPDP, %f, %f, 0, %f, %f, 0\r\n" % (r_kx, r_ky, r_cx, r_cy))
        txtfile.Write("3, bottom, SPRG, SPDP, %f, %f, 0, %f, %f, 0\r\n" % (b_kx, b_ky, b_cx, b_cy))
        txtfile.Write("##\r\n")


if __name__=='__main__':

    l = 600
    h = 300
    module_x = 100
    module_y = 50
    generator = PlaneSquareModelGenerator(l, h, module_x, module_y, 0)

    generator.GenerateModel()

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fileName = "D:\FPM\speed\half_1.fpmt"
    filePath = os.path.join(fileDir, fileName)
    generator.WriteFile(fileName)