#!/usr/bin/python3

import pygame
import sys
import random
import numpy


class Fire(object):
    """
    Simulated Fire, 2d effect
    idea and basic algorithm from
    http://lodev.org/cgtutor/fire.html
    """

    def __init__(self, surface, rect, scale=4):
        """
        (pygame.surface) surface - to draw on
        (pygame.Rect) dest - rect to blit fire on
        (int) width - width of fire
        (int) height - height of fire
        (int) scale - scale fire
        """ 
        self.surface = surface
        self.rect = rect
        self.width = rect.width / scale
        self.height = rect.height / scale
        self.scale = scale
        # initialize values
        # scaled down surface
        self.drawsurface = pygame.Surface((self.width, self.height))
        self.drawsurface.fill((0, 0, 0))
        self.array2d = None
        self.fire = None
        self.palette = None
        self.initialize()

    def initialize(self):
        """generate palette and surface to draw intermdiate fire, also array"""
        # self.drawsurface.fill((0, 0, 0))
        self.array2d = pygame.surfarray.array2d(self.drawsurface)
        self.fire = numpy.zeros((self.width, self.height))
        # generate palette
        self.palette = numpy.zeros(255)
        # aplette should be something from black to yellow red
        self.palette[0] = pygame.Color(0, 0, 0, 255)
        for index in range(1, 255):
            color = pygame.Color(0, 0, 0, 255)
            # original C Comments
            # Hue goes from 0 to 85: red to yellow
            # Saturation is always the maximum: 255
            # Lightness is 0..100 for x=0..128, and 255 for x=128..255
            # color = HSLtoRGB(ColorHSL(x / 3, 255, std::min(255, x * 2)));
            color.hsla = (index, 100, index / 2.55, 10)
            self.palette[index] = color

    def update(self):
        """update every frame"""
        w = self.width
        h = self.height
        # random baseline
        for x in range(w):
            self.fire[x][h - 1] = abs(32768 + random.randint(0, 32768)) % 256
        # calculate each pixel according to neighbours
        for y in range(h - 1):
            for x in range(w):
                # every new point depends on O Points
                #    N
                #   OOO
                #    O
                self.fire[x][y] = \
                    ((self.fire[(x - 1) % w][(y + 1) % h] \
                    + self.fire[(x) % w][(y + 2) % h] \
                    + self.fire[(x + 1) % w][(y + 1) % h] \
                    + self.fire[(x) % w][(y + 3) % h]) \
                    * 16) / 65
                # the last factor 16/65 should be slightly larger than 4
                # and lesser than 5
                # closer to 4 will make flames higher
                self.array2d[x][y] = self.palette[int(self.fire[x][y])]
        pygame.surfarray.blit_array(self.drawsurface, self.array2d)
        # scale fire surface up to given size
        blitsurface = pygame.transform.scale(self.drawsurface, (self.width * self.scale, self.height * self.scale))
        self.surface.blit(blitsurface, self.rect)


def test():
    try:
        fps = 500
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        spheres = (
            Fire(surface, pygame.Rect(0, 0, 600, 600), 4), 
            )
        clock = pygame.time.Clock()       
        pause = False
        surface.fill((0, 0, 0))
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
                for thing in spheres:
                    thing.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'


if __name__ == '__main__':
    import sys
    import os
    import cProfile
    import pstats
    profile = os.path.basename(sys.argv[0].split(".")[0])
    cProfile.runctx( "test()", globals(), locals(), filename=profile)
    s = pstats.Stats(profile)
    s.sort_stats('time')
    s.print_stats(0.1)
    os.unlink(profile)
