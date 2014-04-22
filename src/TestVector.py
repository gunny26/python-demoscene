#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import math

class TestVector(unittest.TestCase):

    testclass = Vector
    NullMatrix = Matrix3d(
            (0.000000, 0.000000, 0.000000, 0.000000),
            (0.000000, 0.000000, 0.000000, 0.000000),
            (0.000000, 0.000000, 0.000000, 0.000000),
            (0.000000, 0.000000, 0.000000, 0.000000),
        )

    def test_init(self):
        result = str(self.testclass(1, 2, 3, 1))
        self.assertEqual(result, "[1.000000, 2.000000, 3.000000, 1.000000]")

    def test_matrix(self):
        """basic matrix functions"""
        result = Utils3d.get_identity_matrix()
        identity = Utils3d.get_identity_matrix()
        #print "A:\n", result
        result *= 2
        #print "A*2:\n", result
        result += identity
        #print "A+I:\n", result

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
        # TODO: only nearly the same not equal
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
        print "v = ", vector
        result_1 = alt_basis_inv.mul_vec(vector)
        print "v1 = C⁻¹(v): ", result_1
        result_2 = alt_basis.mul_vec(result_1)
        print "v = C(v1)): ", result_2
        self.assertEqual(vector, result_2)
 
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
        #print "vector in standard basis", vector
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
        #print "vector in alternate basis: ", t
        # this should be nearly
        self.assertEqual(t, Vector(16, 16, 0, 1))

    def test_shift(self):
        """shift vector with transformation matrix"""
        vector = Vector(1, 0, 0, 1)
        # this should shift X Axis about 2
        shift_matrix = Utils3d.get_shift_matrix(2, 0, 0)
        # calculate linear transformation A*v
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
        self.assertEqual(obj.dot(self.testclass(1, 2, 3, 1)), 14)

    def test_cross(self):
        obj = self.testclass(1, 0, 0, 1)
        result = obj.cross(self.testclass(1, 0, 0, 1))
        self.assertEqual(result, self.testclass(0.000000, 0.000000, 0.000000, 1.000000))
        obj = self.testclass(1, 0, 0, 1)
        result = obj.cross(self.testclass(0, 1, 0, 1))
        self.assertEqual(result, self.testclass(0.000000, 0.000000, 1.000000, 1.000000))
        obj1 = self.testclass(-1, 1, 0, 1).unit()
        self.assertTrue( 1.0 - 1e-10 < obj1.length() < 1.0 + 1e-10)
        obj2 = self.testclass(1, 1, 0, 1).unit()
        self.assertTrue( 1.0 - 1e-10 < obj1.length() < 1.0 + 1e-10)
        result = obj1.cross(obj2)
        self.assertTrue(
                0.0 - 1e-10 < abs(result.length() - math.sin(math.pi/2)) < 0.0 + 1e-10)

    def test_rot_align(self):
        obj1 = self.testclass(1, 0, 0, 1)
        obj2 = self.testclass(0, 1, 0, 1)
        transformation = Utils3d.get_rot_align(obj1, obj2)
        print transformation
        result = transformation.mul_vec(obj1)
        print result
        self.assertEqual(result, obj2)

    def test_angle(self):
        # parallel vectors
        obj1 = self.testclass(1, 0, 0, 1)
        obj2 = self.testclass(1, 0, 0, 1)
        result = obj1.angle_to(obj2)
        # should be 0 degree
        self.assertEqual(result, 0.0)
        # create perpendicular vector
        obj1 = self.testclass(1, 0, 0, 1)
        obj2 = self.testclass(0, 1, 0, 1)
        cross = obj1.cross(obj2)
        result = obj1.angle_to(cross)
        # should be 90 degrees or pi/2
        self.assertEqual(result, math.pi/2)
        # two vectors in different directions
        obj1 = self.testclass(1, 0, 0, 1)
        obj2 = self.testclass(-1, 0, 0, 1)
        result = obj1.angle_to(obj2)
        # should be 180  degree
        self.assertEqual(result, math.pi)

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
