#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import array
from Vector import Vector as Vector

cdef class Matrix3d(object):

    cdef object data

    def __init__(self, *args):
        self.data = array.array("d", [0.0] * 16)
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

    def __setstate__(self, object data):
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

    def __getitem__(self, int key):
        return(self.data[key])

    def __setitem__(self, int key, double value):
        self.data[key] = value

    cpdef _set_col_vector(self, int colnum, object vector):
        counter = colnum
        for item in vector:
            self.data[counter] = item
            counter += 4

    cpdef _get_col_vector(self, int colnum):
        """return column vector as Vector object"""
        return(Vector(self.data[colnum::4]))

    cpdef _set_row_vector(self, int rownum, object vector):
        """set row with data from vector"""
        self.data[rownum*4] = vector[0]
        self.data[rownum*4+1] = vector[1]
        self.data[rownum*4+2] = vector[2]
        self.data[rownum*4+3] = vector[3]

    cpdef _get_row_vector(self, int rownum):
        return(Vector(self.data[rownum*4: rownum*4+4]))

    def __mul__(self, double scalar):
        matrix = Matrix3d(self.__getstate__())
        for counter in range(16):
            matrix[counter] *= scalar
        return(matrix)

    def __imul__(self, double scalar):
        """multiply matrix with scalar"""
        for counter in range(16):
            self.data[counter] *= scalar 
        return(self)

    def __div__(self, double scalar):
        matrix = Matrix3d(self.__getstate__())
        for counter in range(16):
            matrix[counter] /= scalar
        return(matrix)

    def __idiv__(self, double scalar):
        """multiply matrix with scalar"""
        for counter in range(16):
            self.data[counter] /= scalar 
        return(self)

    def __add__(self, object other):
        matrix = self.copy()
        for counter in range[16]:
            matrix[counter] += other[counter]
        return(matrix)

    def __iadd__(self, object other):
        """add two matrices"""
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
        data = [0.0] * 16
        for row in range(4):
            vec_data = [0.0] * 4
            for col in range(4):
                data[row*4 + col] = self._get_row_vector(row).dot4(other._get_col_vector(col))
        return(Matrix3d(data))


    cpdef double determinant(self):
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
        raise(StandardError("Determinant is Zero"))

