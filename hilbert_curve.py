#!/usr/bin/python3

import sys
import pygame
import math
from HilbertCurve import HilbertCurve as HilbertCurve
from Vec2d import Vec2d as Vec2d

class HilbertCurvePy(object):
    """Basic Hilbert Curve Algorithm"""

    def __init__(self, surface, iteration=6, length=6):
        self.surface = surface
        # Which iteration of the Hilbert curve to draw
        self.iteration = iteration
        # Length of each line in the Hilbert curve
        self.length = length
        self.pos = Vec2d(self.surface.get_width() - 10, 10)
        self.color = pygame.Color(238, 255, 0)
        self.angle = 0
        self.deg2rad = math.pi / 180

    def forward(self, distance):
        myangle = self.angle * self.deg2rad
        dest = self.pos + Vec2d(math.cos(myangle), math.sin(myangle)) * (-distance)
        pygame.draw.line(self.surface, self.color, self.pos, dest)
        self.pos = dest

    def right(self, angle):
        self.angle -= angle

    def left(self, angle):
        self.right(-angle)

    def leftHilbert(self, l, w):
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

    def rightHilbert(self, l, w):
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

    def update(self):
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
