#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

cdef class Vector2(object):
    """Vector in R² not homogeneous"""

    cdef public double x
    cdef public double y
    cdef public double z
    cdef public double h

    def __init__(self, double x, double y):
        self.x = x
        self.y = y

    @classmethod
    def from_tuple(cls, data):
        return(cls(data[0], data[1]))

    def __len__(self):
        """list interface"""
        return(2)

    def __getitem__(self, int key):
        """list interface"""
        if key == 0:
            return(self.x)
        elif key == 1:
            return(self.y)
        else:
            raise(IndexError("Invalid index %d to Vector" % key))

    def __setitem__(self, int key, double value):
        """list interface"""
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise(IndexError("Invalid index %d to Vector" % key))

    def __repr__(self):
        """object representation"""
        return("Vector2(%(x)f, %(y)f)" % self.__dict__)

    def __str__(self):
        """string output"""
        return("[%(x)f, %(y)f]" % self.__dict__)

    def __add__(self, object other):
        """vector addition with another Vector class"""
        return(Vector2(self.x + other.x, self.y + other.y))

    def __iadd__(self, object other):
        """vector addition with another Vector class implace"""
        self.x += other.x
        self.y += other.y
        return(self)

    def __sub__(self, object other):
        """vector addition with another Vector class"""
        return(Vector2(self.x - other.x, self.y - other.y))

    def __isub__(self, object other):
        """vector addition with another Vector class implace"""
        self.x -= other.x
        self.y -= other.y
        return(self)

    def __richcmp__(self, object other, int method):
        if method == 0: # < __lt__
            pass
        elif method == 2: # == __eq__
            return(self.x == other.x and self.y == other.y)
        elif method == 4: # > __gt__
            pass
        elif method == 1: # <= lower_equal
            pass
        elif method == 3: # != __ne__
            return(self.x != other.x or self.y != other.y)
        elif method == 5: # >= greater equal
            pass
            
    def __mul__(self, double scalar):
        """multiplication with scalar"""
        return(Vector2(self.x * scalar, self.y * scalar))

    def __imul__(self, double scalar):
        """multiplication with scalar inplace"""
        self.x *= scalar
        self.y *= scalar
        return(self)

    def __div__(self, double scalar):
        """division with scalar"""
        return(Vector2(self.x / scalar, self.y / scalar))

    def __idiv__(self, double scalar):
        """vector addition with another Vector class"""
        self.x /= scalar
        self.y /= scalar
        return(self)

    cpdef length(self):
        """length"""
        return(math.sqrt(self.x **2 + self.y ** 2))

    cpdef length_sqrd(self):
        """length squared"""
        return(self.x **2 + self.y ** 2)

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
        cdef double dotproduct = self.x * other.x + self.y * other.y
        return(dotproduct)

    cpdef normalized(self):
        """
        return self with length=1, unit vector
        """
        return(self / self.length())
    unit = normalized

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
