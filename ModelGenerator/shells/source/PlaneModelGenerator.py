from utility.UtilityBase import FPMFeed, NodeItem, ElementBaseItem, SupportItem, LoadItem
from utility.ModelGeneratorBase import TriElement, ModelGeneratorBase
import math

class PlaneTubeModelGenerator(ModelGeneratorBase):

    # r - outer radius t - thick

    def __init__(self, R, t, module_number_x, module_number_y, p_inner, p_outer):
        ModelGeneratorBase.__init__(self)
        self._t = t
        self._module_number_x = module_number_x
        self._module_number_y = module_number_y
        self._R = R
        self._p_inner = p_inner
        self._p_outer = p_outer

    def _GenerateNode(self):
        count = 1
        dTheta = 90.0 / self._module_number_x
        dt = self._t / self._module_number_y
        for jdx in range(0, self._module_number_y+1):
            for idx in range(0, self._module_number_x+1):
                no = count
                r = self._R - jdx * dt
                x = r * math.cos(math.radians(idx*dTheta))
                y = r * math.sin(math.radians(idx*dTheta))
                z = 0
                self._nodes.append(NodeItem(no, x, y, z))
                count += 1

    def _GenerateElement(self):
        count = 1
        for jdx in range(0, self._module_number_y):
            for idx in range(0, self._module_number_x):
                node_1 = jdx*(self._module_number_x+1) + idx + 1
                node_2 = jdx*(self._module_number_x+1) + idx + 2
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 1
                self._elements.append(TriElement("TRI_PLANE", count, node_1, node_2, node_3, 0, 1, 1))
                count += 1

                node_1 = jdx*(self._module_number_x+1) + idx + 2
                node_2 = (jdx+1)*(self._module_number_x+1) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 2
                self._elements.append(TriElement("TRI_PLANE", count, node_1, node_2, node_3, 0, 1, 1))
                count += 1

    def _GenerateSupport(self):
        for jdx in range(0, self._module_number_y+1):
            for idx in range(0, self._module_number_x+1):
                if idx==0:
                    no = jdx * (self._module_number_x+1) + idx + 1
                    bc = SupportItem('BC_1', no, True, False)
                    bc.FreeDofs(['x'])
                    self._constraints.append(bc)
                if idx==self._module_number_x:
                    no = jdx * (self._module_number_x+1) + idx + 1
                    bc = SupportItem('BC_1', no, True, False)
                    bc.FreeDofs(['y'])
                    self._constraints.append(bc)

    def _GenerateLoad(self):
        inner = 0.25 * 3.14 * self._p_inner * (self._R - self._t) / self._module_number_x
        outer = 0.25 * 3.14 * self._p_outer * self._R / self._module_number_x
        for jdx in range(0, self._module_number_y+1):
            for idx in range(0, self._module_number_x+1):
                if jdx == 0:
                    if math.fabs(outer) < 1e-15:
                        continue
                    no = jdx * (self._module_number_x+1) + idx + 1
                    node = self._nodes[no-1]
                    direction = node.GetDir()
                    if idx == 0 or idx == self._module_number_x:
                        self._loads.append(LoadItem('Pressure_outer',no,outer*direction[0],outer*direction[1],0))
                    else:
                        self._loads.append(LoadItem('Pressure_outer',no,2*outer*direction[0],2*outer*direction[1],0))
                if jdx == self._module_number_y:
                    if math.fabs(inner) < 1e-15:
                        continue
                    no = jdx * (self._module_number_x+1) + idx + 1
                    node = self._nodes[no-1]
                    direction = node.GetDir()
                    if idx == 0 or idx == self._module_number_x:
                        self._loads.append(LoadItem('Pressure_inner',no,inner*direction[0],inner*direction[1],0))
                    else:
                        self._loads.append(LoadItem('Pressure_inner',no,2*inner*direction[0],2*inner*direction[1],0))

    def _WriteBegin(self, txtfile):
        #material
        txtfile.Write("/MATERIAL/\r\n")
        txtfile.Write("Mat_DP 6 2.6e8 9.15e7 1900 0.42 19000 31 31\r\n")
        txtfile.Write("##\r\n")
        #section
        txtfile.Write("/SECTION/\r\n")
        txtfile.Write("Plane 6 0\r\n")
        txtfile.Write("##\r\n")


class PlaneSquareModelGenerator(ModelGeneratorBase):

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
                self._nodes.append(NodeItem(no, x, y, z))
                count += 1

    def _GenerateElement(self):
        count = 1
        for jdx in range(0, self._module_number_y):
            for idx in range(0, self._module_number_x):
                node_1 = jdx*(self._module_number_x+1) + idx + 1
                node_2 = jdx*(self._module_number_x+1) + idx + 2
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 1
                self._elements.append(TriElement("TRI_PLANE", count, node_1, node_2, node_3, 0, 1, 1))
                count += 1

                node_1 = jdx*(self._module_number_x+1) + idx + 2
                node_2 = (jdx+1)*(self._module_number_x+1) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 2
                self._elements.append(TriElement("TRI_PLANE", count, node_1, node_2, node_3, 0, 1, 1))
                count += 1

    def _GenerateSupport(self):
        for jdx in range(0, self._module_number_y+1):
            for idx in range(0, self._module_number_x+1):
                if idx==0:
                    no = jdx * (self._module_number_x+1) + idx + 1
                    bc = SupportItem('BC_1', no, True, False)
                    self._constraints.append(bc)

    def _GenerateLoad(self):
        force = self._force / (self._module_number_y + 1)
        for jdx in range(0, self._module_number_y+1):
            for idx in range(0, self._module_number_x+1):
                if idx==self._module_number_x:
                    no = jdx * (self._module_number_x+1) + idx + 1
                    self._loads.append(LoadItem('Load_1',no,force,0.0,0.0))

    def _WriteBegin(self, txtfile):
        #material
        txtfile.Write("/MATERIAL/\r\n")
        txtfile.Write("DP 6 1e+7 4.2 2000 0.2 0.0 30 30\r\n")
        txtfile.Write("##\r\n")
        #section
        txtfile.Write("/SECTION/\r\n")
        txtfile.Write("Plane 6 0\r\n")
        txtfile.Write("##\r\n")