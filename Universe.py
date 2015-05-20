#!/usr/bin/python3

import sys
import pygame
import random
# own modules
from Vec2d import Vec2d
from Vec3d import Vec3d


class Thing(object):
    """
    the thing at starting point moves randomly
    """

    def __init__(self, surface, universe, pos3d, color):
        self.surface = surface
        self.universe = universe
        self.pos3d = pos3d
        self.mass = random.random()
        self.color = pygame.Color(int(128 + 127 * self.mass), 255, 255, 255)

    def draw(self, viewer_distance, fov):
        t_pos3d = self.pos3d.project(self.surface.get_width(), self.surface.get_height(), viewer_distance, fov)
        t_pos2d = Vec2d(t_pos3d.x, t_pos3d.y)
        pygame.draw.line(self.surface, self.color, t_pos2d, t_pos2d, 1)
        
    def update(self):
        #print self.pos3d
        new_direction = None
        for other_thing in self.universe.things:
            if other_thing == self:
                continue
            if other_thing.pos3d == self.pos3d:
                self.mass += other_thing.mass
                print "removing %s" % other_thing
                self.universe.remove(other_thing)
                continue
            direction = other_thing.get_direction_to(self)
            distance = direction.length
            if new_direction is None:
                new_direction = direction.normalized()
            else:
                new_direction = (new_direction + (direction * other_thing.mass)).normalized()
        self.pos3d += new_direction

    def get_nearest_thing(self):
        min_dist = None
        nearest_thing = None
        for other_thing in self.universe.things:
            if other_thing == self:
                continue
            direction = other_thing.get_direction_to(self)
            distance = direction.length
            if (min_dist is None) or (min_dist > distance):
                nearest_thing = other_thing
                min_dist = distance
        return(nearest_thing)

    def get_direction_to(self, other):
        return(other.pos3d - self.pos3d)

    def get_distance_to(self, other):
        return(self.get_direction_to().length)


class Universe(object):
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
        self.things = []
        self.generate()

    def generate(self):
        """ generates 3d starfield, z=0 to z=depth """
        depth_count = self.stars / self.depth
        for index in range(depth_count ** 3):
            star_x = random.random() * 4 - 2
            star_y = random.random() * 4 - 2
            star_z = random.random() * 4
            self.things.append(Thing(self.surface, self, Vec3d(star_x, star_y, star_z), self.color))

    def update(self, fov=2, viewer_distance=256):
        """update every frame"""
        #parray = pygame.surfarray.pixels2d(surface)
        for thing in self.things:
            thing.update()
            thing.draw(viewer_distance, fov)

def main():
    """test"""
    try:
        fps = 1000
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        spheres = (
            Universe(surface, stars=50, depth=10, speed=0.01),
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
    main()
