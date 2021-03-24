from math import *

g_node_number = 0
g_element_number = 0
g_couple_number = 0

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
    
    def __init__(self, x, y, z, bRigid):
        global g_node_number
        g_node_number += 1
        self._id = g_node_number
        self._x = x
        self._y = y
        self._z = z
        self._bRigid = bRigid

    def LogToTxt(self, txt_file):
        txt_file.Write("%d  %.10f  %.10f  %.10f  1  %d \r\n" % (self._id, self._x, self._y, self._z, self._bRigid))

    def RotateNode(self, angle):
        alpha = angle*pi/180
        x = self._x*cos(alpha) - self._y*sin(alpha)
        y = self._x*sin(alpha) + self._y*cos(alpha)
        self._x = x
        self._y = y

class ElementItem(object):

    def __init__(self, node_1, node_2, section_no):
        global g_element_number
        g_element_number += 1
        self._id = g_element_number
        self._node_1 = node_1
        self._node_2 = node_2
        print "element:%d node1:%d node2:%d" %(self._id, self._node_1._id, self._node_2._id)
        self._section = section_no

    def LogToTxt(self, txt_file):
        txt_file.Write("%d  %d  %d  %d  1  %d  1 \r\n" % (self._id, self._id, self._node_1._id, self._node_2._id, self._section))

class SupportItem(object):

    def __init__(self, node, bx, by, bz=True):
        self._node = node
        self._bx = bx
        self._by = by
        self._bz = bz

    def LogToTxt(self, txt_file):
        txt_file.Write("%d  %d  %d  %d  0  0  0 \r\n" % (self._node._id, int(self._bx), int(self._by), int(self._bz)))

class CoupleItem(object):

    def __init__(self, node_1, node_2, type):
        global g_couple_number
        g_couple_number += 1
        self._id = g_couple_number
        self._node_1 = node_1
        self._node_2 = node_2
        self._type = 1

    def LogToTxt(self, txt_file):
        txt_file.Write("%d  %d  %d  %d \r\n" % (self._id, self._node_1._id, self._node_2._id, self._type))

class LoadItem(object):

    def __init__(self, node, load_x, load_y, load_z):
        self._node = node
        self._load_x = load_x
        self._load_y = load_y
        self._load_z = load_z

    def LogToTxt(self, txt_file):
        txt_file.Write("%d  %d  %d  %d \r\n" % (self._node._id, self._load_x, self._load_y, self._load_z))

