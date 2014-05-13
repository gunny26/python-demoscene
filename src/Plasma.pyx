#!/usr/bin/python
from __future__ import division
import pygame
import math
import random
import numpy as np
cimport numpy as np


cdef class Plasma(object):
    """Plasma Effect on Surface"""

    cdef int tick
    cdef object surface
    cdef object parent
    cdef object colors
    cdef np.ndarray sin
    cdef np.ndarray cos

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
        self.colors = []
        self.sin = np.zeros(512, dtype=np.float)
        self.cos = np.zeros(512, dtype=np.float)
        self.initialize()

    cdef initialize(self):
        cdef rad_to_degree = math.pi / 180
        black = pygame.Color(0, 0, 0, 255)
        for h in range(300):
            black.hsla = (h, 100, 50, 50)
            self.colors.append(black)
        for degree in range(512):
            self.sin[degree] = math.sin(degree * rad_to_degree * 512/360)
            self.cos[degree] = math.cos(degree * rad_to_degree * 512/360)

    cdef calculate(self):
        """version with math.sin"""
        cdef int t
        cdef double x
        cdef double y
        cdef int xx
        cdef int yy
        cdef int h
        cdef int s
        cdef double v
        cdef double cx
        cdef double cy
        #cdef double rad_to_degree =  math.pi / 180
        cdef np.ndarray pixel2d
        t = self.tick
        pixel2d = pygame.surfarray.pixels2d(self.surface)
        for yy in range(self.surface.get_height()):
            for xx in range(self.surface.get_width()):
                #x = xx * rad_to_degree
                #y = yy * rad_to_degree
                cx = (xx + self.sin[t >> 2 & 511])
                cy = (yy + self.cos[t >> 1 & 511])
                v = self.sin[(xx * 10 + t) & 511]
                v += self.sin[(yy * 10 + t) >> 2 & 511]
                v += self.sin[(xx * 10 + yy * 10 + t) >> 2 & 511]
                v += self.sin[(int(math.sqrt(100 * (cx * cx + cy * cy) + 1)) + t) & 511]
                #v = v / 2
                # get to color up your life, calculate hue
                h = (128 + int(math.sin(4 + v) * 128)) << 16
                pixel2d[xx, yy] = h
            # increment angle for next step
        self.tick += 5
        # self.tick = self.tick + 5 * rad_to_degree

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
        #pygame.surfarray.blit_array(self.surface, self.array2d)
        # scale surface to size of parent surface to fit
        pygame.transform.scale(self.surface, self.parent.get_size(), self.parent)


cdef class PlasmaFractal(object):

    cdef object surface

    def __init__(self, surface, scale=1):
        """
        (pygame.Surface) surface - surface to draw on
        (int) scale - scaling factor
        """
        # initialize things
        self.surface = surface
        #self.surface = pygame.Surface(surface.get_size())
        #self.surface = pygame.transform.scale(self.surface, (self.surface.get_width() / scale, self.surface.get_height() / scale))
        #print "using %s arraytype" % pygame.surfarray.get_arraytype()

    cdef Displace(self, float num):
        cdef float maximum = num / (self.surface.get_width() + self.surface.get_height()) * 3
        return((random.random() - 0.5) * maximum)

    cdef ComputeColor(self, float c):
        cdef float red
        cdef float green
        cdef float blue
        if c < 0.5:
            red = c * 2
        else:
            red = (1.0 - c) * 2
        if c >= 0.3 and c < 0.8:
            green = (c - 0.3) * 2
        elif c < 0.3:
            green = (0.3 - c) * 2
        else:
            green = (1.3 - c) * 2
        if c >= 0.5:
            blue = (c - 0.5) * 2
        else:
            blue = (0.5 - c) * 2
        return(pygame.Color(int(red*255), int(green*255), int(blue*255)))

    cpdef update(self):
            """
            This is something of a helper function to create an initial grid
            before the recursive function is called.
            """
            cdef float c1, c2, c3, c4
            #Assign the four corners of the intial grid random color values
            #These will end up being the colors of the four corners of the applet.
            c1 = random.random()
            c2 = random.random()
            c3 = random.random()
            c4 = random.random()
            self.DivideGrid(0, 0, self.surface.get_width(), self.surface.get_height(), c1, c2, c3, c4)

    cdef DivideGrid(self, float x, float y, float width, float height, float c1, float c2, float c3, float c4):
        """
        This is the recursive function that implements the random midpoint
        //displacement algorithm. It will call itself until the grid pieces
        //become smaller than one pixel.
        """
        cdef float Edge1, Edge2, Edge3, Edge4, Middle
        cdef float newWidth = width / 2
        cdef float newHeight = height / 2
        cdef float c

        if width > 2 or height > 2:
            Middle = (c1 + c2 + c3 + c4) / 4 + self.Displace(newWidth + newHeight)  #Randomly displace the midpoint!
            Edge1 = (c1 + c2) / 2  #Calculate the edges by averaging the two corners of each edge.
            Edge2 = (c2 + c3) / 2
            Edge3 = (c3 + c4) / 2
            Edge4 = (c4 + c1) / 2

            #Make sure that the midpoint doesn't accidentally "randomly displaced" past the boundaries!
            if Middle < 0:
                Middle = 0
            elif Middle > 1.0:
                Middle = 1.0
            #Do the operation over again for each of the four new grids.
            self.DivideGrid(x, y, newWidth, newHeight, c1, Edge1, Middle, Edge4)
            self.DivideGrid(x + newWidth, y, newWidth, newHeight, Edge1, c2, Edge2, Middle)
            self.DivideGrid(x + newWidth, y + newHeight, newWidth, newHeight, Middle, Edge2, c3, Edge3)
            self.DivideGrid(x, y + newHeight, newWidth, newHeight, Edge4, Middle, Edge3, c4)
        else:    #This is the "base case," where each grid piece is less than the size of a pixel.
            #The four corners of the grid piece will be averaged and drawn as a single pixel.
            c = (c1 + c2 + c3 + c4) / 4
            self.surface.set_at((int(x), int(y)), self.ComputeColor(c)) #Java doesn't have a function to draw a single pixel, so
