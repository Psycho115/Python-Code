from UtilityBase import FPMFeed, NodeItem, ElementBaseItem, SupportItem, LoadItem
from ModelGeneratorBase import LineElement, TriElement, TetraElement, ModelGeneratorBase
import math

class MembraneModelGenerator(object):

    _nodes = []
    _elements = []
    _constraints = []
    _loads = []

    def __init__(self, length, height, module_number_x):
        self._length = length
        self._height = height
        self._module_number_x = module_number_x
        self._module_number_y = module_number_x

    def GenerateModel(self):
        self._GenerateNode()
        self._GenerateElement()
        self._GenerateSupport()
        #self._GenerateLoad()

    def WriteFile(self, filename):
        txtfile = TXTFeed(filename)
        self._WriteBegin(txtfile)
        self._WriteNodes(txtfile)
        self._WriteElements(txtfile)
        self._WriteContraints(txtfile)
        #self._WriteLoads(txtfile)
        txtfile.Finished()

    def _GenerateNode(self):
        count = 1
        for jdx in range(0, self._module_number_x+1):
            for idx in range(0, self._module_number_x+1):
                no = count
                x = idx * self._length
                y = jdx * self._length
                h_max = self._height
                dh = self._height / self._module_number_x
                if idx <= self._module_number_x-jdx:
                    z = dh * (idx + jdx)
                else:
                    z = 2 * h_max - dh * (idx + jdx)
                self._nodes.append(NodeItem(no, x, y, z))
                count += 1
                #inner grid
        for jdx in range(0, self._module_number_x):
            for idx in range(0, self._module_number_x):
                no = count
                x = idx * self._length + 0.5 * self._length
                y = jdx * self._length + 0.5 * self._length
                h_max = self._height
                dh = self._height / self._module_number_x
                if idx <= self._module_number_x-jdx-1:
                    z = dh * (idx + jdx + 1)
                else:
                    z = 2 * h_max - dh * (idx + jdx + 1)
                self._nodes.append(NodeItem(no, x, y, z))
                count += 1

    def _GenerateElement(self):
        count = 1
        innerStartCount = (self._module_number_x + 1) * (self._module_number_x + 1)
        for jdx in range(0, self._module_number_x):
            for idx in range(0, self._module_number_x):
                node_1 = jdx*(self._module_number_x+1) + idx + 1
                node_2 = jdx*(self._module_number_x+1) + idx + 2
                node_3 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                self._elements.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = jdx*(self._module_number_x+1) + idx + 2
                node_2 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 2
                self._elements.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_2 = (jdx+1)*(self._module_number_x+1) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 2
                self._elements.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = jdx*(self._module_number_x+1) + idx + 1
                node_2 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 1
                self._elements.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

    def _GenerateSupport(self):
        for jdx in range(0, self._module_number_x+1):
            for idx in range(0, self._module_number_x+1):
                if idx==0 or idx==self._module_number_x or jdx==0 or jdx==self._module_number_x:
                    no = jdx * (self._module_number_x+1) + idx + 1
                    dof = True
                    rdof = False
                    self._constraints.append(SupportItem(1, no, dof, rdof))

    def _GenerateLoad(self):
        for jdx in range(0, self._module_number_x+1):
            for idx in range(0, self._module_number_x+1):
                if not (idx==0 or idx==self._module_number_x or jdx==0 or jdx==self._module_number_x):
                    no = jdx * (self._module_number_x+1) + idx + 1
                    self._loads.append(LoadItem(1, no, 0, 0, 10))

    def _WriteBegin(self, txtfile):
        #start
        txtfile.Write("/BEGIN_MST_SPECIAL_DATA/\r\n")
        #material
        txtfile.Write("/MATERIAL INFO/\r\n")
        txtfile.Write("1 6E11 1E3 1150 0.38\r\n")
        txtfile.Write("##\r\n")
        #section
        txtfile.Write("/SECTION PROPERTIES/\r\n")
        txtfile.Write("20 1 0.001\r\n")
        txtfile.Write("##\r\n")
        #prestress
        txtfile.Write("/PRESTRESS/\r\n")
        txtfile.Write("1 1 200000 200000 1 0 0 0 1 0\r\n")
        txtfile.Write("##\r\n")
        #solvestep
        txtfile.Write("/SOLVESTEP SETTINGS/\r\n")
        txtfile.Write("/STEP/\r\n")
        txtfile.Write("0\r\n")
        txtfile.Write("1\r\n")
        txtfile.Write("/STEP_END/\r\n")
        txtfile.Write("##\r\n")

    def _WriteNodes(self, txtfile):
        txtfile.Write("/NODECORD2/\r\n")
        for node in self._nodes:
            node.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteElements(self, txtfile):
        txtfile.Write("/MEM_ELEMS_7/\r\n")
        for element in self._elements:
            element.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteContraints(self, txtfile):
        txtfile.Write("/SUPPORT INFORMATION/\r\n")
        for support in self._constraints:
            support.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteLoads(self, txtfile):
        txtfile.Write("/DEADLOAD/\r\n")
        for load in self._loads:
            load.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

class MembraneCableModelGenerator(object):

    _nodes = []
    _elements_cable = []
    _elements_mem = []
    _constraints = []
    _loads = []

    def __init__(self, length, height, module_number_x):
        self._length = length / module_number_x
        self._height = height
        self._module_number_x = module_number_x

    def GenerateModel(self):
        self._GenerateNode()
        self._GenerateMemElement()
        self._GenerateCableElement()
        self._GenerateSupport()
        self._GenerateLoad()

    def WriteFile(self, filename):
        txtfile = TXTFeed(filename)
        self._WriteBegin(txtfile)
        self._WriteNodes(txtfile)
        self._WriteMemElements(txtfile)
        self._WriteCableElements(txtfile)
        self._WriteContraints(txtfile)
        # self._WriteLoads(txtfile)
        txtfile.Finished()

    def _GenerateNode(self):
        count = 1
        #grid
        for jdx in range(0, self._module_number_x+1):
            for idx in range(0, self._module_number_x+1):
                no = count
                x = idx * self._length
                y = jdx * self._length
                h_max = self._height
                dh = self._height / self._module_number_x
                if idx <= self._module_number_x-jdx:
                    z = dh * (idx + jdx)
                else:
                    z = 2 * h_max - dh * (idx + jdx)
                self._nodes.append(NodeItem(no, x, y, z))
                count += 1
        #inner grid
        for jdx in range(0, self._module_number_x):
            for idx in range(0, self._module_number_x):
                no = count
                x = idx * self._length + 0.5 * self._length
                y = jdx * self._length + 0.5 * self._length
                h_max = self._height
                dh = self._height / self._module_number_x
                if idx <= self._module_number_x-jdx-1:
                    z = dh * (idx + jdx + 1)
                else:
                    z = 2 * h_max - dh * (idx + jdx + 1)
                self._nodes.append(NodeItem(no, x, y, z))
                count += 1

    def _GenerateMemElement(self):
        count = 1
        innerStartCount = (self._module_number_x + 1) * (self._module_number_x + 1)
        for jdx in range(0, self._module_number_x):
            for idx in range(0, self._module_number_x):
                node_1 = jdx*(self._module_number_x+1) + idx + 1
                node_2 = jdx*(self._module_number_x+1) + idx + 2
                node_3 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = jdx*(self._module_number_x+1) + idx + 2
                node_2 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 2
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_2 = (jdx+1)*(self._module_number_x+1) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 2
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = jdx*(self._module_number_x+1) + idx + 1
                node_2 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 1
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

    def _GenerateCableElement(self):
        count = 1
        sub1 = []
        sub2 = []
        sub3 = []
        sub4 = []
        for node in self._nodes:
            if node._x==0:
                sub1.append(node)
            if node._x==self._module_number_x*self._length:
                sub3.append(node)
            if node._y==0:
                sub2.append(node)
            if node._y==self._module_number_x*self._length:
                sub4.append(node)
            sub = [sub1,sub2,sub3,sub4]
        for i in range(0,self._module_number_x):
            for s in sub:
                node_1 = s[i]._id
                node_2 = s[i+1]._id
                self._elements_cable.append(LineElement(count, node_1, node_2, 2, 2, 2))

    def _GenerateSupport(self):
        for jdx in range(0, self._module_number_x+1):
            for idx in range(0, self._module_number_x+1):
                if (idx==0 or idx==self._module_number_x) and (jdx==0 or jdx==self._module_number_x):
                    no = jdx * (self._module_number_x+1) + idx + 1
                    dof = True
                    rdof = False
                    self._constraints.append(SupportItem(1, no, dof, rdof))

    def _GenerateLoad(self):
        for jdx in range(0, self._module_number_x+1):
            for idx in range(0, self._module_number_x+1):
                if not (idx==0 or idx==self._module_number_x or jdx==0 or jdx==self._module_number_x):
                    no = jdx * (self._module_number_x+1) + idx + 1
                    self._loads.append(LoadItem(1, no, 0, 0, 10))

    def _WriteBegin(self, txtfile):
        #start
        txtfile.Write("/BEGIN_MST_SPECIAL_DATA/\r\n")
        #material
        txtfile.Write("/MATERIAL INFO/\r\n")
        txtfile.Write("1 6E8 1E3 1150 0.38\r\n")
        txtfile.Write("1 1.9E11 1E3 7500 0.3\r\n")
        txtfile.Write("##\r\n")
        #section
        txtfile.Write("/SECTION PROPERTIES/\r\n")
        txtfile.Write("20 1 0.0013\r\n")
        txtfile.Write("7  1 2E-4 0 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0 0\r\n")
        txtfile.Write("##\r\n")
        #prestress
        txtfile.Write("/PRESTRESS/\r\n")
        txtfile.Write("1 1 200000\r\n")
        txtfile.Write("2 0 0      16000\r\n")
        txtfile.Write("##\r\n")
        #solvestep
        txtfile.Write("/SOLVESTEP SETTINGS/\r\n")
        txtfile.Write("/STEP/\r\n")
        txtfile.Write("0\r\n")
        txtfile.Write("1\r\n")
        txtfile.Write("/STEP_END/\r\n")
        txtfile.Write("##\r\n")

    def _WriteNodes(self, txtfile):
        txtfile.Write("/NODECORD2/\r\n")
        for node in self._nodes:
            node.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteMemElements(self, txtfile):
        txtfile.Write("/MEM_ELEMS_7/\r\n")
        for element in self._elements_mem:
            element.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteCableElements(self, txtfile):
        txtfile.Write("/CABLE_ELEMS_7/\r\n")
        for element in self._elements_cable:
            element.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteContraints(self, txtfile):
        txtfile.Write("/SUPPORT INFORMATION/\r\n")
        for support in self._constraints:
            support.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteLoads(self, txtfile):
        txtfile.Write("/DEADLOAD/\r\n")
        for load in self._loads:
            load.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

class SaddleModelGenerator(object):

    _nodes = []
    _elements_cable = []
    _elements_mem = []
    _constraints = []
    _loads = []

    def __init__(self, length, height, module_number_x):
        self._length = length
        self._height = height
        self._module_number_x = module_number_x

    def GenerateModel(self):
        self._GenerateNode()
        self._GenerateMemElement()
        self._GenerateSupport()
        self._GenerateLoad()

    def WriteFile(self, filename):
        txtfile = TXTFeed(filename)
        self._WriteBegin(txtfile)
        self._WriteNodes(txtfile)
        self._WriteMemElements(txtfile)
        self._WriteCableElements(txtfile)
        self._WriteContraints(txtfile)
        txtfile.Finished()

    def _GenerateNode(self):
        count = 1
        #grid
        for jdx in range(0, self._module_number_x+1):
            for idx in range(0, self._module_number_x+1):
                no = count
                x = idx * self._length - 0.5 * self._length * self._module_number_x
                y = jdx * self._length - 0.5 * self._length * self._module_number_x
                length = 0.5*self._length * self._module_number_x
                z = self._height * (1.0 - y*y/length/length)
                self._nodes.append(NodeItem(no, x, y, z))
                count += 1
        #inner grid
        for jdx in range(0, self._module_number_x):
            for idx in range(0, self._module_number_x):
                no = count
                x = idx * self._length + 0.5 * self._length - 0.5 * self._length * self._module_number_x
                y = jdx * self._length + 0.5 * self._length - 0.5 * self._length * self._module_number_x
                length = 0.5*self._length * self._module_number_x
                z = self._height * (1.0 - y*y/length/length)
                self._nodes.append(NodeItem(no, x, y, z))
                count += 1

    def _GenerateMemElement(self):
        count = 1
        innerStartCount = (self._module_number_x + 1) * (self._module_number_x + 1)
        for jdx in range(0, self._module_number_x):
            for idx in range(0, self._module_number_x):
                node_1 = jdx*(self._module_number_x+1) + idx + 1
                node_2 = jdx*(self._module_number_x+1) + idx + 2
                node_3 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = jdx*(self._module_number_x+1) + idx + 2
                node_2 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 2
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_2 = (jdx+1)*(self._module_number_x+1) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 2
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = jdx*(self._module_number_x+1) + idx + 1
                node_2 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 1
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

    def _GenerateSupport(self):
        for jdx in range(0, self._module_number_x+1):
            for idx in range(0, self._module_number_x+1):
                if idx==0 or idx==self._module_number_x or jdx==0 or jdx==self._module_number_x:
                    no = jdx * (self._module_number_x+1) + idx + 1
                    dof = True
                    rdof = False
                    self._constraints.append(SupportItem(1, no, dof, rdof))

    def _GenerateLoad(self):
        for jdx in range(0, self._module_number_x+1):
            for idx in range(0, self._module_number_x+1):
                if not (idx==0 or idx==self._module_number_x or jdx==0 or jdx==self._module_number_x):
                    no = jdx * (self._module_number_x+1) + idx + 1
                    self._loads.append(LoadItem(1, no, 0, 0, 10))

    def _WriteBegin(self, txtfile):
        #start
        txtfile.Write("/BEGIN_MST_SPECIAL_DATA/\r\n")
        #material
        txtfile.Write("/MATERIAL INFO/\r\n")
        txtfile.Write("1 6E8 1E3 1100 0.38\r\n")
        txtfile.Write("##\r\n")
        #section
        txtfile.Write("/SECTION PROPERTIES/\r\n")
        txtfile.Write("20 1 0.001\r\n")
        txtfile.Write("##\r\n")
        #prestress
        txtfile.Write("/PRESTRESS/\r\n")
        txtfile.Write("1 1 20000000 20000000 1 0 0 0 1 0\r\n")
        txtfile.Write("##\r\n")
        #solvestep
        txtfile.Write("/SOLVESTEP SETTINGS/\r\n")
        txtfile.Write("/STEP/\r\n")
        txtfile.Write("0\r\n")
        txtfile.Write("1\r\n")
        txtfile.Write("/STEP_END/\r\n")
        txtfile.Write("##\r\n")

    def _WriteNodes(self, txtfile):
        txtfile.Write("/NODECORD2/\r\n")
        for node in self._nodes:
            node.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteMemElements(self, txtfile):
        txtfile.Write("/MEM_ELEMS_7/\r\n")
        for element in self._elements_mem:
            element.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteCableElements(self, txtfile):
        txtfile.Write("/CABLE_ELEMS_7/\r\n")
        for element in self._elements_cable:
            element.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteContraints(self, txtfile):
        txtfile.Write("/SUPPORT INFORMATION/\r\n")
        for support in self._constraints:
            support.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteLoads(self, txtfile):
        txtfile.Write("/DEADLOAD/\r\n")
        for load in self._loads:
            load.LogToTxt(txtfile)
        txtfile.Write("##\r\n")


class UmbrellaModelGenerator(object):

    _nodes = []
    _elements_cable = []
    _elements_mast = []
    _elements_mem = []
    _constraints = []
    _loads = []

    def __init__(self, length, height, module_number_x):
        self._length = length
        self._height = height
        self._module_number_x = module_number_x

    def GenerateModel(self):
        self._GenerateNode()
        self._GenerateLineElement()
        self._GenerateMemElement()
        self._GenerateSupport()
        self._GenerateLoad()

    def WriteFile(self, filename):
        txtfile = TXTFeed(filename)
        self._WriteBegin(txtfile)
        self._WriteNodes(txtfile)
        self._WriteMemElements(txtfile)
        self._WriteCableElements(txtfile)
        self._WriteMastElements(txtfile)
        self._WriteContraints(txtfile)
        txtfile.Finished()

    def _GenerateNode(self):
        count = 1
        #grid
        for jdx in range(0, self._module_number_x+1):
            for idx in range(0, self._module_number_x+1):
                no = count
                x = idx * self._length - 0.5 * self._length * self._module_number_x
                y = jdx * self._length - 0.5 * self._length * self._module_number_x
                z = 0
                self._nodes.append(NodeItem(no, x, y, z))
                count += 1
        #inner grid
        for jdx in range(0, self._module_number_x):
            for idx in range(0, self._module_number_x):
                no = count
                x = idx * self._length + 0.5 * self._length - 0.5 * self._length * self._module_number_x
                y = jdx * self._length + 0.5 * self._length - 0.5 * self._length * self._module_number_x
                z = 0
                self._nodes.append(NodeItem(no, x, y, z))
                count += 1
        self._nodes.append(NodeItem(count, 0, 0, -self._height))

    def _GenerateMemElement(self):
        count = 1
        innerStartCount = (self._module_number_x + 1) * (self._module_number_x + 1)
        for jdx in range(0, self._module_number_x):
            for idx in range(0, self._module_number_x):
                node_1 = jdx*(self._module_number_x+1) + idx + 1
                node_2 = jdx*(self._module_number_x+1) + idx + 2
                node_3 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = jdx*(self._module_number_x+1) + idx + 2
                node_2 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 2
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_2 = (jdx+1)*(self._module_number_x+1) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 2
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = jdx*(self._module_number_x+1) + idx + 1
                node_2 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 1
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

    def _GenerateLineElement(self):
        #cables
        count = 1
        sub1 = []
        sub2 = []
        sub3 = []
        sub4 = []
        sub5 = []
        sub6 = []
        sub_edge = []
        sub_ridge = []
        sub_corner = []
        length = self._module_number_x*self._length
        for node in self._nodes:
            if node._z != 0.0:
                continue
            if node._x == - 0.5 * length:
                sub1.append(node)
            if node._x == 0.5 * length:
                sub3.append(node)
            if node._y ==  - 0.5 * length:
                sub2.append(node)
            if node._y == 0.5 * length:
                sub4.append(node)
            if node._x == node._y:
                sub5.append(node)
            if node._x == -node._y:
                sub6.append(node)
        sub_edge = [sub1,sub2,sub3,sub4]
        sub5.sort(cmp=lambda x,y:cmp(x._x,y._x))
        sub6.sort(cmp=lambda x,y:cmp(x._x,y._x))
        sub_ridge = [sub5,sub6]
        for i in range(0,self._module_number_x):
            for s in sub_edge:
                node_1 = s[i]._id
                node_2 = s[i+1]._id
                self._elements_cable.append(LineElement(count, node_1, node_2, 2, 2, 2))
                count += 1
        for i in range(0,2*self._module_number_x):
            for s in sub_ridge:
                node_1 = s[i]._id
                node_2 = s[i+1]._id
                self._elements_cable.append(LineElement(count, node_1, node_2, 3, 2, 2))
                count += 1
        sub_corner.append(list(set(sub1).intersection(set(sub2))))
        sub_corner.append(list(set(sub2).intersection(set(sub3))))
        sub_corner.append(list(set(sub3).intersection(set(sub4))))
        sub_corner.append(list(set(sub4).intersection(set(sub1))))
        for node in sub_corner:
            node_1 = node[0]._id
            node_2 = self._nodes[-1]._id
            self._elements_cable.append(LineElement(count, node_1, node_2, 4, 2, 2))
            count += 1
        #mast
        node_1 = ((self._module_number_x+1)*(self._module_number_x+1)+1)*0.5
        node_2 = self._nodes[-1]._id
        self._elements_mast.append(LineElement(1, node_1, node_2, 1, 3, 3))        

    def _GenerateSupport(self):
        sub1 = []
        sub2 = []
        sub3 = []
        sub4 = []
        sub_edge = []
        sub_corner = []
        length = self._module_number_x*self._length
        for node in self._nodes:
            if node._x == - 0.5 * length:
                sub1.append(node)
            if node._x == 0.5 * length:
                sub3.append(node)
            if node._y ==  - 0.5 * length:
                sub2.append(node)
            if node._y == 0.5 * length:
                sub4.append(node)
        sub_corner.append(list(set(sub1).intersection(set(sub2))))
        sub_corner.append(list(set(sub2).intersection(set(sub3))))
        sub_corner.append(list(set(sub3).intersection(set(sub4))))
        sub_corner.append(list(set(sub4).intersection(set(sub1))))
        for node in sub_corner:
            no = node[0]._id
            dof = True
            rdof = False
            self._constraints.append(SupportItem(1, no, dof, rdof))
        no = ((self._module_number_x+1)*(self._module_number_x+1)+1)*0.5
        si = SupportItem(1,no,dof,rdof)
        si.JustZ()
        self._constraints.append(si)
        no = self._nodes[-1]._id
        si = SupportItem(1,no,dof,rdof)
        si.JustZ()
        self._constraints.append(si)

    def _GenerateLoad(self):
        for jdx in range(0, self._module_number_x+1):
            for idx in range(0, self._module_number_x+1):
                if not (idx==0 or idx==self._module_number_x or jdx==0 or jdx==self._module_number_x):
                    no = jdx * (self._module_number_x+1) + idx + 1
                    self._loads.append(LoadItem(1, no, 0, 0, 10))

    def _WriteBegin(self, txtfile):
        #start
        txtfile.Write("/BEGIN_MST_SPECIAL_DATA/\r\n")
        #material
        txtfile.Write("/MATERIAL INFO/\r\n")
        txtfile.Write("1 6E8 1E3 1100 0.38\r\n")
        txtfile.Write("1 1.9E11 1E3 7500 0.3\r\n")
        txtfile.Write("1 2.06E11 1E3 7850 0.3\r\n")
        txtfile.Write("##\r\n")
        #section
        txtfile.Write("/SECTION PROPERTIES/\r\n")
        txtfile.Write("20 1 0.001\r\n")
        txtfile.Write("7  1 200E-6 0 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0 0\r\n")
        txtfile.Write("7  1 1.3816E-3 0 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0 0\r\n")
        txtfile.Write("##\r\n")
        #prestress
        txtfile.Write("/PRESTRESS/\r\n")
        txtfile.Write("1 1 3000000 \r\n")        #mem
        txtfile.Write("2 0 0        60000 \r\n")  #edge
        txtfile.Write("3 0 0        12000 \r\n")  #ridge
        txtfile.Write("4 0 0        16000 \r\n")  #ridge
        txtfile.Write("##\r\n")
        #solvestep
        txtfile.Write("/SOLVESTEP SETTINGS/\r\n")
        txtfile.Write("/STEP/\r\n")
        txtfile.Write("0\r\n")
        txtfile.Write("1\r\n")
        txtfile.Write("/STEP_END/\r\n")
        txtfile.Write("##\r\n")

    def _WriteNodes(self, txtfile):
        txtfile.Write("/NODECORD2/\r\n")
        for node in self._nodes:
            node.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteMemElements(self, txtfile):
        txtfile.Write("/MEM_ELEMS_7/\r\n")
        for element in self._elements_mem:
            element.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteCableElements(self, txtfile):
        txtfile.Write("/CABLE_ELEMS_7/\r\n")
        for element in self._elements_cable:
            element.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteMastElements(self, txtfile):
        txtfile.Write("/MAST_ELEMS_7/\r\n")
        for element in self._elements_mast:
            element.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteContraints(self, txtfile):
        txtfile.Write("/SUPPORT INFORMATION/\r\n")
        for support in self._constraints:
            support.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteLoads(self, txtfile):
        txtfile.Write("/DEADLOAD/\r\n")
        for load in self._loads:
            load.LogToTxt(txtfile)
        txtfile.Write("##\r\n")



class FunnelModelGenerator(ModelGeneratorBase):

    def __init__(self, length, height, r0, module_number_x, module_number_y, force):
        ModelGeneratorBase.__init__(self)
        self._length = length
        self._height = height
        self._module_number_x = module_number_x
        self._module_number_y = module_number_y
        self._r0 = r0
        self._force = force

    def _GenerateNode(self):
        count = 1
        for jdx in range(0, self._module_number_y+1):
            for idx in range(0, self._module_number_x):
                no = count
                dTheta = 360.0 / self._module_number_x
                dh = self._height / self._module_number_y
                r = self._r0 + jdx * self._length
                x = r * math.cos(math.radians(idx*dTheta))
                y = r * math.sin(math.radians(idx*dTheta))
                z = self._height - jdx * dh        
                self._nodes.append(NodeItem(no, x, y, z))
                count += 1

    def _GenerateElement(self):
        count = 1
        for jdx in range(0, self._module_number_y):
            for idx in range(0, self._module_number_x):
                if idx != self._module_number_x-1:
                    node_1 = jdx*(self._module_number_x) + idx + 1
                    node_2 = jdx*(self._module_number_x) + idx + 2
                    node_3 = (jdx+1)*(self._module_number_x) + idx + 1
                    self._elements.append(TriElement("SHELL", count, node_1, node_2, node_3, 1, 1, 1))
                    count += 1

                    node_1 = jdx*(self._module_number_x) + idx + 2
                    node_2 = (jdx+1)*(self._module_number_x) + idx + 1
                    node_3 = (jdx+1)*(self._module_number_x) + idx + 2
                    self._elements.append(TriElement("SHELL", count, node_1, node_2, node_3, 1, 1, 1))
                    count += 1
                else:
                    node_1 = jdx*(self._module_number_x) + idx + 1
                    node_2 = (jdx-1)*(self._module_number_x) + idx + 2
                    node_3 = (jdx+1)*(self._module_number_x) + idx + 1
                    self._elements.append(TriElement("SHELL", count, node_1, node_2, node_3, 1, 1, 1))
                    count += 1

                    node_1 = (jdx-1)*(self._module_number_x) + idx + 2
                    node_2 = (jdx+1)*(self._module_number_x) + idx + 1
                    node_3 = jdx*(self._module_number_x) + idx + 2
                    self._elements.append(TriElement("SHELL", count, node_1, node_2, node_3, 1, 1, 1))
                    count += 1                         

    def _GenerateSupport(self):
        for jdx in range(0, self._module_number_y+1):
            for idx in range(0, self._module_number_x):
                if jdx==0 or jdx==self._module_number_y:
                    no = jdx * (self._module_number_x) + idx + 1
                    self._constraints.append(SupportItem('BC_1', no, True, True))

    def _GenerateLoad(self):
        force_seg = self._force*self._height / self._module_number_y / 2
        for jdx in range(0, self._module_number_y+1):
            for idx in range(0, self._module_number_x):
                if idx == 0:
                    no = jdx * (self._module_number_x) + idx + 1
                    if jdx == 0 or jdx == self._module_number_y:
                        self._loads.append(LoadItem('Load_1',no,force_seg,0.0,0.0))
                    else:
                        self._loads.append(LoadItem('Load_1',no,force_seg*2,0.0,0.0))

    def _WriteBegin(self, txtfile):
        #material
        txtfile.Write("/MATERIAL/\r\n")
        txtfile.Write("Mat1 2 201E9 78.5E9 7850 0.3 350E6\r\n")
        txtfile.Write("##\r\n")
        #section
        txtfile.Write("/SECTION/\r\n")
        txtfile.Write("Sect1 5 0.002\r\n")
        txtfile.Write("##\r\n")


class ShellModelGenerator(ModelGeneratorBase):

    def __init__(self, length, height, module_number_x, module_number_y):
        ModelGeneratorBase.__init__(self)
        self._length = length
        self._height = height
        self._module_number_x = module_number_x
        self._module_number_y = module_number_y

    def _GenerateNode(self):
        count = 1
        for jdx in range(0, self._module_number_y+1):
            for idx in range(0, self._module_number_x+1):
                no = count
                x = idx * self._length - 0.5 * self._length * self._module_number_x
                y = jdx * self._length - 0.5 * self._length * self._module_number_x
                #z = - self._height * (x*x+y*y) / (length*length)
                z = - math.sqrt(self._height*self._height-(x*x+y*y))
                self._nodes.append(NodeItem(no, x, y, z))
                count += 1
                #inner grid
        for jdx in range(0, self._module_number_y):
            for idx in range(0, self._module_number_x):
                no = count
                x = idx * self._length + 0.5 * self._length - 0.5 * self._length * self._module_number_x
                y = jdx * self._length + 0.5 * self._length - 0.5 * self._length * self._module_number_x
                length = 0.5 * self._length * self._module_number_x
                #z = - self._height * (x*x+y*y) / (length*length)
                z = - math.sqrt(self._height*self._height-(x*x+y*y))
                self._nodes.append(NodeItem(no, x, y, z))
                count += 1

    def _GenerateElement(self):
        count = 1
        innerStartCount = (self._module_number_x + 1) * (self._module_number_y + 1)
        for jdx in range(0, self._module_number_y):
            for idx in range(0, self._module_number_x):
                node_1 = jdx*(self._module_number_x+1) + idx + 1
                node_2 = jdx*(self._module_number_x+1) + idx + 2
                node_3 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                self._elements.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = jdx*(self._module_number_x+1) + idx + 2
                node_2 = (jdx+1)*(self._module_number_x+1) + idx + 2
                node_3 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                self._elements.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_2 = (jdx+1)*(self._module_number_x+1) + idx + 2
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 1
                self._elements.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = jdx*(self._module_number_x+1) + idx + 1
                node_2 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 1
                self._elements.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

    def _GenerateSupport(self):
        for jdx in range(0, self._module_number_y+1):
            for idx in range(0, self._module_number_x+1):
                if (jdx==0 or jdx==self._module_number_x) or (idx==0 or idx==self._module_number_x):
                    no = jdx * (self._module_number_x+1) + idx + 1
                    self._constraints.append(SupportItem(1, no, True, False))

    def _GenerateLoad(self):
        count = 1
        for jdx in range(0, self._module_number_y+1):
            for idx in range(0, self._module_number_x+1):
                count += 1
                x = idx * self._length - 0.5 * self._length * self._module_number_x
                y = jdx * self._length - 0.5 * self._length * self._module_number_x
                if x == 0 and y == 0:
                    no = jdx * (self._module_number_x+1) + idx + 1
                    self._loads.append(LoadItem(1, no, 0, 0, -4))
        for jdx in range(0, self._module_number_y):
            for idx in range(0, self._module_number_x):
                x = idx * self._length + 0.5 * self._length - 0.5 * self._length * self._module_number_x
                y = jdx * self._length + 0.5 * self._length - 0.5 * self._length * self._module_number_x
                if x == 0 and y == 0:
                    no = jdx * (self._module_number_x+1) + idx + count
                    self._loads.append(LoadItem(1, no, 0, 0, -4))

    def _WriteBegin(self, txtfile):
        #material
        txtfile.Write("/MATERIAL/\r\n")
        txtfile.Write("MAT1 1 68.95E6 26.52E6 2500 0.3\r\n")
        txtfile.Write("##\r\n")
        #section
        txtfile.Write("/SECTION/\r\n")
        txtfile.Write("SHELL 5 0.09945\r\n")
        txtfile.Write("##\r\n")


class ShellSaddleModelGenerator(object):

    _nodes = []
    _elements_cable = []
    _elements_mem = []
    _constraints = []
    _loads = []

    def __init__(self, length, height, module_number_x):
        self._length = length
        self._height = height
        self._module_number_x = module_number_x

    def GenerateModel(self):
        self._GenerateNode()
        self._GenerateMemElement()
        self._GenerateSupport()
        self._GenerateLoad()

    def WriteFile(self, filename):
        txtfile = TXTFeed(filename)
        self._WriteBegin(txtfile)
        self._WriteNodes(txtfile)
        self._WriteMemElements(txtfile)
        self._WriteContraints(txtfile)
        self._WriteLoads(txtfile)
        txtfile.Finished()

    def _GenerateNode(self):
        count = 1
        #grid
        for jdx in range(0, self._module_number_x+1):
            for idx in range(0, self._module_number_x+1):
                no = count
                x = idx * self._length - 0.5 * self._length * self._module_number_x
                y = jdx * self._length - 0.5 * self._length * self._module_number_x
                length = 0.5*self._length * self._module_number_x
                z = self._height * (1.0 - y*y/length/length)
                self._nodes.append(NodeItem(no, x, y, z))
                count += 1
        #inner grid
        for jdx in range(0, self._module_number_x):
            for idx in range(0, self._module_number_x):
                no = count
                x = idx * self._length + 0.5 * self._length - 0.5 * self._length * self._module_number_x
                y = jdx * self._length + 0.5 * self._length - 0.5 * self._length * self._module_number_x
                length = 0.5*self._length * self._module_number_x
                z = self._height * (1.0 - y*y/length/length)
                self._nodes.append(NodeItem(no, x, y, z))
                count += 1

    def _GenerateMemElement(self):
        count = 1
        innerStartCount = (self._module_number_x + 1) * (self._module_number_x + 1)
        for jdx in range(0, self._module_number_x):
            for idx in range(0, self._module_number_x):
                node_1 = jdx*(self._module_number_x+1) + idx + 1
                node_2 = jdx*(self._module_number_x+1) + idx + 2
                node_3 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = jdx*(self._module_number_x+1) + idx + 2
                node_2 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 2
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_2 = (jdx+1)*(self._module_number_x+1) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 2
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

                node_1 = jdx*(self._module_number_x+1) + idx + 1
                node_2 = innerStartCount + jdx*(self._module_number_x) + idx + 1
                node_3 = (jdx+1)*(self._module_number_x+1) + idx + 1
                self._elements_mem.append(TriElement(count, node_1, node_2, node_3, 1, 1, 1))
                count += 1

    def _GenerateSupport(self):
        for jdx in range(0, self._module_number_x+1):
            for idx in range(0, self._module_number_x+1):
                if jdx==0 or jdx==self._module_number_x:
                    no = jdx * (self._module_number_x+1) + idx + 1
                    dof = True
                    rdof = False
                    self._constraints.append(SupportItem(1, no, dof, rdof))

    def _GenerateLoad(self):
        for jdx in range(0, self._module_number_x+1):
            for idx in range(0, self._module_number_x+1):
                if abs(jdx - 0.5*self._module_number_x) <= 2:
                    no = jdx * (self._module_number_x+1) + idx + 1
                    self._loads.append(LoadItem(1, no, 0, 0, -1000000))

    def _WriteBegin(self, txtfile):
        #start
        txtfile.Write("/BEGIN_MST_SPECIAL_DATA/\r\n")
        #material
        txtfile.Write("/MATERIAL INFO/\r\n")
        txtfile.Write("4 2.06e+11 7.92e+10 7850 0.3 2.35e+008 2.06e+10 1 \r\n")
        txtfile.Write("##\r\n")
        #section
        txtfile.Write("/SECTION PROPERTIES/\r\n")
        txtfile.Write("20 1 0.1 \r\n")
        txtfile.Write("##\r\n")
        #gravity
        txtfile.Write("/GRAVITY/\r\n")
        txtfile.Write("1  0  0  -1  9.8 \r\n")
        txtfile.Write("##\r\n")
        #solvestep
        txtfile.Write("/SOLVESTEP SETTINGS/\r\n")
        txtfile.Write("/STEP/\r\n")
        txtfile.Write("1\r\n")
        txtfile.Write("1\r\n")
        txtfile.Write("/STEP_END/\r\n")
        txtfile.Write("##\r\n")

    def _WriteNodes(self, txtfile):
        txtfile.Write("/NODECORD2/\r\n")
        for node in self._nodes:
            node.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteMemElements(self, txtfile):
        txtfile.Write("/SHELL_ELEMS_7/\r\n")
        for element in self._elements_mem:
            element.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteContraints(self, txtfile):
        txtfile.Write("/SUPPORT INFORMATION/\r\n")
        for support in self._constraints:
            support.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteLoads(self, txtfile):
        txtfile.Write("/DEADLOAD/\r\n")
        for load in self._loads:
            load.LogToTxt(txtfile)
        txtfile.Write("##\r\n")