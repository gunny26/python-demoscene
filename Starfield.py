#!/usr/bin/python3

import sys
import pygame
import random
# own modules
from Vec2d import Vec2d
from Vec3d import Vec3d


class Starfield(object):
    """Starfield with 3D Points"""

    def __init__(self, surface, stars, depth, speed=0.01):
        """
        surface = pygame.Surface
        stars - amount of strar to create
        depth - z axis depth from 0 to 0+depth
        speed - how fast should stars travel
        """
        self.surface = surface
        self.stars = stars
        self.depth = depth
        self.speed = speed
        # set initial variables
        self.color = pygame.Color(255, 255, 255, 255)
        # initialize array
        self.generate()

    def generate(self):
        """ generates 3d starfield, z=0 to z=depth """
        depth_count = self.stars / self.depth
        self.stars = []
        for index in range(depth_count ** 3):
            star_x = random.random() * 4 - 2
            star_y = random.random() * 4 - 2
            star_z = random.random() * 4 - 2
            self.stars.append(Vec3d(star_x, star_y, star_z))

    def update(self, fov=2, viewer_distance=256):
        """update every frame"""
        #parray = pygame.surfarray.pixels2d(surface)
        for star in self.stars:
            tstar = star.project(self.surface.get_width(), self.surface.get_height(), \
                viewer_distance, fov)
            tstar2d = Vec2d(tstar.x, tstar.y)
            pygame.draw.line(self.surface, self.color, tstar2d, tstar2d, 1)
            star.x -= self.speed
            if star.x < -2:
                star.x = 2

def test():
    """test"""
    try:
        fps = 50
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        spheres = (
            Starfield(surface, stars=100, depth=10, speed=0.01),
            )
        clock = pygame.time.Clock()       
        # for 3d projection
        fov = 1
        viewer_distance = 256
        pause = False
        while True:
            clock.tick(fps)
            events = pygame.event.get()  
            for event in events:  
                if event.type == pygame.QUIT:  
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                # print keyinput
                if keyinput[pygame.K_ESCAPE]:
                    sys.exit(1)
                if keyinput[pygame.K_UP]:
                    viewer_distance += 1
                if keyinput[pygame.K_DOWN]:
                    viewer_distance -= 1
                if keyinput[pygame.K_PLUS]:
                    fov += .1
                if keyinput[pygame.K_MINUS]:
                    fov -= .1
                if keyinput[pygame.K_p]:
                    pause = not pause
                if keyinput[pygame.K_r]:
                    viewer_distance = 256
                    fov = 2
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                for thing in spheres:
                    # draw
                    thing.update(viewer_distance=viewer_distance, fov=fov)
                pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'

if __name__ == "__main__":
    test()
