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
        return(self.x * other.x + self.y * other.y + self.z * other.z + self.h * other.h)

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

    @staticmethod
    def get_shift_matrix(x, y, z):
        """
        return transformation matrix to shift vector
        | 0  0  0  x|
        | 0  0  0  y|
        | 0  0  0  z|
        | 0  0  0  1|
        """
        return(Matrix3d(
            ( 1, 0, 0, 0),
            ( 0, 1, 0, 0),
            ( 0, 0, 1, 0),
            ( x, y, z, 1)
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

    def __getstate__(self):
        return(self.data)

    def __setstate__(self, data):
        self.data = data

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
        matrix = Matrix3d(self.__getstate__())
        for counter in range(16):
            matrix[counter] *= scalar
        return(matrix)

    def __imul__(self, scalar):
        """multiply matrix with scalar"""
        for counter in range(16):
            self.data[counter] *= scalar 
        return(self)

    def __div__(self, scalar):
        matrix = Matrix3d(self.__getstate__())
        for counter in range(16):
            matrix[counter] /= scalar
        return(matrix)

    def __idiv__(self, scalar):
        """multiply matrix with scalar"""
        for counter in range(16):
            self.data[counter] /= scalar 
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
        multiply self by matrix of same dimension (4x4)
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


    def determinant(self):
        """
        return determinant of self
        | 0   1  2  3 |
        | 4   5  6  7 |
        | 8   9 10 11 |
        | 12 13 14 15 |

        """
        # cross out a11
        det = self[0] * (
                self[5] * self[10] * self[15] +
                self[6] * self[11] * self[13] +
                self[7] * self[9]  * self[14])
        # cross out a12
        det += self[1] * (
                self[6] * self[11] * self[12] +
                self[7] * self[8]  * self[14] +
                self[4] * self[10] * self[15])
        # cross out a13
        det += self[2] * (
                self[7] * self[8] * self[13] +
                self[4] * self[9] * self[15] +
                self[5] * self[11] * self[12])
        # cross out a14
        det += self[3] * (
                self[4] * self[9] * self[14] +
                self[5] * self[10] * self[12] +
                self[6] * self[8] * self[13])
        # minus 
        # cross out a11
        det -= self[0] * (
                self[5] * self[11] * self[14] -
                self[6] * self[9] * self[15] -
                self[7] * self[10] * self[13])
        # cross out a12
        det -= self[1] * (
                self[6] * self[8] * self[15] -
                self[7] * self[10] * self[12] -
                self[4] * self[11] * self[14])
        # cross out a13
        det -= self[2] * (
                self[7] * self[9] * self[12] -
                self[4] * self[11] * self[14] -
                self[5] * self[8] * self[15])
        # cross out a14
        det -= self[3] * (
                self[4] * self[10] * self[13] -
                self[5] * self[8] * self[14] -
                self[6] * self[9] * self[12])
        return(float(det))

    def inverse(self):
        """
        return determinant of self
        | 0   1  2  3 |
        | 4   5  6  7 |
        | 8   9 10 11 |
        | 12 13 14 15 |

        http://www.mathsisfun.com/algebra/matrix-inverse-minors-cofactors-adjugate.html
        """
        det = self.determinant()
        if det != 0:
            adjugate = Matrix3d([
                # b11
                #  5  6  7
                #  9 10 11
                # 13 14 15
                self[5]  * self[10] * self[15] +
                self[6]  * self[11] * self[13] +
                self[7]  * self[9]  * self[14] -
                self[5]  * self[11] * self[14] -
                self[6]  * self[9]  * self[15] -
                self[7]  * self[10] * self[13]
                ,
                #b12
                #  4  5  6
                #  8 10 11
                # 12 14 15
                self[6]  * self[11] * self[12] +
                self[7]  * self[8]  * self[14] +
                self[4]  * self[10] * self[15] -
                self[6]  * self[8]  * self[15] -
                self[7]  * self[10] * self[12] -
                self[4]  * self[11] * self[14]
                ,
                #b13
                #  7  4  5
                # 11  8  9
                # 15 12 13
                self[7]  * self[8]  * self[13] +
                self[4]  * self[9]  * self[15] +
                self[5]  * self[11] * self[12] -
                self[7]  * self[9]  * self[12] -
                self[4]  * self[11] * self[13] -
                self[5]  * self[8]  * self[15]
                ,
                #b14
                #  4  5  6
                #  8  9 10
                # 12 13 14
                self[4]  * self[9]  * self[14] +
                self[5]  * self[10] * self[12] +
                self[6]  * self[8]  * self[13] -
                self[4]  * self[10] * self[13] -
                self[5]  * self[8]  * self[14] -
                self[6]  * self[9]  * self[12]
                ,
                #b21
                #  1  2  3
                #  9 10 11
                # 13 14 15
                self[1]  * self[10] * self[15] +
                self[2]  * self[11] * self[13] +
                self[3]  * self[9]  * self[14] -
                self[1]  * self[11] * self[14] -
                self[2]  * self[9]  * self[15] -
                self[3]  * self[10] * self[13]
                ,
                #b22
                #  0  2  3
                #  8 10 11
                # 12 14 15
                self[2]  * self[11] * self[12] +
                self[3]  * self[8]  * self[14] +
                self[0]  * self[10] * self[15] -
                self[2]  * self[8]  * self[15] -
                self[3]  * self[10] * self[12] -
                self[0]  * self[11] * self[14]
                ,
                #b23
                #  0  1  3
                #  4  9 11
                # 12 13 15
                self[3]  * self[8]  * self[14] +
                self[0]  * self[9]  * self[15] +
                self[1]  * self[11] * self[12] -
                self[3]  * self[9]  * self[12] -
                self[0]  * self[11] * self[13] -
                self[1]  * self[8]  * self[15]
                ,
                #b24
                #  0  1  2
                #  8  9 10
                # 12 13 14
                self[0]  * self[9]  * self[14] +
                self[1]  * self[10] * self[12] +
                self[2]  * self[8]  * self[13] -
                self[0]  * self[10] * self[13] -
                self[1]  * self[8]  * self[14] -
                self[2]  * self[9]  * self[12]
                ,
                #b31
                #  1  2  3
                #  5  6  7
                # 13 14 15
                self[1]  * self[6]  * self[15] +
                self[2]  * self[7]  * self[13] +
                self[3]  * self[5]  * self[14] -
                self[1]  * self[7]  * self[14] -
                self[2]  * self[5]  * self[15] -
                self[3]  * self[6]  * self[13]
                ,
                #b32
                #  0  2  3
                #  4  6  7
                # 12 14 15
                self[0]  * self[6]  * self[15] +
                self[2]  * self[7]  * self[12] +
                self[3]  * self[4]  * self[14] -
                self[0]  * self[7]  * self[14] -
                self[2]  * self[4]  * self[15] -
                self[3]  * self[6]  * self[12]
                ,
                #b33
                #  0  1  3
                #  4  5  7
                # 12 13 15
                self[0]  * self[5]  * self[15] +
                self[1]  * self[7]  * self[12] +
                self[3]  * self[4]  * self[13] -
                self[0]  * self[7]  * self[13] -
                self[1]  * self[4]  * self[15] -
                self[3]  * self[5]  * self[12]
                ,
                #b34
                #  0  1  2
                #  4  5  6
                # 12 13 14
                self[0]  * self[5]  * self[14] +
                self[1]  * self[6]  * self[12] +
                self[2]  * self[4]  * self[13] -
                self[0]  * self[6]  * self[13] -
                self[1]  * self[4]  * self[14] -
                self[2]  * self[5]  * self[12]
                ,
                #b41
                #  1  2  3
                #  5  6  7
                #  9 10 11
                self[1]  * self[6]  * self[11] +
                self[2]  * self[7]  * self[9] +
                self[3]  * self[5]  * self[10] -
                self[1]  * self[7]  * self[10] -
                self[2]  * self[5]  * self[11] -
                self[3]  * self[6]  * self[9]
                ,
                #b42
                #  2  3  0
                #  6  7  4
                # 10 11  8
                self[2]  * self[7]  * self[4] +
                self[3]  * self[4]  * self[10] +
                self[0]  * self[6]  * self[11] -
                self[2]  * self[4]  * self[11] -
                self[3]  * self[6]  * self[8] -
                self[0]  * self[7]  * self[10]
                ,
                #b43
                #  3  0  1
                #  7  4  5
                # 11  8  9
                self[3]  * self[4]  * self[9] +
                self[0]  * self[5]  * self[11] +
                self[1]  * self[7]  * self[8] -
                self[3]  * self[5]  * self[8] -
                self[0]  * self[7]  * self[9] -
                self[1]  * self[4]  * self[11]
                ,
                #b44
                #  0  1  2
                #  4  5  6
                #  8  9 10
                self[0]  * self[5]  * self[10] +
                self[1]  * self[6]  * self[8] +
                self[2]  * self[4]  * self[9] -
                self[0]  * self[6]  * self[9] -
                self[1]  * self[4]  * self[10] -
                self[2]  * self[5]  * self[8]
                ])
            # print adjugate
            return(adjugate / det)
        raise(StandarError("Determinant is Zero"))


class TestVector(unittest.TestCase):

    testclass = Vector

    NullMatrix = Matrix3d((0.000000, 0.000000, 0.000000, 0.000000),(0.000000, 0.000000, 0.000000, 0.000000),(0.000000, 0.000000, 0.000000, 0.000000),(0.000000, 0.000000, 0.000000, 0.000000),)

    def test_init(self):
        result = str(self.testclass(1, 2, 3, 1))
        self.assertEqual(result, "[1.000000, 2.000000, 3.000000, 1.000000]")

    def test_matrix(self):
        """basic matrix functions"""
        result = Utils3d.get_identity_matrix()
        identity = Utils3d.get_identity_matrix()
        print "A:\n", result
        result *= 2
        print "A*2:\n", result
        result += identity
        print "A+I:\n", result

    def test_determinant(self):
        identity = Utils3d.get_identity_matrix()
        det = identity.determinant()
        #print "Determinant of Identity Matrix: ", det
        self.assertEqual(det, 1.0)
        matrix = Matrix3d(
            Vector(1, 0, 0, 0),
            Vector(0, 2, 0, 0),
            Vector(0, 0, 3, 0),
            Vector(0, 0, 0, 1))
        det = matrix.determinant()
        #print "Determinant of test matrix: ", det
        self.assertEqual(det, 6.0)
        inv = matrix.inverse()
        #print "Inverse of test matrix:\n", inv
        #self.assertEqual(inv, Matrix3d(
        #    Vector(1, 0, 0, 0),
        #    Vector(0, 0.5, 0, 0),
        #    Vector(0, 0, 1.0/3.0, 0),
        #    Vector(0, 0, 0, 1)))

    def test_change_of_basis(self):
        vector = Vector(16, 9, 0, 1)
        identiy = Utils3d.get_identity_matrix()
        rot_z = Utils3d.get_rot_z_matrix(1)
        y_ratio = 16.0/9.0
        alt_basis = Matrix3d(
            Vector(1, 0, 0, 0),
            Vector(0, y_ratio, 0, 0),
            Vector(0, 0, 1, 0),
            Vector(0, 0, 0, 1))
        alt_basis_inv = alt_basis.inverse()
        # these two vectors should be the same
        result_1 = alt_basis_inv.mul_vec(rot_z.mul_vec(vector))
        print "C⁻¹(T(v)): ", result_1
        result_2 = rot_z.mul_vec(alt_basis_inv.mul_vec(vector))
        print "T(C⁻¹(v)): ", result_2
 
    def test_rotation(self):
        """test rotation transformation"""
        # original vector point to 0 degree in X-Y coordinates
        vector = Vector(1, 0, 0, 1)
        # print "Original Vector", vector
        identity = Utils3d.get_identity_matrix()
        # should rotate about math.pi = 180 degrees on X-Y Plane counter-clockwise
        # so we need Rotation Matrix around Z-axis
        rot_x = Utils3d.get_rot_z_matrix(math.pi)
        # print "Rotation matrix: \n", rot_x
        t = rot_x.mul_vec(vector)
        # print "Rotated vector: ", t
        self.assertEqual(t.length(), 1)
        # this is maybe not exactly equal
        self.assertTrue(-1.0-1e10 < t.x < -1+1e10)
        self.assertTrue(0.0-1e10 < t.y < 0+1e10)
        self.assertTrue(0.0-1e10 < t.z < 0+1e10)
        self.assertTrue(1.0-1e10 < t.h < 1+1e10)

    def test_basis(self):
        """test change of basis transformations"""
        vector = Vector(16, 9, 0, 1)
        print "vector in standard basis", vector
        # alternate basis Matrix,
        # represent 16:9 aspect ration
        y_ratio = 16.0/9.0
        basis = Matrix3d(
            Vector(1, 0, 0, 0),
            Vector(0, y_ratio, 0, 0),
            Vector(0, 0, 1, 0),
            Vector(0, 0, 0, 1))
        # represent  vector with respect to basis alt_basis
        basis_inv = basis.inverse()
        t = basis.mul_vec(vector)
        print "vector in alternate basis: ", t
        # this should be nearly
        self.assertEqual(t, Vector(16, 16, 0, 1))

    def test_shift(self):
        """shift vector with transformation matrix"""
        vector = Vector(1, 0, 0, 1)
        # this should shift X Axis about 2
        shift_matrix = Utils3d.get_shift_matrix(2, 0, 0)
        # calucalte linear transformation A*v
        t = shift_matrix.mul_vec(vector)
        # result should be shifted about 2 on x-axis
        self.assertEqual(t, Vector(3, 0, 0, 1))

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
        self.assertEqual(obj.dot(self.testclass(1, 2, 3, 1)), 15)

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
