#!/usr/bin/python3

import math
import pygame
from Vector import Vector as Vector

cdef class Mesh(object):
    """abstract class to represent mesh of polygons"""

    cdef object surface
    cdef tuple origin
    cdef int frames
    cdef int len_transformations
    cdef list transformations
    cdef list polygons
    cdef object shift_vec

    def __init__(self, surface, origin, shift, transformations=None, polygons=None):
        """
        pygame surface to draw on
        center positon of mesh in 2d space
        """
        self.surface = surface
        self.origin = origin
        self.shift_vec = shift # should be type Vector
        self.frames = 0
        # initialze list of transformations applied to every face
        if transformations is None:
            self.transformations = []
            self.initialize_transformations()
        else:
            self.transformations = transformations
        self.len_transformations = len(transformations)
        # initialize list of polygons for this mesh
        if polygons is None:
            self.polygons = []
            self.initialize_points()
        else:
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
        cdef int normal_color
        # light from above
        light_position = Vector.from_tuple(0, 0, 10)
        # apply linear transformations to vetices
        # daw faces fom lowe z to higher
        transformation = self.transformations[self.frames % self.len_transformations]
        for polygon in self.polygons:
            # apply transformation
            newpolygon = polygon.transform(transformation).shift(self.shift_vec)
            # get new position vector
            pos_vec = newpolygon.get_position_vector()
            # calculate vector from face to lightsource
            v_light = pos_vec - light_position
            # get the normal of the face
            normal = newpolygon.get_normal()
            # calculate angle between face normal and vector to light source
            light_angle = normal.angle_to(v_light)
            # angle to light source in radians, between 0 and math.pi
            normal_color = int(light_angle * 255/math.pi)
            #avg_z = max(min(abs(int(newface.get_avg_z() * 10)), 255), 0) 
            color = pygame.Color(normal_color, normal_color, normal_color, 255)
            pygame.draw.polygon(self.surface, color, newpolygon.projected(self.origin), 0)
        self.frames += 1
