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

    def __init__(self, surface, universe, pos2d, color):
        self.surface = surface
        self.universe = universe
        self.pos2d = pos2d
        self.mass = random.random()
        print self.mass
        self.acceleration = random.random()
        self.direction = Vec2d(random.random(), random.random()) * self.mass
        self.color = pygame.Color(int(128 + 127 * self.mass), 0, 0, 255)

    def draw(self, viewer_distance, fov):
        color = pygame.Color(int(255 * self.mass), int(255 * self.acceleration), 0, 255)
        pygame.draw.line(self.surface, color, self.pos2d, self.pos2d, 2)

    def update(self):
        #print self.pos3d
        new_direction = self.direction
        for other_thing in self.universe.things:
            if other_thing == self:
                continue
            #if int(other_thing.pos2d.x) == int(self.pos2d.x) and int(other_thing.pos2d.y) == int(self.pos2d.y):
            #    self.mass += other_thing.mass
            #    print "removing %s" % other_thing
            #    self.universe.things.remove(other_thing)
            #    continue
            direction = other_thing.get_direction_to(self)
            new_direction += direction * other_thing.mass
        #pygame.draw.line(self.surface, pygame.Color(0, 0, 255, 0), self.pos2d, self.pos2d + new_direction.normalized() * 10, 1)
        #self.acceleration *= (1 - self.mass)
        self.check_boundaries()
        self.pos2d += (new_direction * self.acceleration).normalized()

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
        return nearest_thing

    def check_boundaries(self):
        """
        check if position is outside of visible surface,
        and change direction accordingly
        """
        newpos = self.pos2d + self.direction
        if (newpos.x < 0) or (newpos.x > self.surface.get_width()):
            self.direction.x *= -1
        if (newpos.y < 0) or (newpos.y > self.surface.get_height()):
            self.direction.y *= -1

    def get_direction_to(self, other):
        return self.pos2d - other.pos2d

    def get_distance_to(self, other):
        return self.get_direction_to(other).length

class Neutron(Thing):
    """
    the thing at starting point moves randomly
    """

    def __init__(self, surface, universe, pos2d, color):
        Thing.__init__(self, surface, universe, pos2d, color)
        self.kind = "Proton"

    def draw(self, viewer_distance, fov):
        color = pygame.Color(0, 0, int(255 * self.mass), int(255 * self.acceleration))
        pygame.draw.line(self.surface, color, self.pos2d, self.pos2d, 2)


    def get_direction_to(self, other):
        return Vec2d(0.0, 0.0)

    def get_distance_to(self, other):
        return self.get_direction_to(other).length



class Proton(Thing):
    """
    the thing at starting point moves randomly
    """

    def __init__(self, surface, universe, pos2d, color):
        Thing.__init__(self, surface, universe, pos2d, color)
        self.kind = "Proton"

    def draw(self, viewer_distance, fov):
        color = pygame.Color(0, int(255 * self.mass), int(255 * self.acceleration), 255)
        pygame.draw.line(self.surface, color, self.pos2d, self.pos2d, 2)


    def get_direction_to(self, other):
        if other.kind != self.kind:
            return self.pos2d - other.pos2d
        return other.pos2d - self.pos2d

    def get_distance_to(self, other):
        return self.get_direction_to(other).length


class Electron(Thing):
    """
    the thing at starting point moves randomly
    """

    def __init__(self, surface, universe, pos2d, color):
        Thing.__init__(self, surface, universe, pos2d, color)
        self.kind = "Electron"

    def get_direction_to(self, other):
        if other.kind != self.kind:
            return self.pos2d - other.pos2d
        return other.pos2d - self.pos2d

    def get_distance_to(self, other):
        return self.get_direction_to(other).length


class Universe(object):
    """Universe with Things"""

    kinds = (Proton, Electron, Neutron)

    def __init__(self, surface, stars, speed=0.01):
        """
        surface = pygame.Surface
        stars - amount of strar to create
        depth - z axis depth from 0 to 0+depth
        speed - how fast should stars travel
        """
        self.surface = surface
        self.stars = stars
        self.speed = speed
        # set initial variables
        self.color = pygame.Color(255, 255, 255, 255)
        # initialize array
        self.things = []
        self.generate()

    def generate(self):
        """ generates 3d starfield, z=0 to z=depth """
        for index in range(self.stars):
            index = int(random.random() * len(self.kinds))
            pos2d = Vec2d(random.random() * self.surface.get_width(), random.random() * self.surface.get_height())
            self.things.append(self.kinds[index](self.surface, self, pos2d, self.color))

    def update(self, fov=2, viewer_distance=256):
        """update every frame"""
        #parray = pygame.surfarray.pixels2d(surface)
        for thing in self.things:
            thing.update()
            thing.draw(viewer_distance, fov)

def main():
    """test"""
    try:
        fps = 30
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        spheres = (
            Universe(surface, stars=50, speed=0.01),
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
