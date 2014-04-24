#!/usr/bin/python
# cython: profile=True
# -*- coding: utf-8 -*-

import math
import array
from Vector import Vector as Vector
import numpy as np
# only for cython
cimport numpy as np
DTYPE = np.float32
ctypedef np.float32_t DTYPE_t

cdef class Matrix3d(object):

    cdef public np.ndarray data

    def __init__(self, np.ndarray data):
        """init from 3 row vectors"""
        self.data = data

    @classmethod
    def from_tuple(cls, np.ndarray data):
        return(cls(np.ndarray(data, dtype=DTYPE).reshape([3,3])))

    @classmethod
    def from_array(cls, data):
        data = np.ndarray(data, dtype=DTYPE).reshape([3, 3])
        return(cls(data))

    @classmethod
    def from_row_vectors(cls, row1, row2, row3):
        data = np.array([row1.data, row2.data, row3.data], dtype=DTYPE)
        return(cls(data.reshape(3, 3)))

    def __repr__(self):
        return("Matrix3d(%s)" % self.data)

    def __str__(self):
        return("Matrix3d(%s)" % self.data)

    cpdef _set_col_vector(self, int colnum, object vector):
        self.data[:,colnum] = vector.data

    cpdef _get_col_vector(self, int colnum):
        """return column vector as Vector object"""
        return(Vector(self.data[:,colnum]))

    cpdef _set_row_vector(self, int rownum, object vector):
        """set row with data from vector"""
        self.data[rownum] = vector.data

    cpdef _get_row_vector(self, int rownum):
        """rownum starts at row = 0"""
        return(Vector(self.data[rownum]))

    def __mul__(self, double scalar):
        return(Matrix3d(self.data * scalar))

    def __imul__(self, double scalar):
        """multiply matrix with scalar"""
        self.data *= scalar
        return(self)

    def __div__(self, double scalar):
        return(Matrix3d(self.data / scalar))

    def __idiv__(self, double scalar):
        """multiply matrix with scalar"""
        self.data /= scalar
        return(self)

    def __add__(self, object other):
        return(Matrix3d(self.data + other.data))

    def __iadd__(self, object other):
        """add two matrices"""
        self.data += other.data
        return(self)

    cpdef mul_vec(self, vector):
        """
        multiply self with vector
        return type is vector

        multiply 3x3 with 3x1 = 3x1
        """
        return(Vector(np.dot(self.data, vector)))

    cpdef Matrix3d mul_matrix(self, Matrix3d other):
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
        #result = np.dot(self.data, other.data)
        return(Matrix3d(self.data.dot(other.data)))

    cpdef double determinant(self):
        """
        return determinant of self
        | 0   1  2  3 |
        | 4   5  6  7 |
        | 8   9 10 11 |
        | 12 13 14 15 |

        """
        return(np.linalg.det(self.data))

    cpdef Matrix3d inverse(self):
        """
        return determinant of self
        | 0   1  2  3 |
        | 4   5  6  7 |
        | 8   9 10 11 |
        | 12 13 14 15 |

        http://www.mathsisfun.com/algebra/matrix-inverse-minors-cofactors-adjugate.html
        """
        return(Matrix3d(np.linalg.inv(self.data)))
