#!/usr/bin/python
#

import sys
import pygame
import random
import math

class PlasmaFractal2(object):
    """Plasma Generator"""

    def __init__(self, surface):
        """
        (pygame.Surface) surface - surface to draw on
        """
        self.surface = surface
        # set some values
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.roughness = random.randint(2, 5)
        self.data = [[0 for y in range(self.height)] for x in range(self.width)]
        self.array2d = pygame.surfarray.array2d(self.surface)
        self.initialize()
        print "done" 

    def adjust(self, xa, ya, x, y, xb, yb):
        if (self.data[x][y] == 0):
          d = math.fabs(xa - xb) + math.fabs(ya - yb)
          v = (self.data[xa][ya] + self.data[xb][yb]) / 2.0 \
             + (random.random() - 0.5) * d * self.roughness
          c = int(math.fabs(v) % 256)
          self.data[x][y] = c

    def subdivide(self, x1, y1, x2, y2):
        if (not ((x2 - x1 < 2.0) and (y2 - y1 < 2.0))):
            x = int((x1 + x2) / 2.0)
            y = int((y1 + y2) / 2.0)
            self.adjust(x1, y1, x, y1, x2, y1)
            self.adjust(x2, y1, x2, y, x2, y2)
            self.adjust(x1, y2, x, y2, x2, y2)
            self.adjust(x1, y1, x1, y, x1, y2)
            if(self.data[x][y] == 0):
                v = int((self.data[x1][y1] + self.data[x2][y1]) \
                   + self.data[x2][y2] + self.data[x1][y2]) / 4.0
                self.data[x][y] = v
            self.subdivide(x1, y1, x, y)
            self.subdivide(x, y1, x2, y)
            self.subdivide(x, y, x2, y2)
            self.subdivide(x1, y, x, y2)

    def initialize(self):
        ## {{{ http://code.activestate.com/recipes/577113/ (r1)
        # plasma.py
        # plasma fractal
        # FB - 201003147
        self.data[0][0] = random.randint(0, 255)
        self.data[self.width - 1][0] = random.randint(0, 255)
        self.data[self.width - 1][self.height - 1] = random.randint(0, 255)
        self.data[0][self.height - 1] = random.randint(0, 255)
        self.subdivide(0, 0, self.width - 1, self.height - 1)
        for y in range(self.height):
            for x in range(self.width):
                self.array2d[x][y] = pygame.Color(0, int(self.data[x][y]), 100)
        ## end of http://code.activestate.com/recipes/577113/ }}}

    def update(self):
        """blit pixelarray to surface"""
        pygame.surfarray.blit_array(self.surface, self.array2d)


def test():
    try:
        fps = 1
        pygame.init()
        surface = pygame.display.set_mode((800, 600))
        print pygame.display.Info()
        thing = PlasmaFractal2(surface)
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
                # surface.fill((0, 0, 0))
                thing.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'


if __name__ == '__main__':
    test()

