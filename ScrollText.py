#!/usr/bin/python3

import pygame
import sys

class ScrollText(object):
    """Simple 2d Scrolling Text"""
    
    def __init__(self, surface, text, hpos, color, size=30):
        """
        (pygame.Surface) surface - surface to draw on
        (string) text - text to draw
        (int) hpos - horizontal position on y axis
        (pygame.Color) color - color of font
        (int) size - size of font
        """
        self.surface = surface
        # prepend and append some blanks
        appendix = " " * (self.surface.get_width() / size)
        self.text = appendix + text + appendix
        self.hpos = hpos
        self.color = color
        self.size = size
        # initialize
        self.position = 0
        self.font = pygame.font.SysFont("mono", self.size, bold=True)
        self.text_surface = self.font.render(self.text, True, self.color)

    def update(self, hpos=None):
        """update every frame"""
        if hpos is not None:
            self.hpos = hpos
        self.surface.blit(self.text_surface, 
            (0, self.hpos), 
            (self.position, 0, self.surface.get_width(), self.size)
        )
        if self.position < self.text_surface.get_width():
            self.position += 1
        else:
            self.position = 0


def test():
    try:
        fps = 25
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        spheres = (
            ScrollText(surface, "Dolor Ipsum Dolor uswef", 400, pygame.Color(255,255,0)),
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
                    thing.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'

if __name__ == '__main__':
    test()

