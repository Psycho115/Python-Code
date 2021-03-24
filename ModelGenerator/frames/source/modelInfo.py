class TXTFeed(object):    
    
    def __init__(self, filename):        
        self.txtfile = open(filename, "wb")

    def __del__(self):        
        if not self.txtfile.closed:
            self.txtfile.close()

    def Write(self, line):
        self.txtfile.write(line)

    def Finished(self): 
        self.txtfile.write("/END/\r\n")       
        self.txtfile.close()


class NodeItem(object):
    
    def __init__(self, no, x, y, z):
        self._id = no
        self._x = x
        self._y = y
        self._z = z

    def LogToTxt(self, txt_file):
        txt_file.Write("%d  %.10f  %.10f  %.10f  1 \r\n" % (self._id, self._x, self._y, self._z))

class ElementItem(object):

    def __init__(self, no, node_1, node_2, section_no):
        self._id = no
        self._node_1 = node_1
        self._node_2 = node_2
        self._section = section_no

    def LogToTxt(self, txt_file):
        txt_file.Write("%d  %d  %d  %d  1  %d  1 \r\n" % (self._id, self._id, self._node_1, self._node_2, self._section))

class SupportItem(object):

    def __init__(self, node, dof, rdof):
        self._node = node
        self._dof = dof
        self._rdof = rdof

    def LogToTxt(self, txt_file):
        if self._dof == True:
            dof_w = "2  2  2"
        else:
            dof_w = "0  0  0"
        if self._rdof == True:
            rdof_w = "2  2  2"
        else:
            rdof_w = "0  0  0"

        txt_file.Write("FixedSet %d  %s  %s \r\n" % (self._node, dof_w, rdof_w))
        

class ModelGenerator(object):

    _nodes = []
    _elements = []
    _constraints = []

    def __init__(self, length, height, module_number_x, module_number_y, module_number_z):
        self._length = length
        self._height = height
        self._module_number_x = module_number_x
        self._module_number_y = module_number_y
        self._module_number_z = module_number_z

    def GenerateModel(self):
        self._GenerateNode()
        self._GenerateElement()
        self._GenerateSupport()

    def WriteFile(self, filename):
        txtfile = TXTFeed(filename)
        self._WriteBegin(txtfile)
        self._WriteNodes(txtfile)
        self._WriteElements(txtfile)
        self._WriteContraints(txtfile)
        txtfile.Finished()

    def _GenerateNode(self):
        count = 1
        for zdx in range(0, self._module_number_z+1):
           for jdx in range(0, self._module_number_y+1):
               for idx in range(0, self._module_number_x+1):
                    no = count
                    x = idx * self._length
                    y = jdx * self._length
                    z = zdx * self._height
                    self._nodes.append(NodeItem(no, x, y, z))
                    count += 1

    def _GenerateElement(self):
        count = 1
        for zdx in range(0, self._module_number_z):
            for jdx in range(0, self._module_number_y+1):
                for idx in range(0, self._module_number_x):
                    start_index_z = (zdx+1)*(self._module_number_x+1)*(self._module_number_y+1)
                    node_1 = start_index_z + jdx*(self._module_number_x+1) + idx + 1
                    node_2 = start_index_z + jdx*(self._module_number_x+1) + idx + 2
                    self._elements.append(ElementItem(count, node_1, node_2, 1))
                    count += 1
            for idx in range(0, self._module_number_x+1):
                for jdx in range(1, self._module_number_y+1):
                    start_index_z = (zdx+1)*(self._module_number_x+1)*(self._module_number_y+1)
                    node_1 = start_index_z + (jdx-1) * (self._module_number_x+1) + idx + 1
                    node_2 = start_index_z + jdx * (self._module_number_x+1) + idx + 1
                    self._elements.append(ElementItem(count, node_1, node_2, 1))
                    count += 1
            for jdx in range(0, self._module_number_y+1):
                for idx in range(0, self._module_number_x+1):
                    planer_count = (self._module_number_x+1)*(self._module_number_y+1)
                    node_1 = planer_count*zdx + jdx*(self._module_number_x+1) + idx + 1
                    node_2 = planer_count*(zdx+1) + jdx*(self._module_number_x+1) + idx + 1
                    self._elements.append(ElementItem(count, node_1, node_2, 2))
                    count += 1

    def _GenerateSupport(self):
        count = 1
        for jdx in range(0, self._module_number_y+1):
            for idx in range(0, self._module_number_x+1):
                no = count
                dof = True
                rdof = True
                self._constraints.append(SupportItem(count, dof, rdof))
                count += 1

    def _WriteBegin(self, txtfile):
        txtfile.Write("/MATERIAL/\r\n")
        txtfile.Write("1, Mat-Soil, TYPE, DP\r\n")
        txtfile.Write("1, Mat-Soil, DENS, 2000\r\n")   
        txtfile.Write("1, Mat-Soil, EM, 1E8\r\n")
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

        

    def _WriteNodes(self, txtfile):
        txtfile.Write("/NODE/\r\n")
        for node in self._nodes:
            node.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteElements(self, txtfile):
        txtfile.Write("/BEAM_ELEM/\r\n")
        for element in self._elements:
            element.LogToTxt(txtfile)
        txtfile.Write("##\r\n")

    def _WriteContraints(self, txtfile):
        txtfile.Write("/CONSTRAINT/\r\n")
        for support in self._constraints:
            support.LogToTxt(txtfile)
        txtfile.Write("##\r\n")




