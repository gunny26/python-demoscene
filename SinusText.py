#!/usr/bin/python3

import pygame
import sys
import math

class SinusText(object):
    """Sinus wave scroll text"""

    def __init__(self, surface, text, hpos, amplitude, frequency, color, size=30):
        """
        (pygame.Surface) surface to draw on
        (string) text - text to draw
        (int) hpos - horizontal position on y axis
        (int) amplitude - amplitude of sinus wave
        (int) frequency - frequency of sinus wave
        (pygame.Color) color - color of font
        (int) size - size of font
        """
        self.surface = surface
        # prepend an append some spaces
        appendix = " " * (self.surface.get_width() / size)
        self.text = appendix + text + appendix
        self.hpos = hpos
        self.amplitude = amplitude
        self.frequency = frequency
        self.color = color
        self.size = size
        # initialize
        self.font = None
        self.text_surface = None
        self.initialize()
        # position in rendered string
        self.position = 0
        # radian to degree
        self.factor = 2 * math.pi / self.surface.get_width()

    def initialize(self):
        """generate initial position"""
        self.font = pygame.font.SysFont("mono", self.size, bold=True)
        self.text_surface = self.font.render(self.text, True, self.color)

    def update(self, hpos=None):
        """
        update every frame
        (int)hpos y axis offset
        """
        if hpos is not None:
            self.hpos = hpos
        for offset in range(self.text_surface.get_width()):
            self.surface.blit( \
                self.text_surface, \
                (0 + offset, self.hpos + math.sin(offset * self.frequency * self.factor) * self.amplitude), \
                (self.position + offset, 0, 1, self.size) \
            )
        if self.position < self.text_surface.get_width():
            self.position += 1
        else:
            self.position = 0
 

def test():
    try:
        fps = 50
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        spheres = (
            SinusText(surface, "Dolor Ipsum Dolor uswef", 200, 30, 2, pygame.Color(0,255,255)),
            )
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
                for thing in spheres:
                    thing.update(hpos=None)
                pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'

if __name__ == '__main__':
    test()
