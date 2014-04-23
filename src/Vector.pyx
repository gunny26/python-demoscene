#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
cimport numpy as np
DTYPE = np.float32
ctypedef np.float32_t DTYPE_d

cdef class Vector(object):

    cdef np.ndarray data
    cdef public double x
    cdef public double y
    cdef public double z
    cdef public double h

    def __init__(self, double x, double y, double z, double h=1):
        self.data = np.ndarray([x, y, z, h], dtype=DTYPE)
        #self.x = self.data[0]
        #self.y = self.data[1]
        #self.z = self.data[2]
        #self.h = self.data[3]

    @classmethod
    def from_tuple4(cls, data):
        return(cls(data[0], data[1], data[2], data[3]))

    @classmethod
    def from_tuple3(cls, data):
        return(cls(data[0], data[1], data[2], 1))

    def __len__(self):
        """list interface"""
        return(4)

    def __getitem__(self, int key):
        """list interface"""
        return(self.data[key])

    def __setitem__(self, int key, double value):
        """list interface"""
        self.data[key] = value

    def __repr__(self):
        """object representation"""
        return("%s(%f, %f, %f, %f)" % (self.__class__.__name__, self.data[0], self.data[1], self.data[2], self.data[3]))

    def __str__(self):
        """string output"""
        return("[%f, %f, %f, %f]" % (self.data[0], self.data[1], self.data[2], self.data[3]))

    def __add__(self, object other):
        """vector addition with another Vector class"""
        result = self.data + other.data
        return(Vector(result))

    def __iadd__(self, object other):
        """vector addition with another Vector class implace"""
        self.data = self.data + other.data
        return(self)

    def __sub__(self, object other):
        """vector addition with another Vector class"""
        result = self.data - other.data
        return(Vector(result))

    def __isub__(self, object other):
        """vector addition with another Vector class implace"""
        self.data = self.data - other.data
        return(self)

    def __richcmp__(self, object other, int method):
        if method == 0: # < __lt__
            pass
        elif method == 2: # == __eq__
            return(self.data == other.data)
        elif method == 4: # > __gt__
            pass
        elif method == 1: # <= lower_equal
            pass
        elif method == 3: # != __ne__
            return(self.data != other.data)
        elif method == 5: # >= greater equal
            pass
            
    def __mul__(self, double scalar):
        """multiplication with scalar"""
        return(Vector(self.data[0] * scalar, self.data[1] * scalar, self.data[2] * scalar, self.data[3]))

    def __imul__(self, double scalar):
        """multiplication with scalar inplace"""
        self.data[0] *= scalar
        self.data[1] *= scalar
        self.data[2] *= scalar
        return(self)

    def __div__(self, double scalar):
        """division with scalar"""
        return(Vector(self.data[0] / scalar, self.data[1] / scalar, self.data[2] / scalar, self.data[3]))

    def __idiv__(self, double scalar):
        """vector addition with another Vector class"""
        self.data[0] /= scalar
        self.data[1] /= scalar
        self.data[2] /= scalar
        return(self)

    cpdef length(self):
        """length"""
        return(math.sqrt(self.data[0] **2 + self.data[1] ** 2 + self.data[2] ** 2))

    cpdef length_sqrd(self):
        """length squared"""
        return(self.data[0] **2 + self.data[1] ** 2 + self.data[2] ** 2)

    cpdef double dot4(self, other):
        """
        homogeneous version, adds also h to dot product

        this version is used in matrix multiplication

        dot product of self and other vector
        dot product is the projection of one vector to another,
        for perpedicular vectors the dot prduct is zero
        for parallell vectors the dot product is the length of the other vector
        """
        cdef double dotproduct
        dotproduct = self.data[0] * other.data[0] + self.data[1] * other.data[1] + self.data[2] * other.data[2] + self.data[3] * other.data[3]
        return(dotproduct)

    cpdef double dot(self, other):
        """
        this is the non-homogeneous dot product of self and other,
        h is set to zero

        dot product of self and other vector
        dot product is the projection of one vector to another,
        for perpedicular vectors the dot prduct is zero
        for parallell vectors the dot product is the length of the other vector

        the dot product of two vectors represents also the sin of the angle
        between these two vectors.
        the dot product represents the projection of other onto self

        dot product = cos(theta)

        so theta could be calculates as 
        theta = acos(dot product)
        """
        return(np.dot(self.data, other.data))
        cdef double dotproduct = self.data[0] * other.data[0] + self.data[1] * other.data[1] + self.data[2] * other.data[2]
        return(dotproduct)


    cpdef cross(self, other):
        """
        cross product of self an other vector
        the result is a new perpendicular vector to self and other

        the length of the new vector is defined as 
        |cross product| = |self| * |other| * cos(theta)

        so the angle theta is calculated as follows

        theta = asin(|cross product| / (|self| * | other|))

        if self and other are unit vectors

        |self| = |other| = 1 
        
        this simplifies to
        
        |cross product| = sin(theta)
        """
        return(np.cross(self.data, other.data))
        return(Vector(
            self.x * other.z - self.z * other.y, 
            self.z * other.x - self.x * other.z, 
            self.x * other.y - self.y * other.x, 
            self.h))

    cpdef normalized(self):
        """
        return self with length=1, unit vector
        """
        return(np.divide(self.data, self.length()))
    unit = normalized

    cpdef tuple project2d(self, shift_vec):
        """
        project self to 2d
        simply divide x and y with z value
        """
        return((self.data[0] / self.data[2] + shift_vec[0], self.data[1] / self.data[2] + shift_vec[1]))

    cpdef double angle_to(self, other):
        """
        angle between self and other Vector object
        to calculate this, the dot product of self and other is used
        """
        v1 = self.normalized()
        v2 = other.normalized()
        cdef double dotproduct = v1.dot(v2)
        return(math.acos(dotproduct))

    cpdef double angle_to_unit(self, other):
        """this version assumes that these two vectors are unit vectors"""
        return(math.acos(self.dot(other)))
