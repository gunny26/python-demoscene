#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import math
# own modules
from Vector import Vector as Vector
from Matrix3d import Matrix3d as Matrix3d
import Utils3d
from Polygon import Polygon as Polygon

class TestVector(unittest.TestCase):

    def test_init(self):
        result = str(Vector.from_tuple(1, 2, 3))
        self.assertEqual(result, "[ 1.  2.  3.]")

    def test_matrix(self):
        """basic matrix functions"""
        result = Utils3d.get_identity_matrix()
        identity = Utils3d.get_identity_matrix()
        result *= 2
        print "__imul__(2):\n", result
        result /= 2
        print "__idiv__(2):\n", result 
        result += identity
        print "__iadd__(eye):\n", result
        print "__mul__(2):\n", result * 2
        print "__div__(2):\n", result / 2
        print "__add__(eye):\n", result + identity


    def test_determinant(self):
        identity = Utils3d.get_identity_matrix()
        det = identity.determinant()
        #print "Determinant of Identity Matrix: ", det
        self.assertEqual(det, 1.0)
        matrix = Matrix3d.from_row_vectors(
            Vector.from_tuple(1, 0, 0),
            Vector.from_tuple(0, 2, 0),
            Vector.from_tuple(0, 0, 3))
        det = matrix.determinant()
        #print "Determinant of test matrix: ", det
        self.assertEqual(det, 6.0)
        inv = matrix.inverse()

    def test_change_of_basis(self):
        vector = Vector.from_tuple(16, 9, 0)
        identiy = Utils3d.get_identity_matrix()
        rot_z = Utils3d.get_rot_z_matrix(1)
        y_ratio = 16.0/9.0
        alt_basis = Matrix3d.from_row_vectors(
            Vector.from_tuple(1, 0, 0),
            Vector.from_tuple(0, y_ratio, 0),
            Vector.from_tuple(0, 0, 1))
        alt_basis_inv = alt_basis.inverse()
        # these two vectors should be the same
        #print "v = ", vector
        result_1 = alt_basis_inv.mul_vec(vector)
        #print "v1 = C⁻¹(v): ", result_1
        result_2 = alt_basis.mul_vec(result_1)
        #print "v = C(v1)): ", result_2
        self.assertEqual(vector, result_2)
 
    def test_rotation(self):
        """test rotation transformation"""
        # original vector point to 0 degree in X-Y coordinates
        vector = Vector.from_tuple(1, 0, 0)
        # print "Original Vector.from_tuple", vector
        identity = Utils3d.get_identity_matrix()
        # should rotate about math.pi = 180 degrees on X-Y Plane counter-clockwise
        # so we need Rotation Matrix around Z-axis
        rot_x = Utils3d.get_rot_z_matrix(math.pi)
        # print "Rotation matrix: \n", rot_x
        t = rot_x.mul_vec(vector)
        # print "Rotated vector: ", t
        self.assertEqual(t.length(), 1)
        # this is maybe not exactly equal
        self.assertTrue(-1.0-1e10 < t[0] < -1+1e10)
        self.assertTrue(0.0-1e10 < t[1] < 0+1e10)
        self.assertTrue(0.0-1e10 < t[2] < 0+1e10)

    def test_basis(self):
        """test change of basis transformations"""
        vector = Vector.from_tuple(16, 9, 0)
        #print "vector in standard basis", vector
        # alternate basis Matrix,
        # represent 16:9 aspect ration
        y_ratio = 16.0/9.0
        basis = Matrix3d.from_row_vectors(
            Vector.from_tuple(1.0, 0.0, 0.0),
            Vector.from_tuple(0.0, y_ratio, 0.0),
            Vector.from_tuple(0.0, 0.0, 1.0))
        print "Basis:\n", basis
        # represent  vector with respect to basis alt_basis
        basis_inv = basis.inverse()
        t = basis.mul_vec(vector)
        #print "vector in alternate basis: ", t
        # this should be nearly
        self.assertEqual(t, Vector.from_tuple(16, 16, 0))

    def test_shift(self):
        """shift vector with transformation matrix"""
        vector = Vector.from_tuple(1, 0, 0)
        # this should shift X Axis about 2
        shift_vector = Utils3d.get_shift_vector(2, 0, 0)
        # calculate linear transformation A*v
        t = shift_vector + vector
        # result should be shifted about 2 on x-axis
        self.assertEqual(t, Vector.from_tuple(3, 0, 0))

    def test_projection(self):
        obj = Vector.from_tuple(1, 2, 3)
        result = Utils3d.project(obj, 800, 600, 1, 1)
        #print result

    def test_normlization(self):
        obj = Vector.from_tuple(5, 0, 0)
        self.assertEqual(obj.normalized(), Vector.from_tuple(1.0, 0.0, 0.0))
        self.assertEqual(obj.normalized().length(), 1.0)

    def test_list_behavior(self):
        obj = Vector.from_tuple(1, 2, 3)
        self.assertEqual(len(obj), 3)
        self.assertEqual(obj[0], 1.0)
        self.assertEqual(obj[1], 2.0)
        self.assertEqual(obj[2], 3.0)
        obj[0] = 2
        obj[1] = 4
        obj[2] = 6
        self.assertEqual(obj, Vector.from_tuple(2, 4, 6))
        counter = 0
        for axis in obj:
            self.assertEqual(axis, obj[counter])
            counter += 1

    def test_length(self):
        obj = Vector.from_tuple(1, 0, 0)
        self.assertEqual(obj.length(), 1)
        obj = Vector.from_tuple(0, 0, 0)
        self.assertEqual(obj.length(), 0.0)
        obj = Vector.from_tuple(1, 1, 1)
        self.assertEqual(obj.length(), math.sqrt(3.0))
        self.assertEqual(obj.length_sqrd(), 3.0)

    def test_dot(self):
        obj = Vector.from_tuple(1, 2, 3)
        self.assertEqual(obj.dot(Vector.from_tuple(1, 2, 3)), 14)

    def test_cross(self):
        obj = Vector.from_tuple(1, 0, 0)
        result = obj.cross(Vector.from_tuple(1, 0, 0))
        self.assertEqual(result, Vector.from_tuple(0.000000, 0.000000, 0.000000))
        obj = Vector.from_tuple(1, 0, 0)
        result = obj.cross(Vector.from_tuple(0, 1, 0))
        self.assertEqual(result, Vector.from_tuple(0.000000, 0.000000, 1.000000))
        obj1 = Vector.from_tuple(-1, 1, 0).unit()
        self.assertEqual(obj1.length(), 1.)
        obj2 = Vector.from_tuple(1, 1, 0).unit()
        self.assertEqual(obj1.length(), 1.)
        result = obj1.cross(obj2)
        self.assertEqual(abs(result.length() - math.sin(math.pi/2)), 0.)

    def test_rot_align(self):
        obj1 = Vector.from_tuple(1, 0, 0)
        obj2 = Vector.from_tuple(0, 1, 0)
        transformation = Utils3d.get_rot_align(obj1, obj2)
        #print transformation
        result = transformation.mul_vec(obj1)
        #print result
        self.assertEqual(result, obj2)

    def test_angle(self):
        # parallel vectors
        obj1 = Vector.from_tuple(1, 0, 0)
        obj2 = Vector.from_tuple(1, 0, 0)
        result = obj1.angle_to(obj2)
        # should be 0 degree
        self.assertEqual(result, 0.0)
        # create perpendicular vector
        obj1 = Vector.from_tuple(1, 0, 0)
        obj2 = Vector.from_tuple(0, 1, 0)
        cross = obj1.cross(obj2)
        result = obj1.angle_to(cross)
        # should be 90 degrees or pi/2
        self.assertEqual(result, math.pi/2)
        # two vectors in different directions
        obj1 = Vector.from_tuple(1, 0, 0)
        obj2 = Vector.from_tuple(-1, 0, 0)
        result = obj1.angle_to(obj2)
        # should be 180  degree
        self.assertEqual(result, math.pi)

    def test_eq(self):
        obj1 = Vector.from_tuple(1, 2, 3)
        obj2 = Vector.from_tuple(1, 2, 3)
        self.assertEqual(obj1, obj2)
        self.assertEqual(obj2, obj1)

    def test_add(self):
        result = Vector.from_tuple(1, 2, 3) + Vector.from_tuple(1, 2, 3)
        self.assertEqual(result, Vector.from_tuple(2.000000, 4.000000, 6.000000))

    def test_iadd(self):
        result = Vector.from_tuple(1, 2, 3) 
        result += Vector.from_tuple(1, 2, 3)
        self.assertEqual(result, Vector.from_tuple(2.000000, 4.000000, 6.000000))

    def test_sub(self):
        result = Vector.from_tuple(1, 2, 3) - Vector.from_tuple(1, 2, 3)
        self.assertEqual(result, Vector.from_tuple(0.000000, 0.000000, 0.000000))

    def test_isub(self):
        result = Vector.from_tuple(1, 2, 3) 
        result -= Vector.from_tuple(1, 2, 3)
        self.assertEqual(result, Vector.from_tuple(0.000000, 0.000000, 0.000000))

    def test_mul(self):
        result = Vector.from_tuple(1, 2, 3) * 2
        self.assertEqual(result, Vector.from_tuple(2.000000, 4.000000, 6.000000))

    def test_imul(self):
        result = Vector.from_tuple(1, 2, 3) 
        result *= 2
        self.assertEqual(result, Vector.from_tuple(2.000000, 4.000000, 6.000000))

    def test_div(self):
        result = Vector.from_tuple(2, 4, 6) / 2
        self.assertEqual(result, Vector.from_tuple(1.000000, 2.000000, 3.000000))

    def test_idiv(self):
        result = Vector.from_tuple(2, 4, 6) 
        result /= 2
        self.assertEqual(result, Vector.from_tuple(1.000000, 2.000000, 3.000000))


if __name__ == "__main__":
    unittest.main()
