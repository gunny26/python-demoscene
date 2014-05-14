#!/usr/bin/python
from __future__ import division
import pygame
import math
import random
import array
import numpy as np
cimport numpy as np
DTYPE = np.float
ctypedef np.float_t DTYPE_t


cdef class Plasma(object):
    """Plasma Effect on Surface"""

    cdef int tick
    cdef object surface
    cdef object parent
    cdef object sin
    cdef object cos

    def __init__(self, surface, scale=1):
        """
        (pygame.Surface) surface - surface to draw on
        (int) scale - scaling factor
        """
        # initialize things
        self.tick = 0
        self.parent = surface
        self.surface = pygame.Surface(surface.get_size())
        self.surface = pygame.transform.scale(self.surface, (int(self.surface.get_width() / scale), int(self.surface.get_height() / scale)))
        print "using %s arraytype" % pygame.surfarray.get_arraytype()
        self.sin = array.array("f", [0.0] * 512)
        self.cos = array.array("f", [0.0] * 512)
        self.initialize()

    cdef initialize(self):
        cdef rad_to_degree = math.pi / 180
        for degree in range(512):
            rad = degree * rad_to_degree * 512/360
            self.sin[degree] = math.sin(rad)
            self.cos[degree] = math.cos(rad)

    cdef calculate(self):
        """version with math.sin"""
        cdef int t
        cdef int xx
        cdef int yy
        cdef int y8
        cdef int x8
        cdef int index
        cdef double v
        cdef double ysin
        #cdef double rad_to_degree =  math.pi / 180
        cdef np.ndarray pixel2d
        t = self.tick
        pixel2d = pygame.surfarray.pixels2d(self.surface)
        for yy in range(self.surface.get_height()):
            # these two values are the same for every xx
            y8 = yy << 3
            ysin = self.sin[(y8 + t) >> 2 & 511]
            for xx in range(self.surface.get_width()):
                # shift by 3 bits, equals multiplication by 8
                x8 = (xx << 3) + t
                # & 511 makes sure, that the result is in between 0-512
                v = ysin + self.sin[x8 & 511]
                v += self.sin[(x8 + y8) >> 2 & 511]
                # this square root cost about 20 fps
                #v += self.sin[(int(math.sqrt(100 * (cx * cx + cy * cy) + 1)) + t) & 511]
                # get to color up your life, calculate hue
                # v should be in boundary -4 to +4, range of 8
                # so get to my array type sin, it should be shifted by 4 and scaled by 64
                index = int((v + 4) * 64)
                pixel2d[xx, yy] = int(128 + self.sin[index] * 128) << 16
        self.tick += 5

    cdef calculate2(self):
        """version with math.sin"""
        cdef int xx
        cdef int yy
        cdef np.ndarray pixel2d
        pixel2d = pygame.surfarray.pixels2d(self.surface)
        for yy in range(self.surface.get_height()):
            for xx in range(self.surface.get_width()):
                pixel2d[xx, yy] = 1 << 24
     
    cpdef update(self):
        """update every frame"""
        self.calculate()
        # scale surface to size of parent surface to fit
        pygame.transform.scale(self.surface, self.parent.get_size(), self.parent)


