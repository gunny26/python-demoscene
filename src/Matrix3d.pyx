#!/usr/bin/python
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

    def __init__(self, data):
        """init from 4 row vectors"""
        assert len(data) == 16
        self.data = data

    @classmethod
    def from_tuple(cls, np.ndarray data):
        return(cls(np.ndarray(data, dtype=DTYPE)))

    @classmethod
    def from_array(cls, data):
        data = np.ndarray(data, dtype=DTYPE)
        return(cls(data))

    @classmethod
    def from_row_vectors(cls, row1, row2, row3, row4):
        data = np.zeros([16], dtype=DTYPE)
        cdef int rownum
        for rownum in range(4):
            data[rownum*4] = row1[rownum]
            data[rownum*4+1] = row2[rownum]
            data[rownum*4+2] = row3[rownum]
            data[rownum*4+3] = row4[rownum]
        return(cls(data))

    def __getstate__(self):
        return(self.data)

    def __setstate__(self, object data):
        self.data = data

    def __repr__(self):
        sb = "Matrix3d("
        cdef int row
        cdef int startindex
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
        cdef int row
        cdef int startindex
        for row in range(4):
            startindex = row * 4
            sb += "| %f, %f, %f, %f|\n" % (
                self.data[startindex], 
                self.data[startindex+1], 
                self.data[startindex+2], 
                self.data[startindex+3])
        return(sb)

    def __getitem__(self, int key):
        return(self.data[key])

    def __setitem__(self, int key, double value):
        self.data[key] = value

    cpdef _set_col_vector(self, int colnum, object vector):
        cdef int counter = colnum
        for item in vector:
            self.data[counter] = item
            counter += 4

    cpdef _get_col_vector(self, int colnum):
        """return column vector as Vector object"""
        return(Vector(
            self.data[colnum],
            self.data[colnum+4],
            self.data[colnum+8],
            self.data[colnum+12]))

    cpdef _set_row_vector(self, int rownum, object vector):
        """set row with data from vector"""
        self.data[rownum*4] = vector[0]
        self.data[rownum*4+1] = vector[1]
        self.data[rownum*4+2] = vector[2]
        self.data[rownum*4+3] = vector[3]

    cpdef _get_row_vector(self, int rownum):
        """rownum starts at row = 0"""
        cdef int start = 4 * rownum
        return(Vector(
            self.data[start], 
            self.data[start+1],
            self.data[start+2],
            self.data[start+3]))

    def __mul__(self, double scalar):
        matrix = Matrix3d(self.__getstate__())
        cdef int counter
        for counter in range(16):
            self.data[counter] *= scalar
        return(matrix)

    def __imul__(self, double scalar):
        """multiply matrix with scalar"""
        cdef int counter
        for counter in range(16):
            self.data[counter] *= scalar 
        return(self)

    def __div__(self, double scalar):
        cdef int counter
        matrix = self.data
        np.divide(matrix, scalar)
        #for counter in range(16):
        #    self.data[counter] /= scalar
        return(Matrix3d(matrix))

    def __idiv__(self, double scalar):
        """multiply matrix with scalar"""
        cdef int counter
        for counter in range(16):
            self.data[counter] /= scalar 
        return(self)

    def __add__(self, object other):
        matrix = Matrix3d(self.__getstate__())
        cdef int counter
        for counter in range[16]:
            self.data[counter] += other[counter]
        return(matrix)

    def __iadd__(self, object other):
        """add two matrices"""
        cdef int counter
        for counter in range(16):
            self.data[counter] += other[counter]
        return(self)

    cpdef mul_vec(self, object vector):
        """
        multiply self with vector
        return type is vector

        multiply 4x4 with 4x1 = 4x1
        """
        return(Vector(
            self._get_row_vector(0).dot4(vector),
            self._get_row_vector(1).dot4(vector),
            self._get_row_vector(2).dot4(vector),
            self._get_row_vector(3).dot4(vector)))

    cpdef mul_matrix(self, object other):
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
        mat1 = np.reshape(self.data, [4, 4])
        mat2 = np.reshape(other.data, [4, 4])
        result = np.dot(mat1, mat2).flatten()
        return(Matrix3d(result))

    cpdef double determinant(self):
        """
        return determinant of self
        | 0   1  2  3 |
        | 4   5  6  7 |
        | 8   9 10 11 |
        | 12 13 14 15 |

        """
        cdef double det
        data = self.data
        det = np.linalg.det(data.reshape([4, 4]))
        return(det)

    cpdef inverse(self):
        """
        return determinant of self
        | 0   1  2  3 |
        | 4   5  6  7 |
        | 8   9 10 11 |
        | 12 13 14 15 |

        http://www.mathsisfun.com/algebra/matrix-inverse-minors-cofactors-adjugate.html
        """
        cdef double det = self.determinant()
        data = np.reshape(self.data, [4, 4])
        return(Matrix3d(np.linalg.inv(data).flatten()))
