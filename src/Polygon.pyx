#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
cimport numpy as np

cdef class Polygon(object):
    """this polygon consists of n-vertices
    stores a number prefereable 3 or 4 of (triangle or rectangle)
    numpy ndarray verctor
    with dimension 3 or 4 (homogeneous)
    """

    cdef np.ndarray vertices
    cdef int len_vertices

    def __init__(self, np.ndarray vertices):
        """
        vertices is a list if numpy ndarrays
        position 0 = x
        position 1 = y
        position 2 = z
        position 3 = h homogeneous, optional
        """
        # vertices should be list of ndarrays
        self.vertices = vertices
        self.len_vertices = len(vertices)

    cpdef double get_avg_z(self):
        """return average z of vertices"""
        return(self.vertices[:,2] / self.len_vertices)

    cpdef Polygon shift(self, np.ndarray shift_vector):
        """return shifted vertices"""
        cdef np.ndarray new_vertices = self.vertices.copy()
        cdef int row
        for row in range(self.len_vertices):
            new_vertices[row] = self.vertices[row] + shift_vector
        return(Polygon(new_vertices))

    cpdef Polygon ishift(self, np.ndarray shift_vector):
        """shift vertices inplace"""
        cdef int row
        for row in range(self.len_vertices):
            self.vertices[row] += shift_vector
        return(self)

    cpdef Polygon itransform(self, np.ndarray matrix):
        """apply transformation to all vertices
        matrix must have the same number as columns, than the length of out vector
        """
        cdef int row
        for row in range(self.len_vertices):
            self.vertices[row] = matrix.dot(self.vertices[row])
        return(self)

    cpdef Polygon transform(self, np.ndarray matrix):
        """apply transformation to all vertices"""
        cdef np.ndarray new_vertices = self.vertices.copy()
        cdef int row
        for row in range(self.len_vertices):
            new_vertices[row] = matrix.dot(self.vertices[row])
        return(Polygon(new_vertices))

    cpdef list projected(self, shift):
        """return point list in 2d for polygon method of pygame.draw"""
        cdef list vertices_2d = []
        for vector in self.vertices:
            vertices_2d.append((vector[0] / vector[2] + shift[0], vector[1] / vector[2] + shift[1]))
        return(vertices_2d)

    cpdef np.ndarray get_normal(self):
        """
        calculate normal vector to polygon
        the returned result is not normalized

        this version workes only for polygon with 3 vertices
        given a triangle ABC
        get v1 = (B-A)
        get v2 = (C-A)
        normal = cross(v1 and v2)
        """
        # get at least two vectors on plane to calculate normal
        v1 = self.vertices[0] - self.vertices[1]
        v2 = self.vertices[0] - self.vertices[2]
        normal = np.cross(v1, v2)
        return(normal)

    cpdef np.ndarray get_normal_new(self):
        """
        calculate normal vector to polygon
        the returned result is normalized

        this is the implementation from 
        http://www.iquilezles.org/www/articles/areas/areas.htm
        it workes generally for n-vertices polygons

        sum all edge normal vector, finally normalize result
        """
        cdef int index
        normal = np.zeros(3)
        for index in range(self.len_vertices - 1):
            normal += np.linalg.cross(self.vertices[index], self.vertices[index+1])
        return(normal)

    cpdef double get_area(self):
        """
        are is defined as the half of the lenght of the polygon normal
        """
        cdef double area
        normal = self.get_normal()
        area = np.linalg.norm(normal) / 2.0
        return(area)

    cpdef np.ndarray get_position_vector(self):
        """
        return virtual position vector, as
        average of all axis
        it should point to the middle of the polygon
        """
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

