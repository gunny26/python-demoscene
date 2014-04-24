#!/usr/bin/python
# cython: profile=True
# -*- coding: utf-8 -*-

import math
import numpy as np
cimport numpy as np
from Vector import Vector as Vector

cdef class Polygon(object):
    """this polygon consists of n-vertices"""

    cdef list vertices
    cdef int len_vertices

    def __init__(self, list vertices):
        # vertices should be list of ndarrays
        self.vertices = vertices
        self.len_vertices = len(vertices)

    cpdef double get_avg_z(self):
        """return average z of vertices"""
        cdef double avg_z = 0.0
        for vector in self.vertices:
            avg_z += vector[1]
        return(avg_z / self.len_vertices)

    cpdef Polygon shift(self, np.ndarray shift_vector):
        """return shifted vertices"""
        new_vertices = []
        for vector in self.vertices:
            new_vertices.append(vector + shift_vector)
        return(Polygon(new_vertices))

    cpdef ishift(self, np.ndarray shift_vector):
        """shift vertices inplace"""
        cdef int counter
        for counter in range(self.len_vertices):
            self.vertices[counter] += shift_vector

    cpdef itransform(self, np.ndarray matrix):
        """apply transformation to all vertices"""
        cdef int counter
        for counter in range(self.len_vertices):
            self.vertices[counter] = matrix * self.vertices[counter]

    cpdef Polygon transform(self, object matrix):
        """apply transformation to all vertices"""
        new_vertices = []
        for vector in self.vertices:
            new_vertices.append(matrix.mul_vec(vector))
        return(Polygon(new_vertices))

    cpdef list projected(self, shift):
        """return point list in 2d for polygon method of pygame.draw"""
        cdef list vertices_2d
        vertices_2d = []
        for vertice in self.vertices:
            vertices_2d.append(vertice.project2d(shift))
        return(vertices_2d)

    cpdef get_normal(self):
        """
        calculate normal vector to polygon
        the returned result is not normalized

        this version workes only for polygon with 3 vertices
        given a triangle ABC
        get v1 = (B-A)
        get v2 = (C-A)
        normal = cross(v1 and v2)
        """
        # get at least two vectors on plan
        v1 = self.vertices[0] - self.vertices[1]
        v2 = self.vertices[0] - self.vertices[2]
        normal = v1.cross(v2)
        return(normal)

    cpdef get_normal_new(self):
        """
        calculate normal vector to polygon
        the returned result is not normalized

        this is the implementation from 
        http://www.iquilezles.org/www/articles/areas/areas.htm
        it workes generally for n-vertices polygons
        """
        cdef int index
        normal = Vector.from_tuple(0, 0, 0)
        for index in range(self.len_vertices - 1):
            normal += self.vertices[index].cross(self.vertices[index+1])
        return(normal)

    cpdef double get_area(self):
        """
        are is defined as the half of the lenght of the polygon normal
        """
        cdef double area
        normal = self.get_normal()
        area = normal.length() / 2.0
        return(area)

    cpdef get_position_vector(self):
        """
        return virtual position vector, as
        average of all axis
        it should point to the middle of the polygon
        """
        cdef double avg_x = 0.0
        cdef double avg_y = 0.0
        cdef double avg_z = 0.0
        pos_vec = self.vertices[0]
        for vector in self.vertices[1:]:
            pos_vec += vector
        return(pos_vec / self.len_vertices)

    def __richcmp__(obj1, obj2, method):
        if method == 0: # < __lt__
            return(obj1.get_avg_z() < obj2.self.avg_z())
        elif method == 2: # == __eq__
            return(obj1.vertices == obj2.vertices)
        elif method == 4: # > __gt__
            return(obj1.get_avg_z() > obj2.self.avg_z())
        elif method == 1: # <= lower_equal
            return(obj1.get_avg_z() <= obj2.self.avg_z())
        elif method == 3: # != __ne__
            return(obj1.vertices != obj2.vertices)
        elif method == 5: # >= greater equal
            return(obj1.get_avg_z() >= obj2.self.avg_z())
 
    def __str__(self):
        sb = ""
        for vertice in self.vertices:
            sb += (str(vertice))
        return(sb)

