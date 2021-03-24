from utility.UtilityBase import FPMFeed, NodeItem, ElementBaseItem, LoadItem, NodeSetItem, FixedItem
from utility.ModelGeneratorBase import LineElement, TriElement, TetraElement, ModelGeneratorBase
import math

class FrameModelGenerator(ModelGeneratorBase):

    nodeset_bottom = NodeSetItem("bottom")

    def __init__(self, xsize, ysize, zsize, module_x, module_y, module_z):
        ModelGeneratorBase.__init__(self)
        self._size_x = xsize
        self._size_y = ysize
        self._size_z = zsize
        self._module_x = module_x
        self._module_y = module_y
        self._module_z = module_z

    def _GenerateNode(self):
        dx = self._size_x/self._module_x
        dy = self._size_y/self._module_y
        dz = self._size_z/self._module_z
        count = 1
        for zdx in range(0, self._module_z+1):
           for jdx in range(0, self._module_y+1):
               for idx in range(0, self._module_x+1):
                    no = count
                    x = idx * dx - 0.5 * self._size_x
                    y = jdx * dy - 0.5 * self._size_y
                    z = zdx * dz
                    nodeItem = NodeItem(no, x, y, z)
                    if zdx==0:
                        self.nodeset_bottom.AddNode(no)
                    self._nodes.append(nodeItem)
                    count += 1

    def _GenerateElement(self):
        count = 1
        for zdx in range(0, self._module_z):
            for jdx in range(0, self._module_y+1):
                for idx in range(0, self._module_x):
                    start_index_z = (zdx+1)*(self._module_x+1)*(self._module_y+1)
                    node_1 = start_index_z + jdx*(self._module_x+1) + idx + 1
                    node_2 = start_index_z + jdx*(self._module_x+1) + idx + 2
                    self._elements.append(LineElement("BEAM", count, node_1, node_2, 0, 1, 2))
                    count += 1
            for idx in range(0, self._module_x+1):
                for jdx in range(1, self._module_y+1):
                    start_index_z = (zdx+1)*(self._module_x+1)*(self._module_y+1)
                    node_1 = start_index_z + (jdx-1) * (self._module_x+1) + idx + 1
                    node_2 = start_index_z + jdx * (self._module_x+1) + idx + 1
                    self._elements.append(LineElement("BEAM", count, node_1, node_2, 0, 1, 2))
                    count += 1
            for jdx in range(0, self._module_y+1):
                for idx in range(0, self._module_x+1):
                    planer_count = (self._module_x+1)*(self._module_y+1)
                    node_1 = planer_count*zdx + jdx*(self._module_x+1) + idx + 1
                    node_2 = planer_count*(zdx+1) + jdx*(self._module_x+1) + idx + 1
                    colume = LineElement("BEAM", count, node_1, node_2, 0, 2, 2)
                    self._elements.append(colume)
                    count += 1

    def _GenerateSupport(self):
        self._constraints.append(FixedItem("fixed_bottom_x", self.nodeset_bottom, [1]))
        self._constraints.append(FixedItem("fixed_bottom_yz", self.nodeset_bottom, [2, 3]))

    def _GenerateLoad(self):
        pass

    def _GenerateNodeSet(self):
        self._nodesets.append(self.nodeset_bottom)

    def _WriteBegin(self, txtfile):
        txtfile.Write("/MATERIAL/\r\n")
        txtfile.Write("1, Mat-Soil, TYPE, DP\r\n")
        txtfile.Write("1, Mat-Soil, DENS, 2700\r\n")   
        txtfile.Write("1, Mat-Soil, EM, 13.23E9\r\n")
        txtfile.Write("1, Mat-Soil, NU, 0.25\r\n")
        txtfile.Write("1, Mat-Soil, DP, 30000, 30, 10\r\n")
        txtfile.Write("2, Mat-Struct, TYPE, LE\r\n")
        txtfile.Write("2, Mat-Struct, DENS, 7850\r\n")
        txtfile.Write("2, Mat-Struct, EM, 206E9\r\n")
        txtfile.Write("2, Mat-Struct, NU, 0.3\r\n")
        txtfile.Write("##\r\n")
        txtfile.Write("/SECTION/\r\n")
        txtfile.Write("1, Rect_Beam, TYPE, RECT\r\n")
        txtfile.Write("1, Rect_Beam, SHAPE, 0.2, 0.4\r\n")
        txtfile.Write("2, Round_Colume, TYPE, ROUND\r\n")
        txtfile.Write("2, Round_Colume, SHAPE, 0.8\r\n")
        txtfile.Write("##\r\n")
        txtfile.Write("/SEQUENCE/\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 0, 0\r\n")
        txtfile.Write("##\r\n")

    def _WriteEnd(self, txtfile):
        txtfile.Write("/STEP/\r\n")
        txtfile.Write("step_init, TYPE, INITIAL\r\n")
        txtfile.Write("step_gravity, TYPE, STATIC\r\n")
        txtfile.Write("step_gravity, TIME, 2.5e-4, 5\r\n")
        txtfile.Write("step_gravity, LOADING, RAMP, 0.5\r\n")
        txtfile.Write("step_gravity, DAMPING, ON, 100\r\n")
        txtfile.Write("step_gravity, OUTPUT, 10\r\n")
        txtfile.Write("step_gravity, CONSTRAINT, fixed_bottom_x, N, fixed_bottom_yz, Y\r\n")
        txtfile.Write("step_gravity, LOAD, GRAVITY_SET, Y\r\n")
        txtfile.Write("step_seismic, TYPE, DYNA\r\n")
        txtfile.Write("step_seismic, TIME, 2.5e-4, 20\r\n")
        txtfile.Write("step_seismic, DAMPING, ON, 0.1\r\n")
        txtfile.Write("step_seismic, OUTPUT, 200\r\n")
        txtfile.Write("step_seismic, CONSTRAINT, DISP_SET, Y\r\n")
        txtfile.Write("##\r\n")
        pass