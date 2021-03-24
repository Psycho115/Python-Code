from UtilityBase import FPMFeed, NodeItem, ElementBaseItem, SupportItem, LoadItem

class TriElement(ElementBaseItem):

    def __init__(self, elem_type, no, node_1, node_2, node_3, real_no, section_no, mat_no):
        ElementBaseItem.__init__(self, elem_type, no, real_no, section_no, mat_no)
        self._node_1 = node_1
        self._node_2 = node_2
        self._node_3 = node_3

    def GetNodeStr(self):
        self._node_str = "%d, %d, %d" % (self._node_1, self._node_2, self._node_3)

class LineElement(ElementBaseItem):

    def __init__(self, elem_type, no, node_1, node_2, real_no, section_no, mat_no):
        ElementBaseItem.__init__(self, elem_type, no, real_no, section_no, mat_no)
        self._node_1 = node_1
        self._node_2 = node_2

    def GetNodeStr(self):
        self._node_str = "%d, %d" % (self._node_1, self._node_2)

class TetraElement(ElementBaseItem):

    def __init__(self, elem_type, no, node_1, node_2, node_3, node_4, real_no, section_no, mat_no):
        ElementBaseItem.__init__(self, elem_type, no, real_no, section_no, mat_no)
        self._node_1 = node_1
        self._node_2 = node_2
        self._node_3 = node_3
        self._node_4 = node_4

    def GetNodeStr(self):
        self._node_str = "%d, %d, %d, %d" % (self._node_1, self._node_2, self._node_3, self._node_4)

class ModelGeneratorBase(object):

    _nodes = []
    _elements = []
    _constraints = []
    _couples = []
    _loads = []
    _disp = []
    _nodegroup = {}

    def __init__(self):
        pass
        
    def GenerateModel(self):
        self._GenerateNode()
        self._GenerateAddtionalNode()
        self._GenerateElement()
        self._GenerateAddtionalElement()
        self._GenerateSupport()
        self._GenerateLoad()
        self._GenerateCouple()

    def WriteFile(self, filename):
        txtfile = FPMFeed(filename)
        self._WriteBegin(txtfile)
        self._WriteNodes(txtfile)
        self._WriteElements(txtfile)
        self._WriteContraints(txtfile)
        self._WriteLoads(txtfile)
        # self._WriteCouples(txtfile)
        # self._WriteOthers(txtfile)
        txtfile.Finished()

    def _GenerateNode(self):
        pass

    def _GenerateElement(self):
        pass                     

    def _GenerateSupport(self):
        pass

    def _GenerateLoad(self):
        pass

    def _GenerateAddtionalNode(self):
        pass

    def _GenerateAddtionalElement(self):
        pass

    def _GenerateCouple(self):
        pass

    def _WriteBegin(self, txtfile):
        pass

    def _WriteNodes(self, txtfile):
        txtfile.Write("/NODE/\r\n")
        for node in self._nodes:
            node.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteElements(self, txtfile):
        txtfile.Write("/ELEM/\r\n")
        for element in self._elements:
            element.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteContraints(self, txtfile):
        txtfile.Write("/CONSTRAINT/\r\n")
        for support in self._constraints:
            support.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteLoads(self, txtfile):
        txtfile.Write("/LOAD/\r\n")
        txtfile.Write("GRAVITY_SET, GRAVITY, 0.0, 0.0, 1.0, 9.8\r\n")
        for load in self._loads:
            load.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteCouples(self, txtfile):
        txtfile.Write("/DOFCOUPLE/\r\n")
        for couple in self._couples:
            couple.LogToTxt(txtfile)
        txtfile.Write("##\r\n")