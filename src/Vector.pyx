#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

cdef class Vector(object):

    cdef public double x
    cdef public double y
    cdef public double z
    cdef public double h

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

    def __getitem__(self, int key):
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

    def __setitem__(self, int key, double value):
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

    def __add__(self, object other):
        """vector addition with another Vector class"""
        return(Vector(self.x + other.x, self.y + other.y, self.z + other.z, self.h))

    def __iadd__(self, object other):
        """vector addition with another Vector class implace"""
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return(self)

    def __sub__(self, object other):
        """vector addition with another Vector class"""
        return(Vector(self.x - other.x, self.y - other.y, self.z - other.z, self.h))

    def __isub__(self, object other):
        """vector addition with another Vector class implace"""
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return(self)

    def __richcmp__(self, object other, int method):
        if method == 0: # < __lt__
            pass
        elif method == 2: # == __eq__
            return(self.x == other.x and self.y == other.y and self.z == other.z and self.h == other.h)
        elif method == 4: # > __gt__
            pass
        elif method == 1: # <= lower_equal
            pass
        elif method == 3: # != __ne__
            return(self.x != other.x or self.y != other.y or self.z != other.z or self.h != other.h)
        elif method == 5: # >= greater equal
            pass
            
    def __mul__(self, double scalar):
        """multiplication with scalar"""
        return(Vector(self.x * scalar, self.y * scalar, self.z * scalar, self.h))

    def __imul__(self, double scalar):
        """multiplication with scalar inplace"""
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        return(self)

    def __div__(self, double scalar):
        """division with scalar"""
        return(Vector(self.x / scalar, self.y / scalar, self.z / scalar, self.h))

    def __idiv__(self, double scalar):
        """vector addition with another Vector class"""
        self.x /= scalar
        self.y /= scalar
        self.z /= scalar
        return(self)

    cpdef length(self):
        """length"""
        return(math.sqrt(self.x **2 + self.y ** 2 + self.z ** 2))

    cpdef length_sqrd(self):
        """length squared"""
        return(self.x **2 + self.y ** 2 + self.z ** 2)

    cpdef double dot4(self, other):
        """
        homogeneous version, adds also h to dot product

        this version is used in matrix multiplication

        dot product of self and other vector
        dot product is the projection of one vector to another,
        for perpedicular vectors the dot prduct is zero
        for parallell vectors the dot product is the length of the other vector
        """
        return(self.x * other.x + self.y * other.y + self.z * other.z + self.h * other.h)

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
        return(self.x * other.x + self.y * other.y + self.z * other.z)


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
        return(Vector(
            self.y * other.z - self.z * other.y, 
            self.z * other.x - self.x * other.z, 
            self.x * other.y - self.y * other.x, 
            self.h))

    cpdef normalized(self):
        """
        return self with length=1, unit vector
        """
        return(self / self.length())
    unit = normalized

    cpdef tuple project2d(self, shift_vec):
        """
        project self to 2d
        simply divide x and y with z value
        """
        return((self.x / self.z + shift_vec[0], self.y / self.z + shift_vec[1]))

    cpdef double angle_to(self, other):
        """
        angle between self and other Vector object
        to calculate this, the dot product of self and other is used
        """
        v1 = self.normalized()
        v2 = other.normalized()
        return(math.acos(v1.dot(v2)))
