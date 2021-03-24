import math

class FPMFeed(object):

    def __init__(self, filename):
        self.fpmFile = open(filename,"wb")

    def __del__(self):
        if not self.fpmFile.closed:
            self.fpmFile.close()

    def Write(self, line):
        self.fpmFile.write(line)

    def Finished(self):
        self.fpmFile.write("/END/\r\n")
        self.fpmFile.close()


class NodeItem(object):

    def __init__(self, no, x, y, z):
        self._id = no
        self._x = x
        self._y = y
        self._z = z

    def LogToTxt(self, fpm_file):
        fpm_file.Write("%d, %.10f, %.10f, %.10f\r\n" % (self._id, self._x, self._y, self._z))

    def GetDir(self):
        length = math.sqrt(self._x*self._x + self._y*self._y + self._z*self._z)
        if length < 1E-15:
            return [0.0, 0.0, 0.0]
        else:
            return [self._x/length, self._y/length, self._z/length]

class CoupleItem(object):

    def __init__(self, node1, node2, dof, rdof):
        self._node1 = node1
        self._node2 = node2
        self._dof = dof
        self._rdof = rdof
        if dof is True:
            self._dx = 1
            self._dy = 1
            self._dz = 1
        else:
            self._dx = 0
            self._dy = 0
            self._dz = 0
        if rdof is True:
            self._rx = 1
            self._ry = 1
            self._rz = 1
        else:
            self._rx = 0
            self._ry = 0
            self._rz = 0     

    def LogToTxt(self, txt_file):
        dof_w = "%d, %d, %d" % (self._dx, self._dy, self._dz)
        rdof_w = "%d, %d, %d" % (self._rx, self._ry, self._rz)
        txt_file.Write("%s, %d, %s, %s \r\n" % (self._node1, self._node2, dof_w, rdof_w))

class ElementBaseItem(object):

    def __init__(self, elem_type, no, real_no, section_no, mat_no):
        self._type = elem_type
        self._id = no
        self._section = section_no
        self._real = real_no
        self._mat = mat_no
        self._node_str = ""

    def GetNodeStr(self):
        pass

    def LogToTxt(self, fpm_file):
        self.GetNodeStr()
        fpm_file.Write("%d, %s, %s, %d, %d, %d\r\n" % (self._id, self._type, self._node_str, self._real, self._section, self._mat))

class SupportItem(object):

    def __init__(self, group, node, dof, rdof):
        self._group = group
        self._node = node
        self._rdof = rdof
        self._k = [0,0,0,0,0,0]
        if dof is True:
            self._dx = 2
            self._dy = 2
            self._dz = 2
        else:
            self._dx = 0
            self._dy = 0
            self._dz = 0
        if rdof is True:
            self._rx = 2
            self._ry = 2
            self._rz = 2
        else:
            self._rx = 0
            self._ry = 0
            self._rz = 0     

    def JustZ(self):
        self._dx = 2
        self._dy = 2
        self._dz = 0

    def FreeDofs(self, dofs):
        for dof in dofs:
            if dof == 'x':
                self._dx = 0
            if dof == 'y':
                self._dy = 0
            if dof == 'z':
                self._dz = 0
            if dof == 'rx':
                self._rx = 0
            if dof == 'ry':
                self._ry = 0
            if dof == 'rz':
                self._rz = 0

    def LogToTxt(self, txt_file):
        dof_w = "%d, %d, %d" % (self._dx, self._dy, self._dz)
        rdof_w = "%d, %d, %d" % (self._rx, self._ry, self._rz)
        k_w = "%f, %f, %f, %f, %f, %f" % (self._k[0],self._k[1],self._k[2],self._k[3],self._k[4],self._k[5])
        txt_file.Write("%s, GENERAL, %d, %s, %s, %s\r\n" % (self._group, self._node, dof_w, rdof_w, k_w))

class LoadItem(object):

    def __init__(self, group,node, fx, fy, fz):
        self._group = group
        self._node = node
        self._fx = fx
        self._fy = fy
        self._fz = fz

    def LogToTxt(self, fpm_file):
        fpm_file.Write("%s, %d, %f, %f, %f\r\n" % (self._group, self._node, self._fx, self._fy, self._fz))