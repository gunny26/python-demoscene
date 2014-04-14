#!/usr/bin/python
#

import sys
import pygame

class Mandelbrot(object):
    """Clasical Mandelbrot Function, realy slow on python, so have some patience"""

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

    def initialize(self, left=-2.1, right=0.7, bottom=-1.2, top=1.2, maxiter=30):
        """
        initialize pixelarray with color value,
        classical approach, really, really slow
        """
        x = xx = y = cx = cy = betrag = x2 = y2 = None
        iteration = hx = hy = None
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
                betrag = 0 
                while (iteration < itermax) and (betrag < maxiter):
                    x2 = x * x
                    y2 = y * y
                    betrag = x2 + y2
                    xx = x2 - y2 + cx
                    y = 2.0 * x * y + cy
                    x = xx
                    iteration += 1
                self.array2d[hx][hy] = pygame.Color(iteration, iteration, iteration)
                cx = cx + stepx
            cy = cy + stepy

    def update(self):
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

