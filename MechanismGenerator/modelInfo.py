from UnitModule import *

class ModelGenerator(object):

    _nodes = []
    _elements = []
    _constraints = []
    _couples = []
    _loads = []
    _units = []

    def __init__(self, bar_length, angle, module_number, expanding_force):
        self._bar_length = bar_length
        self._angle = angle
        self._module_number = module_number
        self._expanding_force = expanding_force

    def GenerateModel(self):
        self._GenerateUnitNodes()
        self._GenerateUnitElements()
        self._GenerateUnitCouples()
        self._GenerateUnitSupports()
        self._GenerateUnitLoads()

    def WriteFile(self, filename):
        txtfile = TXTFeed(filename)
        self._WriteBegin(txtfile)
        self._WriteNodes(txtfile)
        self._WriteElements(txtfile)
        # self._WriteContraints(txtfile)
        self._WriteCouples(txtfile)
        self._WriteLoads(txtfile)
        txtfile.Finished()

    def _GenerateUnitNodes(self):
        angle = 360.0/self._module_number
        for idx in range(0, self._module_number):
            unit = DoubleGAEUnit(self._bar_length, self._angle, self._expanding_force)
            RotateUnit(unit, angle*idx-angle*0.5)
            self._units.append(unit)
        for unit in self._units:
            unit._AssignUnitList(self._units[(unit._id-2)%len(self._units)], self._units[unit._id%len(self._units)])
            self._nodes.extend(unit._UnitNodes())

    def _GenerateUnitElements(self):
        for unit in self._units:
            unit._LinkNodesIntoElement()
            self._elements.extend(unit._elements)

    def _GenerateUnitCouples(self):
        for unit in self._units:
            unit._LinkCouples()
            self._couples.extend(unit._couples)

    def _GenerateUnitSupports(self):
        for unit in self._units:
            unit._SetSupports()
            self._constraints.extend(unit._supports)

    def _GenerateUnitLoads(self):
        for unit in self._units:
            unit._SetDeadload()
            self._loads.extend(unit._loads)

    def _WriteBegin(self, txtfile):
        #start
        txtfile.Write("/BEGIN_MST_SPECIAL_DATA/\r\n")
        #material
        txtfile.Write("/MATERIAL INFO/\r\n")
        txtfile.Write("1 2.06e+008 7.92e+07 7.850 0.3 2.35e+005  2.06e+007 1 \r\n")
        txtfile.Write("##\r\n")
        #section
        txtfile.Write("/SECTION PROPERTIES/\r\n")
        txtfile.Write("1 1 60.00 3.50 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0 1\r\n")
        txtfile.Write("1 2 219.00 14.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0 1\r\n")
        txtfile.Write("##\r\n")

    def _WriteNodes(self, txtfile):
        txtfile.Write("/NODECORD2/\r\n")
        for node in self._nodes:
            node.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteElements(self, txtfile):
        txtfile.Write("/BEAM_ELEMS_7/\r\n")
        for element in self._elements:
            element.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteContraints(self, txtfile):
        txtfile.Write("/SUPPORT INFORMATION/\r\n")
        for support in self._constraints:
            support.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteCouples(self, txtfile):
        txtfile.Write("/NODALCONSTRAINTS/\r\n")
        for couple in self._couples:
            couple.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteLoads(self, txtfile):
        txtfile.Write("/DEADLOAD/\r\n")
        for load in self._loads:
            load.LogToTxt(txtfile)
        txtfile.Write("##\r\n")








