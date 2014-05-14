#!/usr/bin/python3

import sys
import pygame
import math
import array

cdef class HilbertCurve(object):
    """Basic Hilbert Curve Algorithm"""

    cdef object surface
    cdef int iteration
    cdef int length
    cdef tuple pos
    cdef object color
    cdef int angle
    cdef float deg2rad
    cdef object sin
    cdef object cos

    def __init__(self, surface, int iteration=6, int length=6):
        self.surface = surface
        # Which iteration of the Hilbert curve to draw
        self.iteration = iteration
        # Length of each line in the Hilbert curve
        self.length = length
        self.pos = (self.surface.get_width() - 10, 10)
        self.color = pygame.Color(238, 255, 0)
        self.angle = 1
        self.deg2rad = math.pi / 180
        self.sin = array.array("f", [0.0] * 361)
        self.cos = array.array("f", [0.0] * 361)
        self.initialize()

    cdef initialize(self):
        deg2rad = math.pi / 180
        for degree in range(361):
            rad = degree * deg2rad
            self.sin[degree] = math.sin(rad)
            self.cos[degree] = math.cos(rad)

    cdef forward(self, int distance):
        dest = (self.pos[0] + self.cos[self.angle] * (-distance), self.pos[1] + self.sin[self.angle] * (-distance))
        pygame.draw.line(self.surface, self.color, self.pos, dest)
        self.pos = dest

    cdef right(self, int angle):
        self.angle -= angle
        if self.angle < 0:
            self.angle += 360
        elif self.angle > 360:
            self.angle -= 360

    cdef left(self, int angle):
        self.right(-angle)

    cdef leftHilbert(self, int l, int w):
        if l == 0:
            return
        self.right(90)
        self.rightHilbert(l - 1, w)
        self.forward(w)
        self.left(90)
        self.leftHilbert(l - 1, w)
        self.forward(w)
        self.leftHilbert(l - 1, w)
        self.left(90)
        self.forward(w)
        self.rightHilbert(l - 1, w)
        self.right(90)

    cdef rightHilbert(self, int l, int w):
        if l == 0:
            return
        self.left(90)
        self.leftHilbert(l - 1, w)
        self.forward(w)
        self.right(90)
        self.rightHilbert(l - 1, w)
        self.forward(w)
        self.rightHilbert(l - 1, w)
        self.right(90)
        self.forward(w)
        self.leftHilbert(l - 1, w)
        self.left(90)

    cpdef update(self):
        self.leftHilbert(self.iteration, self.length)


def test():
    """ test """
    fps = 1
    surface = pygame.display.set_mode((600, 400))
    pygame.init()
    clock = pygame.time.Clock()
    coffee_draw = HilbertCurve(surface)
    while True:
        clock.tick(fps)
        events = pygame.event.get()  
        for event in events:  
            if event.type == pygame.QUIT:  
                sys.exit(0)
        pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
        coffee_draw.update()
        pygame.display.update()

if __name__ == "__main__" :
    test()
