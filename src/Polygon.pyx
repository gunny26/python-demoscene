#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
cimport numpy as np
DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

cdef class Polygon(object):
    """this polygon consists of n-vertices
    stores a number prefereable 3 or 4 of (triangle or rectangle)
    numpy ndarray verctor
    with dimension 3 or 4 (homogeneous)
    """

    cdef np.ndarray vertices
    cdef np.ndarray normal
    cdef int len_vertices

    def __init__(self, np.ndarray vertices):
        """
        vertices is a list if numpy ndarrays
        position 0 = x
        position 1 = y
        position 2 = z
        position 3 = w homogeneous, optional
        """
        # vertices should be list of ndarrays
        self.vertices = vertices
        self.len_vertices = len(vertices)
        self.normal = self._get_normal_faster()

    cpdef double get_avg_z(self):
        """return average z of vertices"""
        return(self.vertices[:,2] / self.len_vertices)

    cpdef Polygon transform(self, np.ndarray matrix):
        """apply transformation to all vertices"""
        cdef np.ndarray new_vertices = self.vertices.copy()
        cdef int row
        for row in range(self.len_vertices):
            new_vertices[row] = matrix.dot(self.vertices[row])
        return(Polygon(new_vertices))

    cpdef list projected_old(self, int shift_x, int shift_y):
        """
        return point list in 2d for polygon method of pygame.draw
        simple algorithm which divides x and y through z value
        """
        cdef list vertices_2d = []
        for vector in self.vertices:
            abs_z = abs(vector[2])
            vertices_2d.append((vector[0] / abs_z + shift_x, vector[1] / abs_z + shift_y))
        return(vertices_2d)
    
    cpdef list projected(self, int shift_x, int shift_y, double fov=0.8, int viewer_distance=1):
        """
        method with field of view and viewer distance
        """
        cdef list vertices_2d = []
        cdef double factor, x, y
        for vector in self.vertices:
            factor = fov / (viewer_distance + vector[2])
            x = vector[0] * factor + shift_x
            y = -vector[1] * factor + shift_y
            vertices_2d.append((x, y))
        return(vertices_2d)

    cpdef list projected_faster(self, int shift_x, int shift_y):
        """return point list in 2d for polygon method of pygame.draw"""
        cdef list vertices_2d = []
        cdef int counter
        for counter in range(self.len_vertices):
            abs_z = abs(self.vertices[counter][2])
            vertices_2d.append((self.vertices[counter][0] / abs_z + shift_x, self.vertices[counter][1] / abs_z + shift_y))
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
        v1 = self.vertices[0][:3] - self.vertices[1][:3]
        v2 = self.vertices[0][:3] - self.vertices[2][:3]
        normal = np.cross(v1, v2)
        return(np.append(normal, 1.0))

    cpdef np.ndarray _get_normal_faster(self):
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
        cdef np.ndarray v1
        cdef np.ndarray v2
        cdef DTYPE_t x
        cdef DTYPE_t y
        cdef DTYPE_t z
        v1 = self.vertices[0] - self.vertices[1]
        v2 = self.vertices[0] - self.vertices[2]
        x = v1[1] * v2[2] - v1[2] * v2[1]
        y = v1[2] * v2[0] - v1[0] * v2[2]
        z = v1[0] * v2[1] - v1[1] * v2[0]
        return(np.array((x, y, z, 1.0), dtype=DTYPE))

    cpdef np.ndarray get_normal_faster(self):
        return self.normal


    cpdef np.ndarray get_normal_new(self):
        """
        calculate normal vector to polygon
        the returned result is normalized

        this is the implementation from 
        http://www.iquilezles.org/www/articles/areas/areas.htm
        it workes generally for n-vertices polygons

        sum all edge normal vector, finally normalize result
        """
        # calculate vector notmal wiothout homogeneous part,
        # cross product is only well defined for 2 and 3 dimensional verctors
        cdef int index
        normal = np.zeros(4)
        for index in range(self.len_vertices - 1):
            normal += np.linalg.cross(self.vertices[index], self.vertices[index+1])
        # finally add homgeneous part
        return(np.append(normal, 1.0))

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
        cdef np.ndarray pos_vec
        cdef np.ndarray vector
        pos_vec = self.vertices[0].copy()
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
        return(str(self.vertices))

