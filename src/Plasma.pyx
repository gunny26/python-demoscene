#!/usr/bin/python

import pygame
import math
import numpy as np
cimport numpy as np


cdef class Plasma(object):
    """Plasma Effect on Surface"""

    cdef double tick
    cdef object surface
    cdef object parent

    def __init__(self, surface, scale=1):
        """
        (pygame.Surface) surface - surface to draw on
        (int) scale - scaling factor
        """
        # initialize things
        self.tick = 0
        self.parent = surface
        self.surface = pygame.Surface(surface.get_size())
        self.surface = pygame.transform.scale(self.surface, (self.surface.get_width() / scale, self.surface.get_height() / scale))
        print "using %s arraytype" % pygame.surfarray.get_arraytype()

    cdef calculate(self):
        """version with math.sin"""
        cdef double t
        cdef double x
        cdef double y
        cdef int xx
        cdef int yy
        cdef int h
        cdef int s
        cdef double v
        cdef double cx
        cdef double cy
        cdef double rad_to_degree =  math.pi / 180
        cdef np.ndarray pixel2d
        t = self.tick
        color = pygame.Color(0, 0, 0, 255)
        pixel2d = pygame.surfarray.pixels2d(self.surface)
        for yy in range(self.surface.get_height()):
            for xx in range(self.surface.get_width()):
                x = xx * rad_to_degree
                y = yy * rad_to_degree
                cx = x + .5 * math.sin(t / 5.0)
                cy = y + .5 * math.cos(t / 3.0)
                v = math.sin(x * 10 + t)
                v += math.sin((y * 10 + t) / 2.0)
                v += math.sin((x * 10 + y * 10 + t) / 2.0)
                v += math.sin(math.sqrt(100 * (cx * cx + cy * cy) + 1) + t)
                v /= 2.0
                # get to color up your life, calculate hue
                h = int(180 + math.sin(v) * 180)
                s = int(50 + math.cos(v) * 50)
                color.hsla = (h, s, 50, 50)
                pixel2d[xx, yy] = color
            # increment angle for next step
        self.tick = self.tick + 5 * rad_to_degree

    cdef calculate2(self):
        """version with math.sin"""
        cdef double t
        cdef double x
        cdef double y
        cdef int xx
        cdef int yy
        cdef int h
        cdef int s
        cdef double v
        cdef double cx
        cdef double cy
        cdef double rad_to_degree =  math.pi / 180
        cdef np.ndarray pixel2d
        t = self.tick
        color = pygame.Color(0, 0, 0, 255)
        pixel2d = pygame.surfarray.pixels2d(self.surface)
        for yy in range(self.surface.get_height()):
            for xx in range(self.surface.get_width()):
                pixel2d[xx, yy] = color
            # increment angle for next step
        self.tick = self.tick + 5 * rad_to_degree
     
    cpdef update(self):
        """update every frame"""
        self.calculate2()
        #pygame.surfarray.blit_array(self.surface, self.array2d)
        # scale surface to size of parent surface to fit
        pygame.transform.scale(self.surface, self.parent.get_size(), self.parent) 
