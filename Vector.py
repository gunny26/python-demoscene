#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import math

class Vector(object):

    def __init__(self, *args):
        if len(args) == 1 and hasattr(args[0], "__getitem__"):
            if len(args[0]) == 4:
                self.x = args[0][0]
                self.y = args[0][1]
                self.z = args[0][2]
                self.h = args[0][3]
            elif len(args[0]) == 3:
                self.x = args[0][0]
                self.y = args[0][1]
                self.z = args[0][2]
                self.h = 0.0
        elif len(args) == 3:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
            self.h = 0
        elif len(args) == 4:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
            self.h = args[3]
        else:
            self.x = 0.0
            self.y = 0.0
            self.z = 0.0
            self.h = 0.0

    def __len__(self):
        """list interface"""
        return(4)

    def __getitem__(self, key):
        """list interface"""
        if key == 0:
            return(self.x)
        elif key == 1:
            return(self.y)
        elif key == 2:
            return(self.z)
        elif key == 3:
            return(self.h)
        else:
            raise(IndexError("Invalid index %d to Vector" % key))

    def __setitem__(self, key, value):
        """list interface"""
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        elif key == 3:
            self.h = value
        else:
            raise(IndexError("Invalid index %d to Vector" % key))

    def __repr__(self):
        """object representation"""
        return("Vector(%(x)f, %(y)f, %(z)f, %(h)f)" % self.__dict__)

    def __str__(self):
        """string output"""
        return("[%(x)f, %(y)f, %(z)f, %(h)f]" % self.__dict__)

    def __add__(self, other):
        """vector addition with another Vector class"""
        return(Vector(self.x + other.x, self.y + other.y, self.z + other.z, self.h))

    def __iadd__(self, other):
        """vector addition with another Vector class implace"""
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return(self)

    def __sub__(self, other):
        """vector addition with another Vector class"""
        return(Vector(self.x - other.x, self.y - other.y, self.z - other.z, self.h))

    def __isub__(self, other):
        """vector addition with another Vector class implace"""
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return(self)

    def __eq__(self, other):
        """test for euqality"""
        return(self.x == other.x and self.y == other.y and self.z == other.z and self.h == other.h)

    def __ne__(self, other):
        """test for ineuqality"""
        return(self.x != other.x or self.y != other.y or self.z != other.z or self.h != other.h)

    def __nonzero__(self):
        """test if nonzero"""
        return(self.x or self.y or self.z or self.h)

    def __mul__(self, scalar):
        """multiplication with scalar"""
        return(Vector(self.x * scalar, self.y * scalar, self.z * scalar, self.h))

    def __imul__(self, scalar):
        """multiplication with scalar inplace"""
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        return(self)

    def __div__(self, scalar):
        """division with scalar"""
        return(Vector(self.x / scalar, self.y / scalar, self.z / scalar, self.h))

    def __idiv__(self, scalar):
        """vector addition with another Vector class"""
        self.x /= scalar
        self.y /= scalar
        self.z /= scalar
        return(self)

    def length(self):
        """length"""
        return(math.sqrt(self.x **2 + self.y ** 2 + self.z ** 2))

    def length_sqrd(self):
        """length squared"""
        return(self.x **2 + self.y ** 2 + self.z ** 2)

    def dot(self, other):
        """dot product of self and other vector"""
        return(self.x * other.x + self.y * other.y + self.z * other.z)

    def cross(self, other):
        """cross product of self an other vector"""
        return(Vector(self.y * other.z - self.z * other.y, 
            self.z * other.x - self.x * other.z, 
            self.x * other.y - self.y * other.x, 
            self.h))

    def normalized(self):
        return(self / self.length())


class Utils3d(object):

    @staticmethod
    def project(vec1, win_width, win_height, fov, viewer_distance):
        factor = fov / (viewer_distance + vec1.z)
        x = vec1.x * factor + win_width / 2
        y = -vec1.y * factor + win_height / 2
        return(Vector(x, y, 1, vec1.h))

    @staticmethod
    def get_identity_matrix():
        return(Matrix3d(
            (1, 0, 0, 0),
            (0, 1, 0, 0),
            (0, 0, 1, 0),
            (0, 0, 0, 1)))

    @staticmethod
    def get_rot_x_matrix(theta):
        """return rotation matrix around x axis
        return rotated version of self around X-Axis
        theta should be given in radians
        http://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
        |1     0           0| |x|   |        x        |   |x'|
        |0   cos θ    -sin θ| |y| = |y cos θ - z sin θ| = |y'|
        |0   sin θ     cos θ| |z|   |y sin θ + z cos θ|   |z'|
        """
        cos = math.cos(theta)
        sin = math.sin(theta)
        return(Matrix3d(
            (1,    0,   0, 0),
            (0,  cos, sin, 0),
            (0, -sin, cos, 0),
            (0,    0,   0, 1)))

    @staticmethod
    def get_rot_z_matrix(theta):
        """
        return rotated version of self around Z-Axis
        theta should be given in radians
        http://stackoverflow.com/questions/1 4607640/rotating-a-vector-in-3d-space
        |cos θ   -sin θ   0| |x|   |x cos θ - y sin θ|   |x'|
        |sin θ    cos θ   0| |y| = |x sin θ + y cos θ| = |y'|
        |  0       0      1| |z|   |        z        |   |z'|
        """
        cos = math.cos(theta)
        sin = math.sin(theta)
        return(Matrix3d(
            (cos, -sin, 0, 0),
            (sin,  cos, 0, 0),
            (  0,    0, 0, 0),
            (  0,    0, 0, 1)))

    @staticmethod
    def get_rot_y_matrix(theta):
        """
        return rotated version of self around Y-Axis
        theta should be given in radians
        http://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
        | cos θ    0   sin θ| |x|   | x cos θ + z sin θ|   |x'|
        |     0    1       0| |y| = |         y        | = |y'|
        |-sin θ    0   cos θ| |z|   |-x sin θ + z cos θ|   |z'|
        """
        cos = math.cos(theta)
        sin = math.sin(theta)
        return(Matrix3d(
            ( cos, 0, sin, 0),
            (   0, 1,   0, 0),
            (-sin, 0, cos, 0),
            (   0, 0,   0, 1)
            ))


class Matrix3d(object):

    def __init__(self, *args):
        self.data = [0.0] * 16
        if len(args) == 4:
            self._set_col_vector(0, args[0])
            self._set_col_vector(1, args[1])
            self._set_col_vector(2, args[2])
            self._set_col_vector(3, args[3])
        elif len(args) == 16:
            self.data = args
        elif len(args) == 1 and hasattr(args[0], "__getitem__"):
            self.data = args[0]

    def __repr__(self):
        sb = "Matrix3d("
        for row in range(4):
            startindex = row * 4
            sb += "(%f, %f, %f, %f)," % (
                self.data[startindex], 
                self.data[startindex+1], 
                self.data[startindex+2], 
                self.data[startindex+3])
        sb += ")"
        return(sb)

    def __str__(self):
        sb = ""
        for row in range(4):
            startindex = row * 4
            sb += "| %f, %f, %f, %f|\n" % (
                self.data[startindex], 
                self.data[startindex+1], 
                self.data[startindex+2], 
                self.data[startindex+3])
        return(sb)

    def __getitem__(self, key):
        return(self.data[key])

    def __setitem__(self, key, value):
        self.data[key] = value

    def _set_col_vector(self, colnum, vector):
        counter = colnum
        for item in vector:
            self.data[counter] = item
            counter += 4

    def _get_col_vector(self, colnum):
        """return column vector as Vector object"""
        return(Vector(self.data[colnum::4]))

    def _set_row_vector(self, rownum, vector):
        """set row with data from vector"""
        self.data[rownum*4] = vector[0]
        self.data[rownum*4+1] = vector[1]
        self.data[rownum*4+2] = vector[2]
        self.data[rownum*4+3] = vector[3]

    def _get_row_vector(self, rownum):
        return(Vector(self.data[rownum*4: rownum*4+4]))

    def __mul__(self, scalar):
        matrix = self.copy()
        for counter in range[16]:
            matrix[counter] *= scalar
        return(matrix)

    def __imul__(self, scalar):
        """multiply matrix with scalar"""
        for counter in range(16):
            self.data[counter] *= scalar 
        return(self)

    def __add__(self, other):
        matrix = self.copy()
        for counter in range[16]:
            matrix[counter] += other[counter]
        return(matrix)

    def __iadd__(self, other):
        """add two matrices"""
        for counter in range(16):
            self.data[counter] += other[counter]
        return(self)

    def mul_vec(self, vector):
        """
        multiply self with vector
        return type is vector

        multiply 4x4 with 4x1 = 4x1
        """
        return(Vector(
            self._get_row_vector(0).dot(vector),
            self._get_row_vector(1).dot(vector),
            self._get_row_vector(2).dot(vector),
            self._get_row_vector(3).dot(vector)))

    def mul_matrix(self, other):
        """
        multiply matrix by matrix
        only defined for matrices with specific row an column number

        n x k multiplied by k x n is defined
        n x n multiplied by n x n is also defined
        | a11 a12 a13 a24 |   | b11 b12 b13 b14 |     | rowa1 . colb1  
        | a21 a22 a23 a24 | * | b21 b22 b23 b24 | =>  | r2 | * v1 => 
        | a31 a32 a33 a34 |   | b31 b32 b33 b34 |     | r3 |
        | a41 a42 a43 a44 |   | b41 b42 b43 b44 |     | r4 |
        """
        data = [0.0] * 16
        for row in range(4):
            vec_data = [0.0] * 4
            for col in range(4):
                data[row*4 + col] = self._get_row_vector(row).dot(other._get_col_vector(col))
        return(Matrix3d(data))

            


class TestVector(unittest.TestCase):

    testclass = Vector

    NullMatrix = Matrix3d((0.000000, 0.000000, 0.000000, 0.000000),(0.000000, 0.000000, 0.000000, 0.000000),(0.000000, 0.000000, 0.000000, 0.000000),(0.000000, 0.000000, 0.000000, 0.000000),)

    def test_init(self):
        result = str(self.testclass(1, 2, 3, 1))
        self.assertEqual(result, "[1.000000, 2.000000, 3.000000, 1.000000]")

    def test_matrix(self):
        result = Utils3d.get_identity_matrix()
        identity = Utils3d.get_identity_matrix()
        print "A:\n", result
        result *= 2
        print "A*2:\n", result
        result += identity
        print "A+I:\n", result
        rot_x = Utils3d.get_rot_x_matrix(1)
        print "R:\n", rot_x
        print "R Column Vector 1:\n", rot_x._get_col_vector(1)
        print "R RowVector 2:\n", rot_x._get_row_vector(2)
        print "I * R :\n", identity.mul_matrix(rot_x)
        print "R * I :\n", rot_x.mul_matrix(identity)
        degree = math.pi/180
        t = Utils3d.get_rot_x_matrix(degree)
        t = t.mul_matrix(Utils3d.get_rot_z_matrix(degree))
        t = t.mul_matrix(Utils3d.get_rot_y_matrix(degree))
        print "T : \n", t
        v = Vector(1, 0, 0, 0)
        for i in range(5):
            v = t.mul_vec(v)
            print "V : ", v
            print "V.length() : ", v.length()

    def test_projection(self):
        obj = self.testclass(1, 2, 3, 1)
        result = Utils3d.project(obj, 800, 600, 1, 1)
        print result

    def test_normlization(self):
        obj = self.testclass(5, 0, 0, 1)
        self.assertEqual(obj.normalized(), Vector(1.0, 0.0, 0.0, 1.000000))
        self.assertEqual(obj.normalized().length(), 1.0)

    def test_list_behavior(self):
        obj = self.testclass(1, 2, 3, 1)
        self.assertEqual(len(obj), 4)
        self.assertEqual(obj[0], 1.0)
        self.assertEqual(obj[1], 2.0)
        self.assertEqual(obj[2], 3.0)
        self.assertEqual(obj[3], 1.0)
        obj[0] = 2
        obj[1] = 4
        obj[2] = 6
        obj[3] = 0
        self.assertEqual(obj, Vector(2, 4, 6, 0))
        counter = 0
        for axis in obj:
            self.assertEqual(axis, obj[counter])
            counter += 1

    def test_length(self):
        obj = self.testclass(1, 0, 0, 1)
        self.assertEqual(obj.length(), 1)
        obj = self.testclass(0, 0, 0, 1)
        self.assertEqual(obj.length(), 0.0)
        obj = self.testclass(1, 1, 1, 1)
        self.assertEqual(obj.length(), math.sqrt(3.0))
        self.assertEqual(obj.length_sqrd(), 3.0)

    def test_dot(self):
        obj = self.testclass(1, 2, 3, 1)
        self.assertEqual(obj.dot(self.testclass(1, 2, 3, 1)), 14)

    def test_cross(self):
        obj = self.testclass(1, 0, 0, 1)
        result = obj.cross(self.testclass(1, 0, 0, 1))
        self.assertEqual(result, self.testclass(0.000000, 0.000000, 0.000000, 1.000000))
        obj = self.testclass(1, 0, 0, 1)
        result = obj.cross(self.testclass(0, 1, 0, 1))
        self.assertEqual(result, self.testclass(0.000000, 0.000000, 1.000000, 1.000000))

    def test_eq(self):
        obj1 = self.testclass(1, 2, 3, 1)
        obj2 = self.testclass(1, 2, 3, 1)
        self.assertEqual(obj1, obj2)
        self.assertEqual(obj2, obj1)

    def test_add(self):
        result = self.testclass(1, 2, 3, 1) + self.testclass(1, 2, 3, 1)
        self.assertEqual(result, self.testclass(2.000000, 4.000000, 6.000000, 1.000000))

    def test_iadd(self):
        result = self.testclass(1, 2, 3, 1) 
        result += self.testclass(1, 2, 3, 1)
        self.assertEqual(result, self.testclass(2.000000, 4.000000, 6.000000, 1.000000))

    def test_sub(self):
        result = self.testclass(1, 2, 3, 1) - self.testclass(1, 2, 3, 1)
        self.assertEqual(result, self.testclass(0.000000, 0.000000, 0.000000, 1.000000))

    def test_isub(self):
        result = self.testclass(1, 2, 3, 1) 
        result -= self.testclass(1, 2, 3, 1)
        self.assertEqual(result, self.testclass(0.000000, 0.000000, 0.000000, 1.000000))

    def test_mul(self):
        result = self.testclass(1, 2, 3, 1) * 2
        self.assertEqual(result, self.testclass(2.000000, 4.000000, 6.000000, 1.000000))

    def test_imul(self):
        result = self.testclass(1, 2, 3, 1) 
        result *= 2
        self.assertEqual(result, self.testclass(2.000000, 4.000000, 6.000000, 1.000000))

    def test_div(self):
        result = self.testclass(2, 4, 6, 1) / 2
        self.assertEqual(result, self.testclass(1.000000, 2.000000, 3.000000, 1.000000))

    def test_idiv(self):
        result = self.testclass(2, 4, 6, 1) 
        result /= 2
        self.assertEqual(result, self.testclass(1.000000, 2.000000, 3.000000, 1.000000))


if __name__ == "__main__":
    unittest.main()
