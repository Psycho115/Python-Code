from math import sin, cos, tan, sqrt, pi
from ItemModule import *

g_unit_number = 0

def RotateUnit(unit, rotation_angle):
    unit._RotateNodes(rotation_angle)

class UnitBase(object):

    def __init__(self, barlength, angle, expanding_force):
        global g_unit_number
        g_unit_number += 1
        self._id = g_unit_number
        self._unit_list = []
        self._couples = []
        self._supports = []
        self._loads = []
        self._elements = []
        self._nodes = {}
        self._barlength = barlength
        self._angle = angle
        self._expanding_force = expanding_force
         
    def _RotateNodes(self, rotation_angle):
        for (key,node) in self._nodes.items():
            node.RotateNode(rotation_angle)

    def _UnitNodes(self):
        nodes = []
        for (key, node) in self._nodes.items():
            nodes.append(node)
        nodes.sort(key=lambda node: node._id)
        return nodes
    
    def _SetSupports(self):
        supports = []
        for (key, node) in self._nodes.items():
            if self._id == 1:
                if key == "node_1":
                    supports.append(SupportItem(node, True, True))
                else:
                    supports.append(SupportItem(node, False, False))
            else:
                supports.append(SupportItem(node, False, False))
        supports.sort(key=lambda support: support._node._id)
        self._supports = supports


class GAEUnit(UnitBase):

    def __init__(self, barlength, angle, expanding_force):
        UnitBase.__init__(self, barlength, angle, expanding_force)
        node_1 = NodeItem(0, 0, 0, 0)
        node_couple_1 = NodeItem(0, barlength, 0, 1)
        node_couple_2 = NodeItem(0, barlength, 0, 1)
        node_2 = NodeItem(barlength*sin(angle*pi/180), barlength*(1+cos(angle*pi/180)), 0, 0)
        self._nodes = {"node_1": node_1, "node_2": node_2, "node_couple_1": node_couple_1, "node_couple_2": node_couple_2}

    def _LinkNodesIntoElement(self):
        self._elements.append(ElementItem(self._nodes["node_1"], self._nodes["node_couple_1"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple_1"], self._nodes["node_2"], 1))
        if len(self._nodes) == 0:
            print "not ready!!!"
            return
        self._elements.append(ElementItem(self._unit_list[0]._nodes["node_1"], self._nodes["node_couple_2"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple_2"], self._unit_list[1]._nodes["node_2"], 1))

    def _AssignUnitList(self, unit_before, unit_after):
        self._unit_list.append(unit_before)
        self._unit_list.append(unit_after)
        print "self:%d pre:%d next:%d" %(self._id, unit_before._id, unit_after._id)

    def _LinkCouples(self):
        self._couples.append(CoupleItem(self._nodes["node_couple_1"], self._nodes["node_couple_2"], 1))

    def _SetDeadload(self):
        f = self._expanding_force
        (x, y) = (self._nodes["node_couple_2"]._x, self._nodes["node_couple_2"]._y)
        norm = sqrt(x*x+y*y)
        self._loads.append(LoadItem(self._nodes["node_1"], f*x/norm, f*y/norm, 0))

class DoubleGAEUnit(UnitBase):

    def __init__(self, barlength, angle, expanding_force):
        UnitBase.__init__(self, barlength, angle, expanding_force)
        node_1 = NodeItem(0, 0, 0, 0)
        node_couple1_1 = NodeItem(0, barlength, 0, 1)
        node_couple1_2 = NodeItem(0, barlength, 0, 1)
        node_couple2_1 = NodeItem(barlength*sin(angle*pi/180), barlength*(1+cos(angle*pi/180)), 0, 1)
        node_couple2_2 = NodeItem(barlength*sin(angle*pi/180), barlength*(1+cos(angle*pi/180)), 0, 1)
        node_2 = NodeItem(barlength*(sin(angle*pi/180)+sin(2*angle*pi/180)), barlength*(1+cos(angle*pi/180)+cos(2*angle*pi/180)), 0, 0)
        self._nodes = {"node_1": node_1, "node_2": node_2,
                       "node_couple1_1": node_couple1_1, "node_couple1_2": node_couple1_2,
                       "node_couple2_1": node_couple2_1, "node_couple2_2": node_couple2_2}

    def _LinkNodesIntoElement(self):
        if len(self._nodes) == 0:
            print "not ready!!!"
            return
        self._elements.append(ElementItem(self._nodes["node_1"], self._nodes["node_couple1_1"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple1_1"], self._nodes["node_couple2_1"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple2_1"], self._nodes["node_2"], 1))
        self._elements.append(ElementItem(self._nodes["node_1"], self._unit_list[1]._nodes["node_couple1_2"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple1_2"], self._unit_list[1]._nodes["node_couple2_2"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple2_2"], self._unit_list[1]._nodes["node_2"], 1))

    def _AssignUnitList(self, unit_before, unit_after):
        self._unit_list.append(unit_before)
        self._unit_list.append(unit_after)
        print "self:%d pre:%d next:%d" %(self._id, unit_before._id, unit_after._id)

    def _LinkCouples(self):
        self._couples.append(CoupleItem(self._nodes["node_couple1_1"], self._nodes["node_couple1_2"], 1))
        self._couples.append(CoupleItem(self._nodes["node_couple2_1"], self._nodes["node_couple2_2"], 1))

    def _SetDeadload(self):
        f = self._expanding_force
        (x, y) = (self._nodes["node_couple2_1"]._x, self._nodes["node_couple2_1"]._y)
        norm = sqrt(x*x+y*y)
        self._loads.append(LoadItem(self._nodes["node_1"], f*x/norm, f*y/norm, 0))

class TripleGAEUnit(UnitBase):

    def __init__(self, barlength, angle, expanding_force):
        UnitBase.__init__(self, barlength, angle, expanding_force)
        node_1 = NodeItem(0, 0, 0, 0)
        node_couple1_1 = NodeItem(0, barlength, 0, 1)
        node_couple1_2 = NodeItem(0, barlength, 0, 1)
        node_couple2_1 = NodeItem(barlength*sin(angle*pi/180), barlength*(1+cos(angle*pi/180)), 0, 1)
        node_couple2_2 = NodeItem(barlength*sin(angle*pi/180), barlength*(1+cos(angle*pi/180)), 0, 1)
        node_couple3_1 = NodeItem(barlength*(sin(angle*pi/180)+sin(2*angle*pi/180)), barlength*(1+cos(angle*pi/180)+cos(2*angle*pi/180)), 0, 0)
        node_couple3_2 = NodeItem(barlength*(sin(angle*pi/180)+sin(2*angle*pi/180)), barlength*(1+cos(angle*pi/180)+cos(2*angle*pi/180)), 0, 0)
        node_2 = NodeItem(barlength*(sin(angle*pi/180)+sin(2*angle*pi/180)+sin(3*angle*pi/180)), barlength*(1+cos(angle*pi/180)+cos(2*angle*pi/180)+cos(3*angle*pi/180)), 0, 0)
        self._nodes = {"node_1": node_1, "node_2": node_2,
                       "node_couple1_1": node_couple1_1, "node_couple1_2": node_couple1_2,
                       "node_couple2_1": node_couple2_1, "node_couple2_2": node_couple2_2,
                       "node_couple3_1": node_couple3_1, "node_couple3_2": node_couple3_2}

    def _LinkNodesIntoElement(self):
        if len(self._nodes) == 0:
            print "not ready!!!"
            return
        self._elements.append(ElementItem(self._nodes["node_1"], self._nodes["node_couple1_1"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple1_1"], self._nodes["node_couple2_1"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple2_1"], self._nodes["node_couple3_1"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple3_1"], self._nodes["node_2"], 1))

        self._elements.append(ElementItem(self._nodes["node_1"], self._unit_list[1]._nodes["node_couple1_2"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple1_2"], self._unit_list[1]._nodes["node_couple2_2"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple2_2"], self._unit_list[1]._nodes["node_couple3_2"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple3_2"], self._unit_list[1]._nodes["node_2"], 1))

    def _AssignUnitList(self, unit_before, unit_after):
        self._unit_list.append(unit_before)
        self._unit_list.append(unit_after)
        print "self:%d pre:%d next:%d" %(self._id, unit_before._id, unit_after._id)

    def _LinkCouples(self):
        self._couples.append(CoupleItem(self._nodes["node_couple1_1"], self._nodes["node_couple1_2"], 1))
        self._couples.append(CoupleItem(self._nodes["node_couple2_1"], self._nodes["node_couple2_2"], 1))
        self._couples.append(CoupleItem(self._nodes["node_couple3_1"], self._nodes["node_couple3_2"], 1))

    def _SetDeadload(self):
        f = self._expanding_force
        (x, y) = (self._nodes["node_couple2_1"]._x, self._nodes["node_couple2_1"]._y)
        norm = sqrt(x*x+y*y)
        self._loads.append(LoadItem(self._nodes["node_1"], f*x/norm, f*y/norm, 0))

        
class DeployeableUnitBase(object):

    def __init__(self, barlength, angle, expanding_force):
        global g_unit_number
        g_unit_number += 1
        self._id = g_unit_number
        self._unit_list = []
        self._couples = []
        self._supports = []
        self._loads = []
        self._elements = []
        self._nodes = {}
        self._barlength = barlength
        self._angle = angle
        self._expanding_force = expanding_force
         
    def _RotateNodes(self, rotation_angle):
        for (key,node) in self._nodes.items():
            node.RotateNode(rotation_angle)

    def _UnitNodes(self):
        nodes = []
        for (key, node) in self._nodes.items():
            nodes.append(node)
        nodes.sort(key=lambda node: node._id)
        return nodes
    
    def _SetSupports(self):
        supports = []
        supports.append(SupportItem(self._nodes["node_1"], False, False))
        supports.sort(key=lambda support: support._node._id)
        self._supports = supports

    def _SetDeadload(self):
        f = self._expanding_force
        (x, y) = (self._nodes["node_3"]._x, self._nodes["node_3"]._y)
        norm = sqrt(x*x+y*y)
        self._loads.append(LoadItem(self._nodes["node_3"], -0.35*f*x/norm, -0.35*f*y/norm, 0.2*f))
        (x, y) = (self._nodes["node_4"]._x, self._nodes["node_4"]._y)
        norm = sqrt(x*x+y*y)
        self._loads.append(LoadItem(self._nodes["node_4"], -0.5*f*x/norm, -0.5*f*y/norm, 0.2*f))

class DeployeableUnit(DeployeableUnitBase):

    def __init__(self, barlength, angle, modulenumber, expanding_force):
        DeployeableUnitBase.__init__(self, barlength, angle, expanding_force)
        self._module_number = modulenumber
        module_angle = (modulenumber-2)*180.0/modulenumber
        y = barlength*tan(module_angle*0.5*pi/180)
        z = barlength*sin(angle*pi/180)
        node_1 = NodeItem(-barlength, y, 0, 0)
        node_2 = NodeItem(barlength, y, z, 0)
        node_3 = NodeItem(-barlength, y, 2*z, 0)
        node_4 = NodeItem(barlength, y, 3*z, 0)
        node_couple1_1 = NodeItem(0, y, 0, 1)
        node_couple1_2 = NodeItem(0, y, 0, 1)
        node_couple2_1 = NodeItem(0, y, z, 1)
        node_couple2_2 = NodeItem(0, y, z, 1)
        node_couple3_1 = NodeItem(0, y, 2*z, 1)
        node_couple3_2 = NodeItem(0, y, 2*z, 1)
        self._nodes = {"node_1": node_1, "node_2": node_2, "node_3": node_3, "node_4": node_4,
                       "node_couple1_1": node_couple1_1, "node_couple1_2": node_couple1_2,
                       "node_couple2_1": node_couple2_1, "node_couple2_2": node_couple2_2,
                       "node_couple3_1": node_couple3_1, "node_couple3_2": node_couple3_2}

    def _LinkNodesIntoElement(self):
        if len(self._nodes) == 0:
            print "not ready!!!"
            return
        self._elements.append(ElementItem(self._nodes["node_1"], self._nodes["node_couple1_1"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple1_1"], self._nodes["node_2"], 1))
        self._elements.append(ElementItem(self._nodes["node_2"], self._nodes["node_couple2_1"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple2_1"], self._nodes["node_3"], 1))
        self._elements.append(ElementItem(self._nodes["node_3"], self._nodes["node_couple3_1"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple3_1"], self._nodes["node_4"], 1))

        self._elements.append(ElementItem(self._unit_list[0]._nodes["node_1"], self._nodes["node_couple1_2"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple1_2"], self._unit_list[1]._nodes["node_2"], 1))
        self._elements.append(ElementItem(self._unit_list[1]._nodes["node_2"], self._nodes["node_couple2_2"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple2_2"], self._unit_list[0]._nodes["node_3"], 1))
        self._elements.append(ElementItem(self._unit_list[0]._nodes["node_3"], self._nodes["node_couple3_2"], 1))
        self._elements.append(ElementItem(self._nodes["node_couple3_2"], self._unit_list[1]._nodes["node_4"], 1))

    def _AssignUnitList(self, unit_before, unit_after):
        self._unit_list.append(unit_before)
        self._unit_list.append(unit_after)
        print "self:%d pre:%d next:%d" %(self._id, unit_before._id, unit_after._id)

    def _LinkCouples(self):
        self._couples.append(CoupleItem(self._nodes["node_couple1_1"], self._nodes["node_couple1_2"], 1))
        self._couples.append(CoupleItem(self._nodes["node_couple2_1"], self._nodes["node_couple2_2"], 1))
        self._couples.append(CoupleItem(self._nodes["node_couple3_1"], self._nodes["node_couple3_2"], 1))

