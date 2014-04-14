#!/usr/bin/python3

import pygame
import sys
import math
import random
# own modules
from Vec2d import Vec2d


class Tree(object):
    """Tree in 2D"""

    def __init__(self, surface, color, root, depth, length):
        """
        (pygame.Surface) surface - to draw on
        (pygame.Color) color - to draw branches
        (Vec2d) root of tree root
        (int) depth - how many branches
        (int) length - length of initial branch
        """ 
        self.surface = surface
        self.color = color
        self.root = root
        self.depth = depth
        self.length = length
        # set initial variables
        # The number of branches each branch splits into
        self.branching_factor = 4
        # The angle between the branches in degrees
        self.angle_between_branches = 30
        # Controls how much smaller each level of the tree gets
        self.scale_factor = 0.7
        # actual angle in degree
        self.deg2rad = math.pi / 180
        # total angle between left and rightmost branch
        self.total_angle = self.angle_between_branches * (self.branching_factor - 1)
        # draw leafs or not
        self.leafs = True
        # hold every drawing operation, for update
        self.storyboard = []
        # initialize tree
        self.initialize()

    def draw(self, root, angle, length, width):
        """draw line from root with angle and length in width thickness"""
        assert isinstance(root, Vec2d)
        myangle = angle * self.deg2rad
        dest = root + Vec2d(math.cos(myangle), math.sin(myangle)) * (-length)
        self.storyboard.append((pygame.draw.line, (self.surface, self.color, root, dest, width)))
        # return new root point
        return(dest)

    def tree(self, depth, length, root, angle):
        """this method is recurdively called"""
        if depth == 0:
            if self.leafs is True:
                leaf_color = (random.randint(16, 65), int(length * 2 + 40), 0)
                self.storyboard.append((pygame.draw.ellipse, (self.surface, leaf_color, (int(root.x), int(root.y), 10, 10), 0)))
            return
        # forward
        root = self.draw(root, angle, length, self.depth / 2)
        # turn right
        angle -= self.total_angle / 2.0
        for i in range(self.branching_factor):
            # next recursion, smaller
            self.tree(depth - 1, length * self.scale_factor * (0.5 + random.random() * 0.5), root, angle)
            # turn left, one step
            angle += self.angle_between_branches
            # next branch
        # turn back right, and one step left
        angle -= self.total_angle / 2.0 + self.angle_between_branches
        # draw back
        root = self.draw(root, angle, -length, self.depth / 2)
        # we are at root

    def set_color(self, color):
        """set color"""
        self.color = color

    def initialize(self):
        """initialize tree"""
        self.tree(depth=self.depth, length=self.length, root=self.root, angle=90)

    def update(self):
        """update every frame"""
        for func, args in self.storyboard:
            func(*args)

def test():
    try:
        fps = 5
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        spheres = (
            Tree(surface, pygame.Color(255, 255, 0), Vec2d(300, 500), 8, 250),
            Tree(surface, pygame.Color(255, 255, 0), Vec2d(330, 500), 5, 100),
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
