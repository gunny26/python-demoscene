#!/usr/bin/python3

import math
import pygame
import numpy as np
DTYPE = np.float64()
cimport numpy as np
ctypedef np.float64_t DTYPE_t
import Utils3d

cdef class Mesh(object):
    """abstract class to represent mesh of polygons"""

    cdef object surface
    cdef int origin_x
    cdef int origin_y
    cdef tuple origin
    cdef int frames
    cdef int len_transformations
    cdef list transformations
    cdef list polygons
    cdef np.ndarray shift_vec

    def __init__(self, surface, tuple origin, transformations=None, polygons=None):
        """
        pygame surface to draw on
        center positon of mesh in 2d space
        """
        self.surface = surface
        (self.origin_x, self.origin_y) = origin
        self.frames = 0
        # initialze list of transformations applied to every face
        self.transformations = transformations
        self.len_transformations = len(transformations)
        # initialize list of polygons for this mesh
        self.polygons = polygons

    cpdef initialize_points(self):
        """
        fills self.faces with polygons
        """
        pass

    cpdef initialize_transformations(self):
        """
        fill self.transformations with transformation
        matrices applied to every polygon.
        one transformation matrix for every frame
        """
        pass

    cpdef update(self):
        """
        called on every frame
        apply transformation matrix and project every polygon to 2d
        for color avg_z function is used
        polygons are sorted on avg_z value

        finally painting on surface is called
        """
        cdef np.ndarray light_positon
        cdef np.ndarray pos_vec
        cdef np.ndarray v_light
        cdef np.ndarray normal
        cdef double light_angle
        cdef int normal_color
        # light from above
        #light_position = np.array((0.0, 0.0, 10.0, 1.0), dtype=DTYPE)
        # apply linear transformations to vetices
        # daw faces fom lowe z to higher
        transformation = self.transformations[self.frames % self.len_transformations]
        color = pygame.Color(200, 200, 200, 255)
        for polygon in self.polygons:
            # apply transformation to every vertice in polygon
            newpolygon = polygon.transform(transformation)
            # get new position vector
            #pos_vec = newpolygon.get_position_vector()
            # calculate vector from face to lightsource
            #v_light = pos_vec - light_position
            # get the normal of the face
            #normal = newpolygon.get_normal_faster()
            # calculate angle between face normal and vector to light source
            #light_angle = Utils3d.angle_to(normal, v_light)
            # angle to light source in radians, between 0 and math.pi
            #normal_color = int(light_angle * 255 / math.pi)
            #avg_z = max(min(abs(int(newface.get_avg_z() * 10)), 255), 0) 
            #color = pygame.Color(normal_color, normal_color, normal_color, 255)
            pygame.draw.polygon(self.surface, color, newpolygon.projected(self.origin_x, self.origin_y), 1)
        self.frames += 1
