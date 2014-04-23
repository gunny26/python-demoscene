#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
cimport numpy as np
DTYPE = np.float32
ctypedef np.float32_t DTYPE_d

cdef class Vector(object):

    cdef public np.ndarray data

    def __init__(self, np.ndarray data):
        self.data = data

    @classmethod
    def from_tuple(cls, *args):
        return(cls(np.array(args, dtype=DTYPE)))

    def __getitem__(self, int key):
        return(self.data[key])

    def __setitem__(self, int key, double value):
        self.data[key] = value

    def __len__(self):
        """list interface"""
        return(3)

    def __repr__(self):
        """object representation"""
        return("%s(%s)" % (self.__class__.__name__, self.data))

    def __str__(self):
        """string output"""
        return("%s" % (self.data))

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
            return(
                self.data[0] == other.data[0] and 
                self.data[1] == other.data[1] and
                self.data[2] == other.data[2])
        elif method == 4: # > __gt__
            pass
        elif method == 1: # <= lower_equal
            pass
        elif method == 3: # != __ne__
            return(
                self.data[0] != other.data[0] or
                self.data[1] != other.data[1] or
                self.data[2] != other.data[2])
        elif method == 5: # >= greater equal
            pass
            
    def __mul__(self, double scalar):
        """multiplication with scalar"""
        return(Vector(self.data * scalar))

    def __imul__(self, double scalar):
        """multiplication with scalar inplace"""
        self.data *= scalar
        return(self)

    def __div__(self, double scalar):
        """division with scalar"""
        return(Vector(self.data / scalar))

    def __idiv__(self, double scalar):
        """vector addition with another Vector class"""
        self.data /= scalar
        return(self)

    cpdef length(self):
        """length"""
        return(math.sqrt(self.data[0] ** 2 + self.data[1] ** 2 + self.data[2] ** 2))

    cpdef length_sqrd(self):
        """length squared"""
        return(self.data[0] ** 2 + self.data[1] ** 2 + self.data[2] ** 2)

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
        return(Vector(np.cross(self.data, other.data)))

    cpdef normalized(self):
        """
        return self with length=1, unit vector
        """
        return(Vector(np.divide(self.data, self.length())))
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
