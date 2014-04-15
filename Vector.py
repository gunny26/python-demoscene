#!/usr/bin/python

import unittest
import math

class Vector(object):

    def __init__(self, *args):
        if len(args) == 3:
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


class Matrix3d(object):

    def __init__(self, *args):
        self.data = [0.0] * 16
        if len(args) == 4:
            self._set_column_vector(0, args[0])
            self._set_column_vector(1, args[1])
            self._set_column_vector(2, args[2])
            self._set_column_vector(3, args[3])

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

    def _set_column_vector(self, colnum, vector):
        counter = colnum
        for item in vector:
            self.data[counter] = item
            counter += 4

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


class TestVector(unittest.TestCase):

    testclass = Vector

    def test_init(self):
        result = str(self.testclass(1, 2, 3, 1))
        self.assertEqual(result, "[1.000000, 2.000000, 3.000000, 1.000000]")

    def test_matrix(self):
        result = Matrix3d()
        result = Utils3d.get_identity_matrix()
        identity = Utils3d.get_identity_matrix()
        print result
        result *= 2
        print result
        result += identity
        print result

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
