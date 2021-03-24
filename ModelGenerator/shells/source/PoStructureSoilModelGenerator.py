from UtilityBase import FPMFeed, NodeItem, ElementBaseItem, SupportItem, LoadItem, CoupleItem
from ModelGeneratorBase import LineElement, TriElement, TetraElement, ModelGeneratorBase
import math

class PoStructSoilModelGenerator(ModelGeneratorBase):

    bottom_elems = []
    hole_elems = []

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
        self.node_count_accumulated += len(self._nodes)

    def _GenerateSoilNode(self):
        count = self.node_count_accumulated + 1
        soilside = []
        soilbottom = []
        soiltop = []
        soiltopall = []    
        dx = self._soil_size_x/self._soil_module_x
        dy = self._soil_size_y/self._soil_module_y
        dz = self._soil_size_z/self._soil_module_z
        structx = self._struct_size_x * 0.5
        structy = self._struct_size_y * 0.5
        for kdx in range(0, self._soil_module_z+1):
            for jdx in range(0, self._soil_module_y+1):
                for idx in range(0, self._soil_module_x+1):
                    no = count
                    x = idx * dx - 0.5 * self._soil_size_x
                    y = jdx * dy - 0.5 * self._soil_size_y
                    z = - kdx * dz
                    node_item = NodeItem(no, x, y, z)
                    if (idx == self._soil_module_x or idx == 0 or jdx == self._soil_module_y or jdx == 0) and kdx != self._soil_module_z:
                        soilside.append(node_item)
                    if kdx == self._soil_module_z:
                        soilbottom.append(node_item)
                    if abs(x)<=structx and abs(y)<=structy and kdx == 0:
                        soiltop.append(node_item)
                    if kdx == 0:
                        soiltopall.append(node_item)
                    self._nodes.append(node_item)
                    count += 1
        self._nodegroup['soilside'] = soilside
        self._nodegroup['soilbottom'] = soilbottom
        self._nodegroup['soiltop'] = soiltop
        self._nodegroup['soiltopall'] = soiltopall

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
                    for elem in elems:
                        self._elements.append(elem)

    def _GenerateSoilSupport(self):
        for node in self._nodegroup['soilside']:
            support = SupportItem("BC_SoilSide", node._id, True, False)
            support.JustZ()
            self._constraints.append(support)
        for node in self._nodegroup['soilbottom']:
            support = SupportItem("BC_SoilBottom", node._id, True, False)
            self._constraints.append(support)

    def _GenerateSoilLoad(self):
        area = self._soil_size_x * self._soil_size_y
        f = area * self._pressure / len(self._nodegroup['soiltopall'])
        for node in self._nodegroup['soiltopall']:
            load = LoadItem("Load_Pressure", node._id, 0.0, 0.0, f)
            self._loads.append(load)
        for node in self._nodes:
            load = LoadItem("Load_Body", node._id, 0.0, 0.0, self._body_load)
            self._loads.append(load)

    def _GenerateSoilModel(self):
        self._GenerateSoilNode()
        self._GenerateSoilElement()
        self._GenerateSoilSupport()
        self._GenerateSoilLoad()

####################################################################
## Struct

    def _InitStructure(self, xsize, ysize, zsize, module_x, module_y, module_z):
        ModelGeneratorBase.__init__(self)
        self._struct_size_x = xsize
        self._struct_size_y = ysize
        self._struct_size_z = zsize
        self._struct_module_x = module_x
        self._struct_module_y = module_y
        self._struct_module_z = module_z

    def _GenerateStructNode(self):
        structbase = []
        dx = self._struct_size_x/self._struct_module_x
        dy = self._struct_size_y/self._struct_module_y
        dz = self._struct_size_z/self._struct_module_z
        count = self.node_count_accumulated + 1
        for zdx in range(0, self._struct_module_z+1):
           for jdx in range(0, self._struct_module_y+1):
               for idx in range(0, self._struct_module_x+1):
                    no = count
                    x = idx * dx - 0.5 * self._struct_size_x
                    y = jdx * dy - 0.5 * self._struct_size_y
                    z = zdx * dz
                    nodeItem = NodeItem(no, x, y, z)
                    if zdx==0:
                        structbase.append(nodeItem)
                    self._nodes.append(nodeItem)
                    count += 1
        self._nodegroup['structbase'] = structbase

    def _GenerateStructElement(self):
        count = 1
        for zdx in range(0, self._struct_module_z):
            for jdx in range(0, self._struct_module_y+1):
                for idx in range(0, self._struct_module_x):
                    start_index_z = (zdx+1)*(self._struct_module_x+1)*(self._struct_module_y+1) + self.node_count_accumulated
                    node_1 = start_index_z + jdx*(self._struct_module_x+1) + idx + 1
                    node_2 = start_index_z + jdx*(self._struct_module_x+1) + idx + 2
                    self._elements.append(LineElement("BEAM", count, node_1, node_2, 0, 1, 2))
                    count += 1
            for idx in range(0, self._struct_module_x+1):
                for jdx in range(1, self._struct_module_y+1):
                    start_index_z = (zdx+1)*(self._struct_module_x+1)*(self._struct_module_y+1) + self.node_count_accumulated
                    node_1 = start_index_z + (jdx-1) * (self._struct_module_x+1) + idx + 1
                    node_2 = start_index_z + jdx * (self._struct_module_x+1) + idx + 1
                    self._elements.append(LineElement("BEAM", count, node_1, node_2, 0, 1, 2))
                    count += 1
            for jdx in range(0, self._struct_module_y+1):
                for idx in range(0, self._struct_module_x+1):
                    planer_count = (self._struct_module_x+1)*(self._struct_module_y+1)
                    node_1 = self.node_count_accumulated + planer_count*zdx + jdx*(self._struct_module_x+1) + idx + 1
                    node_2 = self.node_count_accumulated + planer_count*(zdx+1) + jdx*(self._struct_module_x+1) + idx + 1
                    colume = LineElement("BEAM", count, node_1, node_2, 0, 2, 2)
                    self._elements.append(colume)
                    if zdx == 0:
                        self.bottom_elems.append(colume)
                    count += 1

    def _GenerateStructSupport(self):
        for node in self._nodegroup['structbase']:
            self._constraints.append(SupportItem("BC_Struct", node._id, True, True))

    def _GenerateStructLoad(self):
        pass

    def _GenerateStructModel(self):
        self._GenerateStructNode()
        self._GenerateStructElement()
        self._GenerateStructSupport()
        self._GenerateStructLoad()

####################################################################
## Couple

    def _AdjustNode(self):
        for elem in self.bottom_elems:
            old_id = elem._node_1
            new_id = 0
            oldNode = NodeItem(0, 0, 0, 0)
            for node in self._nodegroup['structbase']:
                if node._id == old_id:
                    oldNode = node
            for node in self._nodegroup['soiltop']:
                if node._x == oldNode._x and node._y == oldNode._y:
                    new_id = node._id
            elem._node_1 = new_id

####################################################################
## Load

    def _InitSoilLoad(self,pressure,bodyLoad):
        self._pressure = pressure
        self._body_load = bodyLoad

####################################################################
## Control

    def _WriteBegin(self, txtfile):
        #material
        txtfile.Write("/MATERIAL/\r\n")
        txtfile.Write("Mat-Soil     1   15E7	6E7     1650    0.3	\r\n")
        txtfile.Write("Mat-Struct   1   206E9   79E9    7850    0.3\r\n")
        txtfile.Write("##\r\n")
        #section
        txtfile.Write("/SECTION/\r\n")
        txtfile.Write("Rect_Beam 2 0.2 0.4\r\n")
        txtfile.Write("Round_Colume 3 0.8\r\n")
        txtfile.Write("##\r\n")

    def GenerateModel(self):
        self._GenerateStructModel()
        self._LogNodeCount()
        self._GenerateSoilModel()
        self._AdjustNode()

        