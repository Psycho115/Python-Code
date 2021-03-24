from UtilityBase import FPMFeed, NodeItem, ElementBaseItem, SupportItem, LoadItem, CoupleItem
from ModelGeneratorBase import LineElement, TriElement, TetraElement, ModelGeneratorBase
import math
from random import randint

class SlideSoilModelGenerator(ModelGeneratorBase):

    bottom_elems = []
    hole_elems = []

    soilCons = {}

    m = 2000000

    def __init__(self):
        ModelGeneratorBase.__init__(self)
        self.node_count_accumulated = 0

########################################################
## Soil

    def _InitSoil(self, xsize, ysize, zsize, module_x, module_y, module_z):
        ModelGeneratorBase.__init__(self)
        self._soil_size_x = xsize
        self._soil_size_y = ysize
        self._soil_size_z = zsize
        self._soil_module_x = module_x
        self._soil_module_y = module_y
        self._soil_module_z = module_z

    def _LogNodeCount(self):
        self.node_count_accumulated = len(self._nodes)

    def _GenerateSoilNode(self):
        count = self.node_count_accumulated + 1
        soiltop = []
        dx = self._soil_size_x/self._soil_module_x
        dy = self._soil_size_y/self._soil_module_y
        dz = self._soil_size_z/self._soil_module_z

        for kdx in range(0, self._soil_module_z+1):
            for jdx in range(0, self._soil_module_y+1):
                for idx in range(0, self._soil_module_x+1):
                    no = count
                    x = idx * dx - 0.5 * self._soil_size_x
                    y = jdx * dy - 0.5 * self._soil_size_y

                    ratio_z = 1.0

                    if idx < self._soil_module_x / 3.0:
                        ratio_z = 1.0
                    elif idx >= self._soil_module_x / 3.0 and idx < 2.0 * self._soil_module_x / 3.0:
                        ratio_z = -1.5 * idx / self._soil_module_x+1.5
                    else:
                        ratio_z = 0.5

                    z = - kdx * dz * ratio_z

                    node_item = NodeItem(no, x, y, z)

                    if kdx == 0:
                        soiltop.append(node_item)

                    if idx == self._soil_module_x or idx == 0:
                        if not self.soilCons.has_key(no):
                            self.soilCons.setdefault(no, [])
                        self.soilCons[no].append('x')
                    if jdx == self._soil_module_y or jdx == 0:
                        if not self.soilCons.has_key(no):
                            self.soilCons.setdefault(no, [])
                        self.soilCons[no].append('y')
                    if kdx == 0:
                        if not self.soilCons.has_key(no):
                            self.soilCons.setdefault(no, [])
                        self.soilCons[no].append('x')
                        self.soilCons[no].append('y')
                        self.soilCons[no].append('z')

                    self._nodes.append(node_item)
                    count += 1

        self._nodegroup['soiltop'] = soiltop

    def _GenerateSoilElement(self):
        count = 1
        for kdx in range(0, self._soil_module_z):
            for jdx in range(0, self._soil_module_y):
                for idx in range(0, self._soil_module_x):
                    node_1 = self.node_count_accumulated + kdx*(self._soil_module_x+1)*(self._soil_module_y+1) + jdx*(self._soil_module_x+1) + (idx+1)
                    node_2 = self.node_count_accumulated + kdx*(self._soil_module_x+1)*(self._soil_module_y+1) + jdx*(self._soil_module_x+1) + (idx+2)
                    node_3 = self.node_count_accumulated + kdx*(self._soil_module_x+1)*(self._soil_module_y+1) + (jdx+1)*(self._soil_module_x+1) + (idx+1)
                    node_4 = self.node_count_accumulated + kdx*(self._soil_module_x+1)*(self._soil_module_y+1) + (jdx+1)*(self._soil_module_x+1) + (idx+2)
                    node_5 = self.node_count_accumulated + (kdx+1)*(self._soil_module_x+1)*(self._soil_module_y+1) + jdx*(self._soil_module_x+1) + (idx+1)
                    node_6 = self.node_count_accumulated + (kdx+1)*(self._soil_module_x+1)*(self._soil_module_y+1) + jdx*(self._soil_module_x+1) + (idx+2)
                    node_7 = self.node_count_accumulated + (kdx+1)*(self._soil_module_x+1)*(self._soil_module_y+1) + (jdx+1)*(self._soil_module_x+1) + (idx+1)
                    node_8 = self.node_count_accumulated + (kdx+1)*(self._soil_module_x+1)*(self._soil_module_y+1) + (jdx+1)*(self._soil_module_x+1) + (idx+2)
                    elems = []
                    if (idx%2+jdx%2+kdx%2)%2==1:
                        elems.append(TetraElement("SOLID", count, node_1, node_3, node_2, node_5, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_2, node_3, node_4, node_8, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_2, node_3, node_8, node_5, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_2, node_6, node_5, node_8, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_3, node_7, node_8, node_5, 0, 0, 1))
                        count += 1
                    else:
                        elems.append(TetraElement("SOLID", count, node_1, node_3, node_4, node_7, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_4, node_7, node_8, node_6, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_1, node_4, node_2, node_6, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_1, node_6, node_5, node_7, 0, 0, 1))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_1, node_7, node_4, node_6, 0, 0, 1))
                        count += 1

                    # if abs(jdx-0.5*self._soil_module_y) <=1 and abs(kdx-0.5*self._soil_module_z) <=1:
                    #     for elem in elems:
                    #         self.hole_elems.append(elem)
                    # else:
                    #     for elem in elems:
                    #         self._elements.append(elem)

                    for elem in elems:
                        self._elements.append(elem)

    def _GenerateSoilSupport(self):
        nodes = self.soilCons.keys()
        nodes.sort()
        for node in nodes:
            support = SupportItem("BC", node, False, False)
            for dof in self.soilCons[node]:
                if dof == 'x':
                    support._dx = 2
                if dof == 'y':
                    support._dy = 2
                if dof == 'z':
                    support._dz = 2   
            self._constraints.append(support)

    def _GenerateSoilLoad(self):
        # area = self._soil_size_x * self._soil_size_y
        # f = area * self._pressure / len(self._nodegroup['soiltopall'])
        # for node in self._nodegroup['soiltopall']:
        #     load = LoadItem("Load_Pressure", node._id, 0.0, 0.0, f)
        #     self._loads.append(load)
        # for node in self._nodes:
        #     load = LoadItem("Load_Body", node._id, 0.0, 0.0, self._body_load)
        #     self._loads.append(load)
        pass

    def _GenerateSoilModel(self):
        self._GenerateSoilNode()
        self._GenerateSoilElement()
        self._GenerateSoilSupport()

####################################################################
## Control

    def _WriteBegin(self, txtfile):
        #material
        txtfile.Write("/MATERIAL/\r\n")
        txtfile.Write("1, Mat_DP, DP, 10e6, 9.15e7, 1540, 0.33, 3560, 17.9, 17.9\r\n")
        txtfile.Write("##\r\n")
        #section
        # txtfile.Write("/SECTION/\r\n")
        # txtfile.Write("1, Rect_Beam, RECT, 0.2, 0.4\r\n")
        # txtfile.Write("2, Round_Colume, ROUND, 0.8\r\n")
        # txtfile.Write("##\r\n")

    def GenerateModel(self):
        self._GenerateSoilModel()

        