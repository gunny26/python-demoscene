#!/usr/bin/python
#

import sys
import pygame
import numpy as np
cimport numpy as np

cdef class Mandelbrot(object):
    """Clasical Mandelbrot Function, realy slow on python, so have some patience"""

    cdef object surface
    cdef int width
    cdef int height
    cdef np.ndarray array2d

    def __init__(self, surface):
        """
        (pygame.Surface) surface - surface to draw on
        """
        self.surface = surface
        # set some values
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.array2d = pygame.surfarray.array2d(self.surface)
        self.initialize()
        print "done" 

    cdef initialize(self, float left=-2.1, float right=0.7, float bottom=-1.2, float top=1.2, int maxiter=30):
        """
        initialize pixelarray with color value,
        classical approach, really, really slow
        """
        cdef float x, xx, y, cx, cy, betrag, x2, y2
        cdef int interation, hx, hy
        cdef int itermax
        cdef float magnify
        cdef float stepy
        cdef float stepx
        cdef int color
        x = xx = y = cx = cy = betrag = x2 = y2 = 0.0
        iteration = hx = hy = 0
        itermax = 255		# how many iterations to do
        magnify=1.0		# no magnification
        stepy = (top - bottom) / self.height
        stepx = (right - left) / self.width
        cy = bottom
        for hy in xrange(self.height):
            cx = left
            for hx in xrange(self.width):
                x = cx
                y = cy
                iteration = 0
                betrag = 0.0 
                while (iteration < itermax) and (betrag < maxiter):
                    x2 = x * x
                    y2 = y * y
                    betrag = x2 + y2
                    xx = x2 - y2 + cx
                    y = 2.0 * x * y + cy
                    x = xx
                    iteration += 1
                color = (iteration << 16) + (iteration << 8) + iteration
                # color = pygame.Color(iteration, iteration, iteration)
                self.array2d[hx][hy] = color
                cx = cx + stepx
            cy = cy + stepy

    cpdef update(self):
        """blit pixelarray to surface"""
        pygame.surfarray.blit_array(self.surface, self.array2d)

def test():
    try:
        fps = 1
        surface = pygame.display.set_mode((800, 600))
        pygame.init()
        mandelbrot = Mandelbrot(surface)
        clock = pygame.time.Clock()       
        pause = False
        while True:
            clock.tick(fps)
            events = pygame.event.get()  
            for event in events:  
                if event.type == pygame.QUIT:  
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                if keyinput[pygame.K_ESCAPE]:
                    sys.exit(1)
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                mandelbrot.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'


if __name__ == '__main__':
    test()

