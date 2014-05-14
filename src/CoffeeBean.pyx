#!/usr/bin/python3

import sys
import pygame
from pygame import gfxdraw
import noise

class Bean(object):
    """represents one colored line"""

    def __init__(self, surface, beans, parameter_dict):
        """
        (pygame.Surface) surface - surface to draw on
        (list) beans - list of beans to remove self when velocity is 0
        (dict) parameter_dict - dictionary of parameters
        """
        self.surface = surface
        self.beans = beans
        self.x = None
        self.y = None
        self.x_off = None
        self.y_off = None
        self.__dict__.update(parameter_dict)
        self.vel = 3 # or option vel
        self.accel = -0.003 # or option accel
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.color = pygame.Color(0, 0, 0, 0)

    def draw(self):
        """draw line"""
        if self.vel < 0 :
            # remove self
            self.beans.remove(self)
        # original 0.0007
        self.x_off += 0.0007
        self.y_off += 0.0007
        self.vel += self.accel
        self.x += noise.pnoise1(self.x_off, octaves=8) * self.vel - self.vel / 2
        self.y += noise.pnoise1(self.y_off, octaves=8) * self.vel - self.vel / 2
        # set color
        h = abs(noise.pnoise1((self.x_off + self.y_off) / 2)) * 360
        self.color.hsva = (h, 100, 100, 4)
        pygame.gfxdraw.pixel(self.surface, int(self.x) % self.width, int(self.y) % self.height, self.color)


cdef class CoffeeDraw(object):
    """draws nice colored lines on surface"""

    cdef object surface
    cdef list beans
    cdef int framecount

    def __init__(self, surface):
        """
        (pygame.Surface) surface - surface to draw on
        """
        self.surface = surface
        # initialize
        self.beans = []
        self.framecount = 1

    cpdef update(self):
        """update every frame"""
        cdef float x_off
        cdef float y_off
        cdef float x
        cdef float y
        self.framecount += 1
        x_off = self.framecount * 0.0003
        y_off = x_off + 20
        x = noise.pnoise1(x_off, octaves=8) * self.surface.get_width()
        y = noise.pnoise1(y_off, octaves=8) * self.surface.get_height()
        # every 8th frame a new bean
        if self.framecount % 2 == 0:
            self.beans.append(Bean(self.surface, self.beans, { 
                "x" : x, 
                "y" : y, 
                "x_off" : x_off, 
                "y_off" : y_off}))
        for bean in self.beans:
            bean.draw()

def test():
    """ test """
    fps = 50
    surface = pygame.display.set_mode((600, 400))
    pygame.init()
    clock = pygame.time.Clock()
    coffee_draw = CoffeeDraw(surface)
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
