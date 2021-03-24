from utility.UtilityBase import FPMFeed, NodeItem, ElementBaseItem, FixedItem, SpdpKItem, SpdpCItem, NodeSetItem, ElemSetItem, LoadItem, CoupleItem
from utility.ModelGeneratorBase import PointElement, LineElement, TriElement, TetraElement, ModelGeneratorBase
import math
from random import randint

class StructureSoilFoundationModelGenerator(ModelGeneratorBase):

    foundation_length_module = 12
    foundation_height_module = 6

    bottom_elems = []
    hole_elems = []

    kn = 2346e6
    kt = 1173e6
    ct = 26e6
    cn = 15e6

    height = [10, 9, 8, 5, 5, 7, 5, 7, 9, 6, 5, 9, 10, 5, 6, 7, 7, 8, 6, 9, 9, 5, 10, 7, 8, 7, 6, 8, 7, 8, 7, 10, 10, 5, 9, 6, 10, 9, 6, 7, 10, 9, 7, 7, 8, 6, 5, 8, 7, 6, 6, 6, 7, 8, 6, 8, 10, 9, 8, 9, 9, 10, 7, 10]

    nodeset_soil_left = NodeSetItem("soil_left")
    nodeset_soil_right = NodeSetItem("soil_right")
    nodeset_soil_top = NodeSetItem("soil_top")
    nodeset_foundation_left = NodeSetItem("foundation_left")
    nodeset_foundation_right = NodeSetItem("foundation_right")
    nodeset_foundation_bottom = NodeSetItem("foundation_bottom")

    nodeset_x = NodeSetItem("x")
    nodeset_y = NodeSetItem("y")
    nodeset_z = NodeSetItem("z")
    nodeset_xy = NodeSetItem("xy")

    nodeset_x_con = NodeSetItem("x_con")
    nodeset_y_con = NodeSetItem("y_con")
    nodeset_xy_con = NodeSetItem("xy_con")
    nodeset_disp = NodeSetItem("disp")

    elemset_side_target = ElemSetItem("side_target")
    elemset_bottom_target = ElemSetItem("bottom_target")

    def __init__(self):
        ModelGeneratorBase.__init__(self)
        self.node_count_accumulated = 0
        self.elem_count_accumulated = 0

########################################################
## Soil

    def _InitSoil(self, xsize, ysize, zsize, module_x, module_y, module_z, module_count_x, module_count_y, space):
        ModelGeneratorBase.__init__(self)
        self._module_count_x = module_count_x
        self._module_count_y = module_count_y
        self._soil_size_x = xsize * module_count_x
        self._soil_size_y = ysize * module_count_y
        self._soil_size_z = zsize
        self._soil_module_x = module_x * module_count_x
        self._soil_module_y = module_y * module_count_y
        self._soil_module_z = module_z
        self._building_space = space

    def _LogNodeCount(self):
        if len(self._nodes) != 0:
            self.node_count_accumulated = self._nodes[-1]._id
        else:
            self.node_count_accumulated = 0

    def _LogElementCount(self):
        if len(self._elements) != 0:
            self.elem_count_accumulated = self._elements[-1]._id
        else:
            self.elem_count_accumulated = 0

    def _GenerateSoilNode_Soil(self):
        count = self.node_count_accumulated + 1
        dx = self._soil_size_x/self._soil_module_x
        dy = self._soil_size_y/self._soil_module_y
        dz = self._soil_size_z/self._soil_module_z
        for kdx in range(0, self._soil_module_z+1):
            for jdx in range(0, self._soil_module_y+1):
                for idx in range(0, self._soil_module_x+1):
                    no = count
                    x = idx * dx - 0.5 * self._soil_size_x
                    y = jdx * dy - 0.5 * self._soil_size_y
                    z = - kdx * dz
                    node_item = NodeItem(no, x, y, z)

                    if x == -0.5*dx*self.foundation_length_module and z >= -dz*self.foundation_height_module:
                        self.nodeset_soil_left.AddNode(node_item)
                    if x == 0.5*dx*self.foundation_length_module and z >= -dz*self.foundation_height_module:
                        self.nodeset_soil_right.AddNode(node_item)
                    if z == -dz*self.foundation_height_module and x >= -0.5*dx*self.foundation_length_module and x <= 0.5*dx*self.foundation_length_module:
                        self.nodeset_soil_top.AddNode(node_item)

                    self._nodes.append(node_item)
                    count += 1

        # for kdx in range(0, self._soil_module_z+1):
        #     for jdx in range(0, self._soil_module_y+1):
        #         for idx in range(0, self._soil_module_x+1):
        #             no = count
        #             x = idx * dx - 0.5 * self._soil_size_x
        #             y = jdx * dy - 0.5 * self._soil_size_y
        #             z = - kdx * dz
        #             node_item = NodeItem(no, x, y, z)

        #             if idx == self._soil_module_x or idx == 0:
        #                 if jdx != self._soil_module_y and jdx != 0:
        #                     self.nodeset_x_con.AddNode(node_item)
        #                     self.nodeset_disp.AddNode(node_item)
        #                     self._nodes.append(node_item)
        #                     count += 1
        #             if (idx == self._soil_module_x or idx == 0) and (jdx == self._soil_module_y or jdx == 0):
        #                 self.nodeset_xy_con.AddNode(node_item)
        #                 self.nodeset_disp.AddNode(node_item)
        #                 self._nodes.append(node_item)
        #                 count += 1

    def _GenerateSoilElement_Soil(self):
        count = self.elem_count_accumulated + 1
        for kdx in range(0, self._soil_module_z):
            for jdx in range(0, self._soil_module_y):
                for idx in range(0, self._soil_module_x):
                    if idx >= 0.5*(self._soil_module_x-self.foundation_length_module):
                        if idx <= 0.5*(self._soil_module_x+self.foundation_height_module)+2:
                            if kdx < self.foundation_height_module:
                                continue

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

                    for elem in elems:
                        self._elements.append(elem)

        # for idx in range(0, self.nodeset_x_con.Size()):
        #     node_1 = self.nodeset_x_con.GetNode(idx)
        #     node_2 = self.nodeset_x.GetNode(idx)
        #     self._elements.append(LineElement("COMBIN", count, node_1, node_2, 1, 0, 0))
        #     count += 1
        # for idx in range(0, self.nodeset_xy_con.Size()):
        #     node_1 = self.nodeset_xy_con.GetNode(idx)
        #     node_2 = self.nodeset_xy.GetNode(idx)
        #     self._elements.append(LineElement("COMBIN", count, node_1, node_2, 3, 0, 0))
        #     count += 1
        # for idx in range(0, self.nodeset_disp.Size()):
        #     node_1 = self.nodeset_disp.GetNode(idx)
        #     self._elements.append(PointElement("MASS", count, node_1, 4, 0, 0))
        #     count += 1

    def _ClearSoilNode_Soil(self):
        dx = self._soil_size_x/self._soil_module_x
        dy = self._soil_size_y/self._soil_module_y
        dz = self._soil_size_z/self._soil_module_z
        funca = lambda node: (node._x <= -0.5*dx*self.foundation_length_module or node._x >= 0.5*dx*self.foundation_length_module) or node._z <= -dz*self.foundation_height_module
        self._nodes = filter(funca, self._nodes)

    def _GenerateSoilInterface(self):
        count = self.elem_count_accumulated + 1

        # left
        for jdx in range(0, self.foundation_height_module):
            for idx in range(0, self._soil_module_y):
                node_1 = self.nodeset_soil_left.GetNode(jdx*(self._soil_module_y+1) + idx)
                node_2 = self.nodeset_soil_left.GetNode(jdx*(self._soil_module_y+1) + idx + 1)
                node_3 = self.nodeset_soil_left.GetNode((jdx+1)*(self._soil_module_y+1) + idx)
                elem = TriElement("CONTACT", count, node_1._id, node_3._id, node_2._id, 5, 0, 0)
                self._elements.append(elem)
                self.elemset_side_target.AddElem(elem)
                count += 1

                node_1 = self.nodeset_soil_left.GetNode(jdx*(self._soil_module_y+1) + idx + 1)
                node_2 = self.nodeset_soil_left.GetNode((jdx+1)*(self._soil_module_y+1) + idx)
                node_3 = self.nodeset_soil_left.GetNode((jdx+1)*(self._soil_module_y+1) + idx + 1)
                elem = TriElement("CONTACT", count, node_1._id, node_2._id, node_3._id, 5, 0, 0)
                self._elements.append(elem)
                self.elemset_side_target.AddElem(elem)
                count += 1

        # right
        for jdx in range(0, self.foundation_height_module):
            for idx in range(0, self._soil_module_y):
                node_1 = self.nodeset_soil_right.GetNode(jdx*(self._soil_module_y+1) + idx)
                node_2 = self.nodeset_soil_right.GetNode(jdx*(self._soil_module_y+1) + idx + 1)
                node_3 = self.nodeset_soil_right.GetNode((jdx+1)*(self._soil_module_y+1) + idx)
                elem = TriElement("CONTACT", count, node_1._id, node_2._id, node_3._id, 5, 0, 0)
                self._elements.append(elem)
                self.elemset_side_target.AddElem(elem)
                count += 1

                node_1 = self.nodeset_soil_right.GetNode(jdx*(self._soil_module_y+1) + idx + 1)
                node_2 = self.nodeset_soil_right.GetNode((jdx+1)*(self._soil_module_y+1) + idx)
                node_3 = self.nodeset_soil_right.GetNode((jdx+1)*(self._soil_module_y+1) + idx + 1)
                elem = TriElement("CONTACT", count, node_1._id, node_3._id, node_2._id, 5, 0, 0)
                self._elements.append(elem)
                self.elemset_side_target.AddElem(elem)
                count += 1

        # top
        for jdx in range(0, self._soil_module_y):
            for idx in range(0, self.foundation_length_module):
                node_1 = self.nodeset_soil_top.GetNode(jdx*(self.foundation_length_module+1) + idx)
                node_2 = self.nodeset_soil_top.GetNode(jdx*(self.foundation_length_module+1) + idx + 1)
                node_3 = self.nodeset_soil_top.GetNode((jdx+1)*(self.foundation_length_module+1) + idx)
                elem = TriElement("CONTACT", count, node_1._id, node_2._id, node_3._id, 6, 0, 0)
                self._elements.append(elem)
                self.elemset_bottom_target.AddElem(elem)
                count += 1

                node_1 = self.nodeset_soil_top.GetNode(jdx*(self.foundation_length_module+1) + idx + 1)
                node_2 = self.nodeset_soil_top.GetNode((jdx+1)*(self.foundation_length_module+1) + idx)
                node_3 = self.nodeset_soil_top.GetNode((jdx+1)*(self.foundation_length_module+1) + idx + 1)
                elem = TriElement("CONTACT", count, node_1._id, node_3._id, node_2._id, 6, 0, 0)
                self._elements.append(elem)
                self.elemset_bottom_target.AddElem(elem)
                count += 1

    def _GenerateSoilNode_Foundation(self):
        count = self.node_count_accumulated + 1
        soiltop = []
        dx = self._soil_size_x/self._soil_module_x
        dy = self._soil_size_y/self._soil_module_y
        dz = self._soil_size_z/self._soil_module_z
        for kdx in range(0, self.foundation_height_module+1):
            for jdx in range(0, self._soil_module_y+1):
                for idx in range(0, self.foundation_length_module+1):
                    no = count
                    x = idx * dx - 0.5 * self.foundation_length_module*dx
                    y = jdx * dy - 0.5 * self._soil_size_y
                    z = - kdx * dz
                    node_item = NodeItem(no, x, y, z)

                    if kdx == 0:
                        soiltop.append(node_item)

                    if x == -0.5*dx*self.foundation_length_module and z >= -dz*self.foundation_height_module:
                        self.nodeset_foundation_left.AddNode(node_item)
                    if x == 0.5*dx*self.foundation_length_module and z >= -dz*self.foundation_height_module:
                        self.nodeset_foundation_right.AddNode(node_item)
                    if z == -dz*self.foundation_height_module and x >= -0.5*dx*self.foundation_length_module and x <= 0.5*dx*self.foundation_length_module:
                        self.nodeset_foundation_bottom.AddNode(node_item)

                    self._nodes.append(node_item)
                    count += 1

        self._nodegroup['soiltop'] = soiltop

    def _GenerateSoilElement_Foundation(self):
        count = self.elem_count_accumulated + 1
        for kdx in range(0, self.foundation_height_module):
            for jdx in range(0, self._soil_module_y):
                for idx in range(0, self.foundation_length_module):
                    node_1 = self.node_count_accumulated + kdx*(self.foundation_length_module+1)*(self._soil_module_y+1) + jdx*(self.foundation_length_module+1) + (idx+1)
                    node_2 = self.node_count_accumulated + kdx*(self.foundation_length_module+1)*(self._soil_module_y+1) + jdx*(self.foundation_length_module+1) + (idx+2)
                    node_3 = self.node_count_accumulated + kdx*(self.foundation_length_module+1)*(self._soil_module_y+1) + (jdx+1)*(self.foundation_length_module+1) + (idx+1)
                    node_4 = self.node_count_accumulated + kdx*(self.foundation_length_module+1)*(self._soil_module_y+1) + (jdx+1)*(self.foundation_length_module+1) + (idx+2)
                    node_5 = self.node_count_accumulated + (kdx+1)*(self.foundation_length_module+1)*(self._soil_module_y+1) + jdx*(self.foundation_length_module+1) + (idx+1)
                    node_6 = self.node_count_accumulated + (kdx+1)*(self.foundation_length_module+1)*(self._soil_module_y+1) + jdx*(self.foundation_length_module+1) + (idx+2)
                    node_7 = self.node_count_accumulated + (kdx+1)*(self.foundation_length_module+1)*(self._soil_module_y+1) + (jdx+1)*(self.foundation_length_module+1) + (idx+1)
                    node_8 = self.node_count_accumulated + (kdx+1)*(self.foundation_length_module+1)*(self._soil_module_y+1) + (jdx+1)*(self.foundation_length_module+1) + (idx+2)
                    elems = []
                    if (idx%2+jdx%2+kdx%2)%2==1:
                        elems.append(TetraElement("SOLID", count, node_1, node_3, node_2, node_5, 0, 0, 3))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_2, node_3, node_4, node_8, 0, 0, 3))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_2, node_3, node_8, node_5, 0, 0, 3))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_2, node_6, node_5, node_8, 0, 0, 3))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_3, node_7, node_8, node_5, 0, 0, 3))
                        count += 1
                    else:
                        elems.append(TetraElement("SOLID", count, node_1, node_3, node_4, node_7, 0, 0, 3))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_4, node_7, node_8, node_6, 0, 0, 3))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_1, node_4, node_2, node_6, 0, 0, 3))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_1, node_6, node_5, node_7, 0, 0, 3))
                        count += 1
                        elems.append(TetraElement("SOLID", count, node_1, node_7, node_4, node_6, 0, 0, 3))
                        count += 1 

                    for elem in elems:
                        self._elements.append(elem)

    def _GenerateSoilInterface_Foundation(self):
        count = self.elem_count_accumulated + 1

        # left
        for jdx in range(0, self.foundation_height_module):
            for idx in range(0, self._soil_module_y):
                node_1 = self.nodeset_foundation_left.GetNode(jdx*(self._soil_module_y+1) + idx)
                node_2 = self.nodeset_foundation_left.GetNode(jdx*(self._soil_module_y+1) + idx + 1)
                node_3 = self.nodeset_foundation_left.GetNode((jdx+1)*(self._soil_module_y+1) + idx)
                elem = TriElement("CONTACT", count, node_1._id, node_2._id, node_3._id, 5, 0, 0)
                self._elements.append(elem)
                count += 1

                node_1 = self.nodeset_foundation_left.GetNode(jdx*(self._soil_module_y+1) + idx + 1)
                node_2 = self.nodeset_foundation_left.GetNode((jdx+1)*(self._soil_module_y+1) + idx)
                node_3 = self.nodeset_foundation_left.GetNode((jdx+1)*(self._soil_module_y+1) + idx + 1)
                elem = TriElement("CONTACT", count, node_1._id, node_3._id, node_2._id, 5, 0, 0)
                self._elements.append(elem)
                count += 1

        # right
        for jdx in range(0, self.foundation_height_module):
            for idx in range(0, self._soil_module_y):
                node_1 = self.nodeset_foundation_right.GetNode(jdx*(self._soil_module_y+1) + idx)
                node_2 = self.nodeset_foundation_right.GetNode(jdx*(self._soil_module_y+1) + idx + 1)
                node_3 = self.nodeset_foundation_right.GetNode((jdx+1)*(self._soil_module_y+1) + idx)
                elem = TriElement("CONTACT", count, node_1._id, node_3._id, node_2._id, 5, 0, 0)
                self._elements.append(elem)
                count += 1

                node_1 = self.nodeset_foundation_right.GetNode(jdx*(self._soil_module_y+1) + idx + 1)
                node_2 = self.nodeset_foundation_right.GetNode((jdx+1)*(self._soil_module_y+1) + idx)
                node_3 = self.nodeset_foundation_right.GetNode((jdx+1)*(self._soil_module_y+1) + idx + 1)
                elem = TriElement("CONTACT", count, node_1._id, node_2._id, node_3._id, 5, 0, 0)
                self._elements.append(elem)
                count += 1

        # top
        for jdx in range(0, self._soil_module_y):
            for idx in range(0, self.foundation_length_module):
                node_1 = self.nodeset_foundation_bottom.GetNode(jdx*(self.foundation_length_module+1) + idx)
                node_2 = self.nodeset_foundation_bottom.GetNode(jdx*(self.foundation_length_module+1) + idx + 1)
                node_3 = self.nodeset_foundation_bottom.GetNode((jdx+1)*(self.foundation_length_module+1) + idx)
                elem = TriElement("CONTACT", count, node_1._id, node_3._id, node_2._id, 6, 0, 0)
                self._elements.append(elem)
                count += 1

                node_1 = self.nodeset_foundation_bottom.GetNode(jdx*(self.foundation_length_module+1) + idx + 1)
                node_2 = self.nodeset_foundation_bottom.GetNode((jdx+1)*(self.foundation_length_module+1) + idx)
                node_3 = self.nodeset_foundation_bottom.GetNode((jdx+1)*(self.foundation_length_module+1) + idx + 1)
                elem = TriElement("CONTACT", count, node_1._id, node_2._id, node_3._id, 6, 0, 0)
                self._elements.append(elem)
                count += 1

    def _GenerateSoilSupport(self):
        count = self.node_count_accumulated+1
        dx = self._soil_size_x/self._soil_module_x
        dy = self._soil_size_y/self._soil_module_y
        dz = self._soil_size_z/self._soil_module_z
        for kdx in range(0, self._soil_module_z+1):
            for jdx in range(0, self._soil_module_y+1):
                for idx in range(0, self._soil_module_x+1):
                    no = count
                    x = idx * dx - 0.5 * self._soil_size_x
                    y = jdx * dy - 0.5 * self._soil_size_y
                    z = - kdx * dz
                    node_item = NodeItem(no, x, y, z)

                    if idx == self._soil_module_x or idx == 0:
                        if jdx != self._soil_module_y and jdx != 0:
                            self.nodeset_x_con.AddNode(node_item)
                            self.nodeset_disp.AddNode(node_item)
                            self._nodes.append(node_item)
                            count += 1

        for node in self._nodes:
            if node._x == -0.5*self._soil_size_x or node._x == 0.5*self._soil_size_x:
                if node._y != -0.5*self._soil_size_y and node._y != 0.5*self._soil_size_y:
                    self.nodeset_x.AddNode(node)
            if node._y == -0.5*self._soil_size_y or node._y == 0.5*self._soil_size_y:
                if node._x != -0.5*self._soil_size_x and node._x != 0.5*self._soil_size_x:
                    self.nodeset_y.AddNode(node)
            if node._z == -self._soil_size_z:
                self.nodeset_z.AddNode(node)
                self.nodeset_disp.AddNode(node)
            if (node._x == -0.5*self._soil_size_x or node._x == 0.5*self._soil_size_x) and (node._y == -0.5*self._soil_size_y or node._y == 0.5*self._soil_size_y):
                self.nodeset_xy.AddNode(node)

        count = self.elem_count_accumulated+1
        for idx in range(0, self.nodeset_x_con.Size()):
            node_1 = self.nodeset_x_con.GetNode(idx)
            node_2 = self.nodeset_x.GetNode(idx)
            self._elements.append(LineElement("COMBIN", count, node_1._id, node_2._id, 1, 0, 0))
            count += 1
        for idx in range(0, self.nodeset_disp.Size()):
            node_1 = self.nodeset_disp.GetNode(idx)
            self._elements.append(PointElement("MASS", count, node_1._id, 4, 0, 0))
            count += 1

        # self._constraints.append(FixedItem("bc_x", self.nodeset_x, [1]))
        self._constraints.append(FixedItem("bc_y", self.nodeset_y, [2]))
        self._constraints.append(FixedItem("bc_y", self.nodeset_xy, [2]))
        self._constraints.append(FixedItem("bc_z", self.nodeset_z, [3]))
        self._constraints.append(FixedItem("bc_xy", self.nodeset_xy, [1, 2]))
        self._constraints.append(FixedItem("bc_wall_fixall", self.nodeset_disp, [1, 2, 3]))
        self._constraints.append(FixedItem("bc_wall_fixz", self.nodeset_disp, [3]))

    def _GenerateSoilLoad(self):
        pass

    def _GenerateSoilModel(self):
        self._GenerateSoilNode_Soil()
        self._GenerateSoilElement_Soil()

        self._LogNodeCount()
        self._LogElementCount()

        self._GenerateSoilInterface()

        self._ClearSoilNode_Soil()

        self._LogNodeCount()
        self._LogElementCount()

        self._GenerateSoilNode_Foundation()
        self._GenerateSoilElement_Foundation()

        self._LogNodeCount()
        self._LogElementCount()

        self._GenerateSoilInterface_Foundation()

        self._LogNodeCount()
        self._LogElementCount()

        self._GenerateSoilSupport()
        # self._GenerateSoilLoad()

####################################################################
## Struct

    module_z = {}

    def _InitStructure(self, zsize, module_z):
        ModelGeneratorBase.__init__(self)
        self._struct_size_x = 4 * 4
        self._struct_size_y = 4 * 4
        self._struct_size_z = zsize
        self._struct_module_x = 4
        self._struct_module_y = 4
        self._struct_module_z = module_z
        for xm in range(0, self._module_count_x):
            for ym in range(0, self._module_count_y):
                z = self.height[xm*self._module_count_x+ym]
                self.module_z[(xm,ym)] = z
        print(self.module_z)

    def _GenerateStructNode(self, xm, ym):
        dx = self._struct_size_x/self._struct_module_x
        dy = self._struct_size_y/self._struct_module_y
        dz = self._struct_size_z/self._struct_module_z
        count = self.node_count_accumulated + 1
        for zdx in range(0, self.module_z[(xm,ym)]+1):
            for jdx in range(0, self._struct_module_y+1):
                for idx in range(0, self._struct_module_x+1):
                    no = count
                    x = idx * dx - 0.5 * self._struct_size_x
                    y = jdx * dy - 0.5 * self._struct_size_y
                    x = x - 0.5 * (self._module_count_x - 1) * self._building_space
                    y = y - 0.5 * (self._module_count_y - 1) * self._building_space
                    x = x + xm * self._building_space
                    y = y + ym * self._building_space
                    z = zdx * dz
                    nodeItem = NodeItem(no, x, y, z)
                    if zdx==0:
                        self._nodegroup['structbase'].append(nodeItem)
                    self._nodes.append(nodeItem)
                    count += 1

    def _GenerateStructElement(self, xm, ym):
        count = self.elem_count_accumulated + 1
        real = self._GetReal(xm, ym)
        for zdx in range(0, self.module_z[(xm,ym)]):
            for jdx in range(0, self._struct_module_y+1):
                for idx in range(0, self._struct_module_x):
                    start_index_z = (zdx+1)*(self._struct_module_x+1)*(self._struct_module_y+1) + self.node_count_accumulated
                    node_1 = start_index_z + jdx*(self._struct_module_x+1) + idx + 1
                    node_2 = start_index_z + jdx*(self._struct_module_x+1) + idx + 2
                    self._elements.append(LineElement("BEAM", count, node_1, node_2, real, 1, 2))
                    count += 1
            for idx in range(0, self._struct_module_x+1):
                for jdx in range(1, self._struct_module_y+1):
                    start_index_z = (zdx+1)*(self._struct_module_x+1)*(self._struct_module_y+1) + self.node_count_accumulated
                    node_1 = start_index_z + (jdx-1) * (self._struct_module_x+1) + idx + 1
                    node_2 = start_index_z + jdx * (self._struct_module_x+1) + idx + 1
                    self._elements.append(LineElement("BEAM", count, node_1, node_2, real, 1, 2))
                    count += 1
            for jdx in range(0, self._struct_module_y+1):
                for idx in range(0, self._struct_module_x+1):
                    planer_count = (self._struct_module_x+1)*(self._struct_module_y+1)
                    node_1 = self.node_count_accumulated + planer_count*zdx + jdx*(self._struct_module_x+1) + idx + 1
                    node_2 = self.node_count_accumulated + planer_count*(zdx+1) + jdx*(self._struct_module_x+1) + idx + 1
                    colume = LineElement("BEAM", count, node_1, node_2, real, 2, 2)
                    self._elements.append(colume)
                    if zdx == 0:
                        self.bottom_elems.append(colume)
                    count += 1

    def _GetReal(self, xm, ym):
        if xm == 2 and ym == 2:
            return 1
        elif xm == 2 and ym == 0:
            return 3
        elif xm == 0 and ym == 2:
            return 2
        else:
            return 0

    def _GenerateStructSupport(self):
        pass

    def _GenerateStructLoad(self):
        pass

    def _GenerateStructModel(self):
        self._nodegroup['structbase'] = []
        for xm in range(0,self._module_count_x):
            for ym in range(0,self._module_count_y):
                self._GenerateStructNode(xm, ym)
                self._GenerateStructElement(xm, ym)
                self._LogNodeCount()
                self._LogElementCount()
        #self._GenerateStructSupport()
        #self._GenerateStructLoad()

####################################################################
## Couple

    def _AdjustNode(self):
        for elem in self.bottom_elems:
            old_id = elem._node_1
            new_id = 0
            oldNode = NodeItem(0, 0, 0, 0)
            if (self._nodegroup.has_key('structbase')):
                for node in self._nodegroup['structbase']:
                    if node._id == old_id:
                        oldNode = node
                        break
            if (self._nodegroup.has_key('soiltop')):
                for node in self._nodegroup['soiltop']:
                    if node._x == oldNode._x and node._y == oldNode._y:
                        new_id = node._id
                        elem._node_1 = new_id
                        self._nodes.remove(oldNode)
                        break

####################################################################
## Load

    def _InitSoilLoad(self,pressure,bodyLoad):
        self._pressure = pressure
        self._body_load = bodyLoad

####################################################################
## Control

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
        txtfile.Write("3, Mat-Foundation, TYPE, LE\r\n")
        txtfile.Write("3, Mat-Foundation, DENS, 2500\r\n")
        txtfile.Write("3, Mat-Foundation, EM, 32500E6\r\n")
        txtfile.Write("3, Mat-Foundation, NU, 0.25\r\n")
        txtfile.Write("##\r\n")
        txtfile.Write("/SECTION/\r\n")
        txtfile.Write("1, Rect_Beam, TYPE, RECT\r\n")
        txtfile.Write("1, Rect_Beam, SHAPE, 0.2, 0.4\r\n")
        txtfile.Write("2, Round_Colume, TYPE, ROUND\r\n")
        txtfile.Write("2, Round_Colume, SHAPE, 0.8\r\n")
        txtfile.Write("##\r\n")
        txtfile.Write("/REAL_CONSTANT/\r\n")
        txtfile.Write("1, combinx, TYPE, SPRG\r\n")
        txtfile.Write("1, combinx, K, %f, %f, %f\r\n" % (self.kn, self.kt, 0.0))
        txtfile.Write("1, combinx, C, %f, %f, %f\r\n" % (self.cn, self.ct, 0.0))
        txtfile.Write("2, combiny, TYPE, SPRG\r\n")
        txtfile.Write("2, combiny, K, %f, %f, %f\r\n" % (self.kn, self.kt, 0.0))
        txtfile.Write("2, combiny, C, %f, %f, %f\r\n" % (self.cn, self.ct, 0.0))
        txtfile.Write("3, combinxy, TYPE, SPRG\r\n")
        txtfile.Write("3, combinxy, K, %f, %f, %f\r\n" % (self.kn, self.kn, 0.0))
        txtfile.Write("3, combinxy, C, %f, %f, %f\r\n" % (self.cn, self.cn, 0.0))
        txtfile.Write("4, mass, TYPE, INER\r\n")
        txtfile.Write("4, mass, MASS, %f, %f, %f\r\n" % (1.0, 1.0, 1.0))
        txtfile.Write("5, contact_side, TYPE, INTF\r\n")
        txtfile.Write("5, contact_side, CELL, 1, 0.1, 0.5\r\n")
        txtfile.Write("5, contact_side, BOND, OFF, 1.0, 300000000000, 0\r\n")
        txtfile.Write("5, contact_side, REGSHEAR, 1.95e9, 0.01, 30000, 30, 0\r\n")
        txtfile.Write("6, contact_bottom, TYPE, INTF\r\n")
        txtfile.Write("6, contact_bottom, CELL, 1, 0.1, 0.5\r\n")
        txtfile.Write("6, contact_bottom, BOND, OFF, 1.0, 30000000000, 0\r\n")
        txtfile.Write("6, contact_bottom, REGSHEAR, 1.95e9, 0.01, 30000, 30, 10\r\n")
        txtfile.Write("##\r\n")
        txtfile.Write("/SEQUENCE/\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 0, 0\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 0.1, 0.02579\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 0.2, 0.03857\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 0.3, 0.05214\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 0.4, 0.06682\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 0.5, 0.08187\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 0.6, 0.0972\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 0.7, 0.1134\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 0.8, 0.13006\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 0.9, 0.14284\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 1, 0.15056\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 1.1, 0.15318\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 1.2, 0.15287\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 1.3, 0.15391\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 1.4, 0.15043\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 1.5, 0.13618\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 1.6, 0.11234\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 1.7, 0.08948\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 1.8, 0.07764\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 1.9, 0.0732\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 2, 0.05703\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 2.1, 0.02729\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 2.2, -0.00847\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 2.3, -0.04005\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 2.4, -0.07481\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 2.5, -0.10399\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 2.6, -0.13155\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 2.7, -0.15873\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 2.8, -0.18068\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 2.9, -0.19461\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 3, -0.19783\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 3.1, -0.19519\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 3.2, -0.18645\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 3.3, -0.17619\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 3.4, -0.16205\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 3.5, -0.14277\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 3.6, -0.12141\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 3.7, -0.10821\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 3.8, -0.09992\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 3.9, -0.09466\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 4, -0.0922\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 4.1, -0.09078\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 4.2, -0.0896\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 4.3, -0.09277\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 4.4, -0.08811\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 4.5, -0.07581\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 4.6, -0.06347\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 4.7, -0.06235\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 4.8, -0.06889\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 4.9, -0.07115\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 5, -0.06698\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 5.1, -0.05857\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 5.2, -0.0477\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 5.3, -0.03253\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 5.4, -0.01047\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 5.5, 0.00874\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 5.6, 0.0209\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 5.7, 0.03405\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 5.8, 0.04534\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 5.9, 0.05239\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 6, 0.05831\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 6.1, 0.0631\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 6.2, 0.06918\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 6.3, 0.07536\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 6.4, 0.0808\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 6.5, 0.08331\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 6.6, 0.08724\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 6.7, 0.09146\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 6.8, 0.09543\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 6.9, 0.09824\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 7, 0.09714\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 7.1, 0.0996\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 7.2, 0.09729\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 7.3, 0.09113\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 7.4, 0.09079\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 7.5, 0.09294\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 7.6, 0.09121\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 7.7, 0.08673\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 7.8, 0.08506\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 7.9, 0.08389\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 8, 0.07967\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 8.1, 0.06985\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 8.2, 0.05486\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 8.3, 0.03749\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 8.4, 0.01943\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 8.5, -0.00496\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 8.6, -0.02763\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 8.7, -0.04162\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 8.8, -0.0538\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 8.9, -0.06602\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 9, -0.07448\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 9.1, -0.07434\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 9.2, -0.06633\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 9.3, -0.05397\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 9.4, -0.03984\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 9.5, -0.02763\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 9.6, -0.02021\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 9.7, -0.01453\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 9.8, -0.01278\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 9.9, -0.01096\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 10, -0.0077\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 10.1, -0.01017\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 10.2, -0.01432\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 10.3, -0.01484\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 10.4, -0.0135\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 10.5, -0.01321\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 10.6, -0.01481\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 10.7, -0.0188\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 10.8, -0.02247\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 10.9, -0.02446\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 11, -0.02574\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 11.1, -0.02309\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 11.2, -0.02601\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 11.3, -0.03772\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 11.4, -0.04832\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 11.5, -0.0431\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 11.6, -0.02169\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 11.7, 0.00576\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 11.8, 0.02474\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 11.9, 0.04256\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 12, 0.05075\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 12.1, 0.05063\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 12.2, 0.04325\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 12.3, 0.03218\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 12.4, 0.02528\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 12.5, 0.02049\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 12.6, 0.01378\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 12.7, 0.00707\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 12.8, 0.00253\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 12.9, 0.00206\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 13, 0.0022\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 13.1, 0.00096\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 13.2, 0.00086\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 13.3, -0.00085\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 13.4, -0.00309\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 13.5, -0.00772\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 13.6, -0.01433\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 13.7, -0.02153\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 13.8, -0.02551\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 13.9, -0.0289\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 14, -0.03258\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 14.1, -0.03655\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 14.2, -0.03472\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 14.3, -0.03309\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 14.4, -0.03347\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 14.5, -0.0332\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 14.6, -0.03466\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 14.7, -0.0358\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 14.8, -0.03688\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 14.9, -0.04157\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 15, -0.04671\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 15.1, -0.04888\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 15.2, -0.05306\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 15.3, -0.05775\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 15.4, -0.06023\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 15.5, -0.05965\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 15.6, -0.05624\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 15.7, -0.05135\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 15.8, -0.04499\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 15.9, -0.0341\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 16, -0.02285\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 16.1, -0.01509\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 16.2, -0.00692\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 16.3, 0.00506\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 16.4, 0.01652\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 16.5, 0.02508\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 16.6, 0.03502\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 16.7, 0.04597\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 16.8, 0.05366\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 16.9, 0.05775\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 17, 0.06023\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 17.1, 0.06316\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 17.2, 0.06627\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 17.3, 0.06835\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 17.4, 0.06919\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 17.5, 0.06968\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 17.6, 0.07171\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 17.7, 0.07703\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 17.8, 0.07652\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 17.9, 0.07104\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 18, 0.0648\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 18.1, 0.05877\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 18.2, 0.05451\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 18.3, 0.05366\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 18.4, 0.05342\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 18.5, 0.0541\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 18.6, 0.05363\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 18.7, 0.05452\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 18.8, 0.0602\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 18.9, 0.06338\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 19, 0.06156\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 19.1, 0.05979\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 19.2, 0.05619\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 19.3, 0.04986\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 19.4, 0.04312\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 19.5, 0.03987\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 19.6, 0.03957\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 19.7, 0.03626\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 19.8, 0.02965\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 19.9, 0.02677\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 20, 0.02517\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 20.1, 0.02037\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 20.2, 0.01813\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 20.3, 0.01547\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 20.4, 0.01342\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 20.5, 0.01811\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 20.6, 0.02591\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 20.7, 0.02977\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 20.8, 0.02664\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 20.9, 0.02487\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 21, 0.02647\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 21.1, 0.02664\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 21.2, 0.02756\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 21.3, 0.03048\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 21.4, 0.02991\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 21.5, 0.0257\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 21.6, 0.01859\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 21.7, 0.01154\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 21.8, 0.00227\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 21.9, -0.00486\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 22, -0.01075\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 22.1, -0.01862\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 22.2, -0.02606\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 22.3, -0.03064\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 22.4, -0.03367\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 22.5, -0.03681\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 22.6, -0.04221\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 22.7, -0.04496\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 22.8, -0.05069\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 22.9, -0.05585\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 23, -0.06214\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 23.1, -0.07011\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 23.2, -0.07548\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 23.3, -0.08164\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 23.4, -0.08849\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 23.5, -0.09427\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 23.6, -0.09869\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 23.7, -0.10464\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 23.8, -0.11545\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 23.9, -0.12599\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 24, -0.12964\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 24.1, -0.13205\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 24.2, -0.13169\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 24.3, -0.13605\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 24.4, -0.13968\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 24.5, -0.1431\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 24.6, -0.14692\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 24.7, -0.14506\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 24.8, -0.1464\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 24.9, -0.15635\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 25, -0.16671\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 25.1, -0.16772\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 25.2, -0.15881\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 25.3, -0.15135\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 25.4, -0.14098\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 25.5, -0.13065\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 25.6, -0.11596\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 25.7, -0.09765\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 25.8, -0.08229\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 25.9, -0.06515\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 26, -0.04271\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 26.1, -0.02387\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 26.2, -0.00745\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 26.3, 0.00235\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 26.4, 0.00942\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 26.5, 0.01964\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 26.6, 0.02916\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 26.7, 0.04097\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 26.8, 0.05434\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 26.9, 0.06637\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 27, 0.07908\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 27.1, 0.09293\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 27.2, 0.10764\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 27.3, 0.11957\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 27.4, 0.12998\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 27.5, 0.13699\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 27.6, 0.14204\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 27.7, 0.145\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 27.8, 0.14502\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 27.9, 0.14341\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 28, 0.14126\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 28.1, 0.13782\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 28.2, 0.13318\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 28.3, 0.12744\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 28.4, 0.12168\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 28.5, 0.11407\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 28.6, 0.1074\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 28.7, 0.10076\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 28.8, 0.0932\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 28.9, 0.08634\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 29, 0.07954\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 29.1, 0.0717\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 29.2, 0.06525\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 29.3, 0.05873\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 29.4, 0.05202\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 29.5, 0.04591\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 29.6, 0.04093\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 29.7, 0.03705\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 29.8, 0.03651\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 29.9, 0.03679\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 30, 0.03586\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 30.1, 0.03357\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 30.2, 0.03293\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 30.3, 0.03493\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 30.4, 0.03665\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 30.5, 0.03601\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 30.6, 0.0351\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 30.7, 0.03501\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 30.8, 0.03395\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 30.9, 0.03009\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 31, 0.02663\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 31.1, 0.02498\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 31.2, 0.02365\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 31.3, 0.02206\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 31.4, 0.01954\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 31.5, 0.01674\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 31.6, 0.01512\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 31.7, 0.01495\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 31.8, 0.01596\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 31.9, 0.01703\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 32, 0.01662\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 32.1, 0.01645\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 32.2, 0.01646\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 32.3, 0.01569\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 32.4, 0.01538\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 32.5, 0.01445\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 32.6, 0.01284\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 32.7, 0.01157\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 32.8, 0.00974\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 32.9, 0.00689\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 33, 0.00316\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 33.1, -0.00034\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 33.2, -0.00289\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 33.3, -0.00584\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 33.4, -0.00992\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 33.5, -0.01352\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 33.6, -0.01522\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 33.7, -0.01616\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 33.8, -0.01706\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 33.9, -0.01841\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 34, -0.01935\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 34.1, -0.02029\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 34.2, -0.02211\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 34.3, -0.025\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 34.4, -0.02747\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 34.5, -0.02879\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 34.6, -0.03021\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 34.7, -0.03228\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 34.8, -0.03378\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 34.9, -0.03503\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 35, -0.03681\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 35.1, -0.03876\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 35.2, -0.03982\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 35.3, -0.04038\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 35.4, -0.04052\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 35.5, -0.0412\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 35.6, -0.04153\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 35.7, -0.04141\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 35.8, -0.04178\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 35.9, -0.04269\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 36, -0.0432\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 36.1, -0.04399\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 36.2, -0.04521\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 36.3, -0.04523\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 36.4, -0.04465\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 36.5, -0.04422\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 36.6, -0.0438\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 36.7, -0.04327\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 36.8, -0.04314\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 36.9, -0.04372\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 37, -0.04525\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 37.1, -0.04767\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 37.2, -0.05113\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 37.3, -0.05563\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 37.4, -0.05966\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 37.5, -0.06274\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 37.6, -0.06556\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 37.7, -0.06745\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 37.8, -0.06856\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 37.9, -0.06866\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 38, -0.06774\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 38.1, -0.06648\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 38.2, -0.06412\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 38.3, -0.06094\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 38.4, -0.05703\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 38.5, -0.05279\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 38.6, -0.04871\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 38.7, -0.04467\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 38.8, -0.04102\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 38.9, -0.03742\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 39, -0.03343\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 39.1, -0.02939\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 39.2, -0.02599\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 39.3, -0.02289\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 39.4, -0.01954\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 39.5, -0.01614\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 39.6, -0.01289\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 39.7, -0.00994\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 39.8, -0.00647\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 39.9, -0.002\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 40, 0.00297\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 40.1, 0.00736\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 40.2, 0.01091\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 40.3, 0.01321\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 40.4, 0.01429\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 40.5, 0.01387\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 40.6, 0.0128\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 40.7, 0.0118\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 40.8, 0.01043\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 40.9, 0.00898\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 41, 0.00808\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 41.1, 0.00784\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 41.2, 0.00814\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 41.3, 0.009\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 41.4, 0.01058\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 41.5, 0.01255\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 41.6, 0.01386\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 41.7, 0.01463\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 41.8, 0.01566\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 41.9, 0.01735\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 42, 0.01909\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 42.1, 0.02047\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 42.2, 0.02239\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 42.3, 0.02527\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 42.4, 0.02915\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 42.5, 0.03435\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 42.6, 0.04049\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 42.7, 0.04701\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 42.8, 0.05365\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 42.9, 0.06023\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 43, 0.06674\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 43.1, 0.07279\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 43.2, 0.07787\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 43.3, 0.08169\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 43.4, 0.08418\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 43.5, 0.08653\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 43.6, 0.08915\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 43.7, 0.09228\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 43.8, 0.09546\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 43.9, 0.09799\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 44, 0.09966\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 44.1, 0.10012\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 44.2, 0.09974\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 44.3, 0.09878\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 44.4, 0.09717\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 44.5, 0.09464\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 44.6, 0.09231\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 44.7, 0.09015\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 44.8, 0.08772\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 44.9, 0.08485\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 45, 0.08119\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 45.1, 0.07662\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 45.2, 0.0705\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 45.3, 0.0628\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 45.4, 0.05434\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 45.5, 0.046\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 45.6, 0.03757\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 45.7, 0.02864\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 45.8, 0.01957\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 45.9, 0.01103\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 46, 0.0033\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 46.1, -0.00358\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 46.2, -0.01025\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 46.3, -0.01705\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 46.4, -0.02429\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 46.5, -0.03151\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 46.6, -0.03867\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 46.7, -0.04573\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 46.8, -0.05235\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 46.9, -0.05839\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 47, -0.064\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 47.1, -0.06882\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 47.2, -0.07272\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 47.3, -0.07549\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 47.4, -0.07727\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 47.5, -0.07808\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 47.6, -0.07798\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 47.7, -0.07719\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 47.8, -0.07621\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 47.9, -0.07544\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 48, -0.07423\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 48.1, -0.0715\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 48.2, -0.0676\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 48.3, -0.06301\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 48.4, -0.05815\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 48.5, -0.0531\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 48.6, -0.04837\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 48.7, -0.0444\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 48.8, -0.04127\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 48.9, -0.03875\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 49, -0.03631\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 49.1, -0.03386\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 49.2, -0.03183\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 49.3, -0.03008\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 49.4, -0.02788\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 49.5, -0.02475\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 49.6, -0.02081\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 49.7, -0.01682\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 49.8, -0.01314\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 49.9, -0.00985\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 50, -0.00697\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 50.1, -0.00456\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 50.2, -0.00245\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 50.3, -0.0003\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 50.4, 0.00176\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 50.5, 0.00351\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 50.6, 0.00449\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 50.7, 0.00433\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 50.8, 0.00239\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 50.9, 0.00056\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 51, -0.00177\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 51.1, -0.00524\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 51.2, -0.00866\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 51.3, -0.01192\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 51.4, -0.01454\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 51.5, -0.01648\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 51.6, -0.01751\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 51.7, -0.01788\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 51.8, -0.01786\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 51.9, -0.01727\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 52, -0.01579\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 52.1, -0.01349\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 52.2, -0.01118\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 52.3, -0.00916\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 52.4, -0.00758\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 52.5, -0.00617\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 52.6, -0.00504\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 52.7, -0.00397\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 52.8, -0.00272\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 52.9, -0.00127\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 53, 0.00076\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 53.1, 0.00314\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 53.2, 0.00543\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 53.3, 0.00693\r\n")
        txtfile.Write("EL_EW_DISP, DATA, 53.4, 0.00818\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 0, 0\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 0.1, 0.01648\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 0.2, 0.01025\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 0.3, 0.00276\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 0.4, -0.00604\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 0.5, -0.01594\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 0.6, -0.0263\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 0.7, -0.03888\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 0.8, -0.05293\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 0.9, -0.06502\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 1, -0.07335\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 1.1, -0.07721\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 1.2, -0.07637\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 1.3, -0.07901\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 1.4, -0.08034\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 1.5, -0.07089\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 1.6, -0.05135\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 1.7, -0.02963\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 1.8, -0.02554\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 1.9, -0.03742\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 2, -0.05289\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 2.1, -0.05271\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 2.2, -0.02552\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 2.3, -0.00411\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 2.4, 0.01428\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 2.5, 0.03513\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 2.6, 0.04563\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 2.7, 0.04307\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 2.8, 0.03293\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 2.9, 0.0196\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 3, 0.0017\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 3.1, -0.01492\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 3.2, -0.02779\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 3.3, -0.0334\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 3.4, -0.0321\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 3.5, -0.03493\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 3.6, -0.04621\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 3.7, -0.06167\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 3.8, -0.07657\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 3.9, -0.08979\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 4, -0.09508\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 4.1, -0.09516\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 4.2, -0.09304\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 4.3, -0.07931\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 4.4, -0.05149\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 4.5, -0.02915\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 4.6, -0.02298\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 4.7, -0.0158\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 4.8, -0.00298\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 4.9, 0.02159\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 5, 0.03936\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 5.1, 0.04293\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 5.2, 0.03733\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 5.3, 0.02289\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 5.4, 0.00052\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 5.5, -0.02064\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 5.6, -0.03785\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 5.7, -0.04336\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 5.8, -0.04228\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 5.9, -0.04064\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 6, -0.0395\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 6.1, -0.03705\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 6.2, -0.03461\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 6.3, -0.03015\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 6.4, -0.02548\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 6.5, -0.02097\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 6.6, -0.01858\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 6.7, -0.01684\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 6.8, -0.01573\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 6.9, -0.01209\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 7, -0.0071\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 7.1, -0.00379\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 7.2, -0.00001\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 7.3, 0.00326\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 7.4, 0.00691\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 7.5, 0.01256\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 7.6, 0.01973\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 7.7, 0.02944\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 7.8, 0.04407\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 7.9, 0.0597\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 8, 0.0718\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 8.1, 0.08128\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 8.2, 0.0873\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 8.3, 0.09081\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 8.4, 0.09594\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 8.5, 0.1039\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 8.6, 0.1086\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 8.7, 0.10253\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 8.8, 0.09292\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 8.9, 0.08374\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 9, 0.08192\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 9.1, 0.07883\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 9.2, 0.07049\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 9.3, 0.06841\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 9.4, 0.06764\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 9.5, 0.06006\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 9.6, 0.05715\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 9.7, 0.05613\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 9.8, 0.05469\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 9.9, 0.05651\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 10, 0.06127\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 10.1, 0.06577\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 10.2, 0.06985\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 10.3, 0.07301\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 10.4, 0.08143\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 10.5, 0.08597\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 10.6, 0.08961\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 10.7, 0.09314\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 10.8, 0.09173\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 10.9, 0.08814\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 11, 0.08406\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 11.1, 0.08246\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 11.2, 0.07983\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 11.3, 0.07538\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 11.4, 0.06602\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 11.5, 0.05003\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 11.6, 0.02808\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 11.7, 0.0083\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 11.8, -0.00152\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 11.9, 0.00322\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 12, 0.00958\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 12.1, 0.00625\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 12.2, -0.00577\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 12.3, -0.02484\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 12.4, -0.04217\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 12.5, -0.0553\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 12.6, -0.06508\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 12.7, -0.07353\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 12.8, -0.08249\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 12.9, -0.09098\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 13, -0.09553\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 13.1, -0.09592\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 13.2, -0.09021\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 13.3, -0.0861\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 13.4, -0.08307\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 13.5, -0.08053\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 13.6, -0.08071\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 13.7, -0.08304\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 13.8, -0.08492\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 13.9, -0.08423\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 14, -0.08891\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 14.1, -0.09375\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 14.2, -0.10174\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 14.3, -0.10262\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 14.4, -0.09903\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 14.5, -0.0937\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 14.6, -0.08902\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 14.7, -0.08828\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 14.8, -0.08817\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 14.9, -0.08854\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 15, -0.08877\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 15.1, -0.08727\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 15.2, -0.08328\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 15.3, -0.08005\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 15.4, -0.07865\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 15.5, -0.07664\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 15.6, -0.07026\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 15.7, -0.06112\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 15.8, -0.0548\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 15.9, -0.05074\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 16, -0.04741\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 16.1, -0.04499\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 16.2, -0.03942\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 16.3, -0.03655\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 16.4, -0.03196\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 16.5, -0.02541\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 16.6, -0.02015\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 16.7, -0.01629\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 16.8, -0.01456\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 16.9, -0.01299\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 17, -0.00542\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 17.1, 0.00356\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 17.2, 0.01263\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 17.3, 0.01784\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 17.4, 0.02025\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 17.5, 0.01913\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 17.6, 0.01396\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 17.7, 0.00877\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 17.8, 0.00949\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 17.9, 0.01094\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 18, 0.0134\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 18.1, 0.01621\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 18.2, 0.01877\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 18.3, 0.02015\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 18.4, 0.02158\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 18.5, 0.0248\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 18.6, 0.03143\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 18.7, 0.03865\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 18.8, 0.04238\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 18.9, 0.04556\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 19, 0.04673\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 19.1, 0.04802\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 19.2, 0.05076\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 19.3, 0.05098\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 19.4, 0.05195\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 19.5, 0.05298\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 19.6, 0.05495\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 19.7, 0.05727\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 19.8, 0.0558\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 19.9, 0.05094\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 20, 0.0454\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 20.1, 0.04329\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 20.2, 0.04621\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 20.3, 0.0466\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 20.4, 0.04696\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 20.5, 0.04948\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 20.6, 0.05167\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 20.7, 0.05738\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 20.8, 0.05869\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 20.9, 0.05745\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 21, 0.05999\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 21.1, 0.06287\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 21.2, 0.06885\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 21.3, 0.07495\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 21.4, 0.07705\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 21.5, 0.07717\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 21.6, 0.07668\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 21.7, 0.07326\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 21.8, 0.06521\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 21.9, 0.05667\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 22, 0.05264\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 22.1, 0.04868\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 22.2, 0.04446\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 22.3, 0.04261\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 22.4, 0.04138\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 22.5, 0.04046\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 22.6, 0.03764\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 22.7, 0.03256\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 22.8, 0.03099\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 22.9, 0.03112\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 23, 0.02878\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 23.1, 0.02346\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 23.2, 0.01773\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 23.3, 0.01314\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 23.4, 0.00718\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 23.5, -0.00033\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 23.6, -0.00725\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 23.7, -0.0139\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 23.8, -0.0204\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 23.9, -0.02459\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 24, -0.0302\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 24.1, -0.03587\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 24.2, -0.04551\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 24.3, -0.05008\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 24.4, -0.05711\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 24.5, -0.06674\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 24.6, -0.07354\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 24.7, -0.07508\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 24.8, -0.07349\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 24.9, -0.07528\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 25, -0.08316\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 25.1, -0.08971\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 25.2, -0.0924\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 25.3, -0.09389\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 25.4, -0.09953\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 25.5, -0.10416\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 25.6, -0.10274\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 25.7, -0.09318\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 25.8, -0.08551\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 25.9, -0.07844\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 26, -0.07025\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 26.1, -0.05677\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 26.2, -0.03597\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 26.3, -0.02037\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 26.4, -0.01401\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 26.5, -0.01078\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 26.6, -0.00779\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 26.7, -0.00454\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 26.8, 0.00247\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 26.9, 0.01128\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 27, 0.0194\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 27.1, 0.02904\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 27.2, 0.03783\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 27.3, 0.04498\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 27.4, 0.05003\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 27.5, 0.05172\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 27.6, 0.05239\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 27.7, 0.05101\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 27.8, 0.04629\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 27.9, 0.04254\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 28, 0.03973\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 28.1, 0.03599\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 28.2, 0.0343\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 28.3, 0.03213\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 28.4, 0.03074\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 28.5, 0.02995\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 28.6, 0.02835\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 28.7, 0.02547\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 28.8, 0.02084\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 28.9, 0.01896\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 29, 0.0185\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 29.1, 0.0171\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 29.2, 0.01359\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 29.3, 0.00876\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 29.4, 0.00563\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 29.5, 0.00381\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 29.6, 0.00206\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 29.7, 0.0002\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 29.8, -0.00292\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 29.9, -0.00563\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 30, -0.00685\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 30.1, -0.00712\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 30.2, -0.00881\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 30.3, -0.01409\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 30.4, -0.01885\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 30.5, -0.02118\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 30.6, -0.02397\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 30.7, -0.02885\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 30.8, -0.03434\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 30.9, -0.03905\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 31, -0.04143\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 31.1, -0.04156\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 31.2, -0.04115\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 31.3, -0.04249\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 31.4, -0.0447\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 31.5, -0.04738\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 31.6, -0.04798\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 31.7, -0.04741\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 31.8, -0.04767\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 31.9, -0.0481\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 32, -0.04769\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 32.1, -0.0452\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 32.2, -0.04151\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 32.3, -0.03812\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 32.4, -0.03371\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 32.5, -0.02934\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 32.6, -0.02534\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 32.7, -0.0214\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 32.8, -0.01687\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 32.9, -0.0116\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 33, -0.00672\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 33.1, -0.00149\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 33.2, 0.00368\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 33.3, 0.00867\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 33.4, 0.01381\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 33.5, 0.01893\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 33.6, 0.02301\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 33.7, 0.02653\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 33.8, 0.03054\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 33.9, 0.03447\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 34, 0.03753\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 34.1, 0.03952\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 34.2, 0.04024\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 34.3, 0.04065\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 34.4, 0.0424\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 34.5, 0.04418\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 34.6, 0.04418\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 34.7, 0.04264\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 34.8, 0.04201\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 34.9, 0.04346\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 35, 0.0445\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 35.1, 0.04341\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 35.2, 0.04206\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 35.3, 0.04173\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 35.4, 0.04186\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 35.5, 0.04074\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 35.6, 0.03897\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 35.7, 0.03691\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 35.8, 0.03504\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 35.9, 0.0335\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 36, 0.03119\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 36.1, 0.02865\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 36.2, 0.02652\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 36.3, 0.02512\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 36.4, 0.02458\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 36.5, 0.02483\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 36.6, 0.02602\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 36.7, 0.02709\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 36.8, 0.02657\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 36.9, 0.02338\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 37, 0.01792\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 37.1, 0.01136\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 37.2, 0.00445\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 37.3, -0.00207\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 37.4, -0.00811\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 37.5, -0.01285\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 37.6, -0.01616\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 37.7, -0.01904\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 37.8, -0.02114\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 37.9, -0.02196\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 38, -0.02171\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 38.1, -0.02127\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 38.2, -0.02037\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 38.3, -0.01901\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 38.4, -0.01802\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 38.5, -0.01673\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 38.6, -0.01438\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 38.7, -0.01086\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 38.8, -0.00782\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 38.9, -0.00643\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 39, -0.0064\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 39.1, -0.00717\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 39.2, -0.00804\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 39.3, -0.00866\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 39.4, -0.00916\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 39.5, -0.00956\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 39.6, -0.0093\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 39.7, -0.00787\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 39.8, -0.00639\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 39.9, -0.00558\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 40, -0.00464\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 40.1, -0.00348\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 40.2, -0.00227\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 40.3, -0.00079\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 40.4, 0.00076\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 40.5, 0.0015\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 40.6, 0.00159\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 40.7, 0.00147\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 40.8, 0.00131\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 40.9, 0.00032\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 41, -0.00239\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 41.1, -0.00676\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 41.2, -0.01108\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 41.3, -0.01463\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 41.4, -0.01824\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 41.5, -0.02161\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 41.6, -0.02433\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 41.7, -0.02634\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 41.8, -0.0277\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 41.9, -0.02789\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 42, -0.0271\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 42.1, -0.026\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 42.2, -0.02461\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 42.3, -0.02244\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 42.4, -0.01969\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 42.5, -0.01721\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 42.6, -0.01562\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 42.7, -0.01468\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 42.8, -0.01379\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 42.9, -0.01261\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 43, -0.01151\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 43.1, -0.01105\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 43.2, -0.01079\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 43.3, -0.01\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 43.4, -0.00907\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 43.5, -0.0084\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 43.6, -0.00777\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 43.7, -0.00716\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 43.8, -0.00668\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 43.9, -0.00647\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 44, -0.00682\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 44.1, -0.00775\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 44.2, -0.00858\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 44.3, -0.00902\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 44.4, -0.00891\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 44.5, -0.0079\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 44.6, -0.00601\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 44.7, -0.00343\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 44.8, -0.0005\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 44.9, 0.00263\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 45, 0.00574\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 45.1, 0.00848\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 45.2, 0.0103\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 45.3, 0.01101\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 45.4, 0.0111\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 45.5, 0.01075\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 45.6, 0.01037\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 45.7, 0.01051\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 45.8, 0.01137\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 45.9, 0.01253\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 46, 0.01364\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 46.1, 0.01413\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 46.2, 0.01368\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 46.3, 0.01256\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 46.4, 0.01159\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 46.5, 0.01112\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 46.6, 0.01035\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 46.7, 0.00907\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 46.8, 0.00765\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 46.9, 0.00655\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 47, 0.0063\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 47.1, 0.00707\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 47.2, 0.00861\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 47.3, 0.01055\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 47.4, 0.01263\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 47.5, 0.01481\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 47.6, 0.01672\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 47.7, 0.01832\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 47.8, 0.02023\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 47.9, 0.02294\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 48, 0.02575\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 48.1, 0.02792\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 48.2, 0.02914\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 48.3, 0.0294\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 48.4, 0.02874\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 48.5, 0.0273\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 48.6, 0.02522\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 48.7, 0.02272\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 48.8, 0.02022\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 48.9, 0.01771\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 49, 0.01529\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 49.1, 0.01294\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 49.2, 0.01059\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 49.3, 0.00803\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 49.4, 0.0052\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 49.5, 0.00197\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 49.6, -0.00154\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 49.7, -0.00488\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 49.8, -0.00746\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 49.9, -0.00946\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 50, -0.01115\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 50.1, -0.0129\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 50.2, -0.01472\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 50.3, -0.01662\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 50.4, -0.01856\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 50.5, -0.02037\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 50.6, -0.02166\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 50.7, -0.0226\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 50.8, -0.02314\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 50.9, -0.02344\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 51, -0.02249\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 51.1, -0.02165\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 51.2, -0.02081\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 51.3, -0.02001\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 51.4, -0.01859\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 51.5, -0.01685\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 51.6, -0.01535\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 51.7, -0.01374\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 51.8, -0.0125\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 51.9, -0.01118\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 52, -0.00984\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 52.1, -0.00904\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 52.2, -0.00835\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 52.3, -0.00798\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 52.4, -0.0073\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 52.5, -0.00595\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 52.6, -0.00447\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 52.7, -0.00351\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 52.8, -0.00249\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 52.9, -0.00071\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 53, 0.00158\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 53.1, 0.00379\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 53.2, 0.00556\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 53.3, 0.00696\r\n")
        txtfile.Write("EL_NS_DISP, DATA, 53.4, 0.00766\r\n")
        txtfile.Write("##\r\n")

    def _WriteEnd(self, txtfile):
        txtfile.Write("/ELEM_PROPERTY/\r\n")
        txtfile.Write("CONTACT_TARGET, side_target\r\n")
        txtfile.Write("CONTACT_TARGET, bottom_target\r\n")
        txtfile.Write("##\r\n")
        txtfile.Write("/STEP/\r\n")
        txtfile.Write("step_init, TYPE, INITIAL\r\n")
        txtfile.Write("step_gravity, TYPE, STATIC\r\n")
        txtfile.Write("step_gravity, TIME, 1.6e-4, 5\r\n")
        txtfile.Write("step_gravity, LOADING, RAMP, 0.5\r\n")
        txtfile.Write("step_gravity, DAMPING, ON, 100\r\n")
        txtfile.Write("step_gravity, OUTPUT, 10\r\n")
        txtfile.Write("step_gravity, CONSTRAINT, bc_y, Y, bc_xy, N, bc_z, Y, bc_wall_fixall, N\r\n")
        txtfile.Write("step_gravity, LOAD, GRAVITY_SET, Y\r\n")
        txtfile.Write("step_seismic, TYPE, DYNA\r\n")
        txtfile.Write("step_seismic, TIME, 1.6e-4, 20\r\n")
        txtfile.Write("step_seismic, DAMPING, ON, 0.1\r\n")
        txtfile.Write("step_seismic, OUTPUT, 200\r\n")
        txtfile.Write("step_seismic, CONSTRAINT, DISP_SET, Y, bc_wall_fixz, Y\r\n")
        txtfile.Write("##\r\n")
        pass

    def GenerateModel(self):
        # self._LogNodeCount()
        self._GenerateSoilModel()
        self._LogNodeCount()
        self._LogElementCount()
        self._GenerateStructModel()
        self._AdjustNode()
        self._GenerateNodeSet()

    def _GenerateNodeSet(self):
        self._nodesets.append(self.nodeset_x)
        self._nodesets.append(self.nodeset_y) 
        self._nodesets.append(self.nodeset_z)
        self._nodesets.append(self.nodeset_xy)
        self._nodesets.append(self.nodeset_x_con)
        self._nodesets.append(self.nodeset_y_con) 
        self._nodesets.append(self.nodeset_xy_con)
        self._nodesets.append(self.nodeset_disp)
        self._elemsets.append(self.elemset_side_target)
        self._elemsets.append(self.elemset_bottom_target)

        