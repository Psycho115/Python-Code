from UtilityBase import FPMFeed, NodeItem, ElementBaseItem, SupportItem, LoadItem
from ModelGeneratorBase import LineElement, TriElement, TetraElement, ModelGeneratorBase
import math

class CubeModelGenerator(ModelGeneratorBase):

    _node_groups = {}
    hole_elems = []

    def __init__(self, xsize, ysize, zsize, module_x, module_y, module_z, force, pressure):
        ModelGeneratorBase.__init__(self)
        self._size_x = xsize
        self._size_y = ysize
        self._size_z = zsize
        self._module_x = module_x
        self._module_y = module_y
        self._module_z = module_z
        self._force = force
        self._pressure = pressure

    def _GenerateNode(self):
        count = 1
        side = []
        bottom = []
        dx = self._size_x/self._module_x
        dy = self._size_y/self._module_y
        dz = self._size_z/self._module_z
        for kdx in range(0, self._module_z+1):
            for jdx in range(0, self._module_y+1):
                for idx in range(0, self._module_x+1):
                    no = count
                    x = idx * dx - 0.5 * self._size_x
                    y = jdx * dy - 0.5 * self._size_y
                    z = kdx * dz - 0.5 * self._size_z
                    node = NodeItem(no, x, y, z)
                    if (idx == self._module_x or idx == 0 or jdx == self._module_y or jdx == 0) and kdx != self._module_z:
                        side.append(node)
                    if kdx == 0:
                        bottom.append(node)
                    self._nodes.append(node)
                    count += 1
        self._nodegroup['side'] = side
        self._nodegroup['bottom'] = bottom

    def _GenerateElement(self):
        count = 1
        for kdx in range(0, self._module_z):
            for jdx in range(0, self._module_y):
                for idx in range(0, self._module_x):
                    elems = []
                    node_1 = kdx*(self._module_x+1)*(self._module_y+1) + jdx*(self._module_x+1) + (idx+1)
                    node_2 = kdx*(self._module_x+1)*(self._module_y+1) + jdx*(self._module_x+1) + (idx+2)
                    node_3 = kdx*(self._module_x+1)*(self._module_y+1) + (jdx+1)*(self._module_x+1) + (idx+1)
                    node_4 = kdx*(self._module_x+1)*(self._module_y+1) + (jdx+1)*(self._module_x+1) + (idx+2)
                    node_5 = (kdx+1)*(self._module_x+1)*(self._module_y+1) + jdx*(self._module_x+1) + (idx+1)
                    node_6 = (kdx+1)*(self._module_x+1)*(self._module_y+1) + jdx*(self._module_x+1) + (idx+2)
                    node_7 = (kdx+1)*(self._module_x+1)*(self._module_y+1) + (jdx+1)*(self._module_x+1) + (idx+1)
                    node_8 = (kdx+1)*(self._module_x+1)*(self._module_y+1) + (jdx+1)*(self._module_x+1) + (idx+2)
                    if (idx%2+jdx%2+kdx%2)%2==1:
                        elems.append(TetraElement("SOLIDTETRA", count, node_1, node_2, node_3, node_5, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLIDTETRA", count, node_2, node_4, node_3, node_8, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLIDTETRA", count, node_2, node_8, node_3, node_5, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLIDTETRA", count, node_2, node_5, node_6, node_8, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLIDTETRA", count, node_3, node_8, node_7, node_5, 0, 0, 1))
                        count += 1
                    else:
                        elems.append(TetraElement("SOLIDTETRA", count, node_1, node_4, node_3, node_7, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLIDTETRA", count, node_4, node_8, node_7, node_6, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLIDTETRA", count, node_1, node_2, node_4, node_6, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLIDTETRA", count, node_1, node_5, node_6, node_7, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLIDTETRA", count, node_1, node_4, node_7, node_6, 0, 0, 1))
                        count += 1
                    # if (idx%2+jdx%2+kdx%2)%2==1:
                    #     elems.append(TetraElement("SOLIDTETRA", count, node_1, node_3, node_2, node_5, 0, 0, 1))
                    #     count += 1
                    #     elems.append(TetraElement("SOLIDTETRA", count, node_2, node_3, node_4, node_8, 0, 0, 1))
                    #     count += 1
                    #     elems.append(TetraElement("SOLIDTETRA", count, node_2, node_3, node_8, node_5, 0, 0, 1))
                    #     count += 1
                    #     elems.append(TetraElement("SOLIDTETRA", count, node_2, node_6, node_5, node_8, 0, 0, 1))
                    #     count += 1
                    #     elems.append(TetraElement("SOLIDTETRA", count, node_3, node_7, node_8, node_5, 0, 0, 1))
                    #     count += 1
                    # else:
                    #     elems.append(TetraElement("SOLIDTETRA", count, node_1, node_3, node_4, node_7, 0, 0, 1))
                    #     count += 1
                    #     elems.append(TetraElement("SOLIDTETRA", count, node_4, node_7, node_8, node_6, 0, 0, 1))
                    #     count += 1
                    #     elems.append(TetraElement("SOLIDTETRA", count, node_1, node_4, node_2, node_6, 0, 0, 1))
                    #     count += 1
                    #     elems.append(TetraElement("SOLIDTETRA", count, node_1, node_6, node_5, node_7, 0, 0, 1))
                    #     count += 1
                    #     elems.append(TetraElement("SOLIDTETRA", count, node_1, node_7, node_4, node_6, 0, 0, 1))
                    #     count += 1
                    for elem in elems:
                        self._elements.append(elem)

    def _GenerateSupport(self):
        for kdx in range(0, self._module_z+1):
            for jdx in range(0, self._module_y+1):
                for idx in range(0, self._module_x+1):
                    if idx==0:
                        no = kdx*(self._module_x+1)*(self._module_y+1) + jdx*(self._module_x+1) + (idx+1)
                        self._constraints.append(SupportItem("BC_1", no, True, False))

    def _GenerateLoad(self):
        for node in self._nodegroup['side']:
            support = SupportItem("BC_Side", node._id, True, False)
            support.JustZ()
            self._constraints.append(support)
        for node in self._nodegroup['bottom']:
            support = SupportItem("BC_Bottom", node._id, True, False)
            self._constraints.append(support)

    def _WriteBegin(self, txtfile):
        #material
        txtfile.Write("/MATERIAL/\r\n")
        txtfile.Write("Mat-1 1 3E10 77.3E9 2000 0.3\r\n")
        txtfile.Write("##\r\n")
        #section
        txtfile.Write("/SECTION/\r\n")
        txtfile.Write("##\r\n")