#!/usr/bin/python3

import sys
import pygame
import random
import cProfile
import time
import numpy
# own modules
from Vec2dFast import Vec2d
#from Vec3d import Vec3d


class Thing(object):
    """
    the thing at starting point moves randomly
    """

    def __init__(self, surface, universe, pos2d, color):
        self.surface = surface
        self.universe = universe
        self.position = pos2d
        # define some additional variables
        self.direction = Vec2d(random.random(), random.random())
        self.color = pygame.Color(128, 128, 128, 255)
        self.next_direction = self.direction
        self.next_position = None

    def update(self):
        # sum up all directions to every other particle
        #print sum(self.get_direction_to(other) for other in self.universe.things)
        #    direction = self.get_direction_to(other)
        #    self.next_direction.x += direction.x
        #    self.next_direction.y += direction.y
        # multiply by timescaler, to get fast movement also on slow
        # computers
        self.next_direction = self.next_direction.normalized() * self.universe.timescale
        self.next_position = self.position + self.next_direction
        self.check_boundaries() # inside visible area
        if not self.check_reserved(): # is the new position already used
            self.position = self.next_position
        self.direction = self.next_direction
        self.surface.set_at((int(self.position.x), int(self.position.y)), self.color)

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

    def check_reserved(self):
        """
        check if on new position there is some other element
        if yes, stop
        """
        if self.surface.get_at((int(self.next_position.x), int(self.next_position.y))) != self.universe.empty:
        #if new_position in self.universe.positions:
            return True
        return False

    def check_boundaries(self):
        """
        check if position is outside of visible surface,
        and change direction accordingly
        """
        if not (0 < self.next_position.x < self.surface.get_width()):
            self.next_direction.x *= -1
            self.next_position.x = self.position.x
        if not (0 < self.next_position.y < self.surface.get_height()):
            self.next_direction.y *= -1
            self.next_position.y = self.position.y

    def get_direction_to(self, other):
        return self.position - other.position

    def get_distance_to(self, other):
        return self.get_direction_to(other).length()


class Neutron(Thing):
    """
    the thing at starting point moves randomly
    """

    def __init__(self, surface, universe, pos2d, color):
        Thing.__init__(self, surface, universe, pos2d, color)
        self.color = pygame.Color(0, 0, 255, 255)
        self.kind = "Neutron"

    def get_direction_to(self, other):
        if other.kind == self.kind:
            return self.position - other.position
        return other.position - self.position


    def get_distance_to(self, other):
        return self.get_direction_to(other).length()


class Proton(Thing):
    """
    the thing at starting point moves randomly
    """

    def __init__(self, surface, universe, pos2d, color):
        Thing.__init__(self, surface, universe, pos2d, color)
        self.color = pygame.Color(0, 255, 0, 255)
        self.kind = "Proton"

    def get_direction_to(self, other):
        # wants to neutron
        if other.kind != self.kind:
            return self.position - other.position
        return other.position - self.position

    def get_distance_to(self, other):
        return self.get_direction_to(other).length()


class Electron(Thing):
    """
    the thing at starting point moves randomly
    """

    def __init__(self, surface, universe, pos2d, color):
        Thing.__init__(self, surface, universe, pos2d, color)
        self.color = pygame.Color(255, 0, 0, 255)
        self.kind = "Electron"

    def get_distance_to(self, other):
        return self.get_direction_to(other).length

    def get_direction_to(self, other):
        # wants to pronton
        if other.kind == "Proton":
            return self.position - other.position
        elif other.kind == "Neutron":
            return Vec2d(0, 0)
        else:
            return other.position - self.position



class Universe(object):
    """Universe with Things"""

    kinds = (Proton, Electron, Neutron)
    #kinds = (Proton, )

    def __init__(self, surface, number, speed=0.01):
        """
        surface = pygame.Surface
        stars - amount of strar to create
        depth - z axis depth from 0 to 0+depth
        speed - how fast should stars travel
        """
        self.surface = surface
        self.number = number
        self.speed = speed
        # set initial variables
        self.color = pygame.Color(255, 255, 255, 255)
        self.empty = pygame.Color(0, 0, 0, 255) # indicates empty place
        # initialize array
        self.things = []
        self.positions = []
        # initial text surface to get points from
        self.font = pygame.font.SysFont("mono", 20, bold=True)
        self.text_surface = self.font.render("AM", True, self.color)
        self.number = self.text_surface.get_width() * self.text_surface.get_height()
        print "There are %d points in Textsurface" % self.number
        self.timestamp = 1
        self.fps = 1.0 / 30.0
        self.lasttime = None
        self.timescale = None
        # initialize universe
        self.generate()

    def generate(self):
        zoom = Vec2d(10, 10)
        pan = Vec2d(200, 100)
        """ generates 3d starfield, z=0 to z=depth """
        for x in range(self.text_surface.get_width()):
            for y in range(self.text_surface.get_height()):
                color = self.text_surface.get_at((x, y))
                if color != pygame.Color(255, 255, 255, 0):
                    print "Found non-black color %s at %s x %s" % (color, x, y)
                    kind = int(random.random() * len(self.kinds))
                    pos2d = Vec2d(x, y) * zoom + pan
                    new_thing = self.kinds[kind](self.surface, self, pos2d, self.color)
                    self.things.append(self.kinds[kind](self.surface, self, pos2d, self.color))
                    self.positions.append(new_thing.position)
        print "Placed %d things in universe" % len(self.things)
        self.lasttime = time.time()

    def update(self, fov=2, viewer_distance=256):
        """update every frame"""
        duration = time.time() - self.lasttime
        self.timescale = self.fps / duration
        #print "Duration %f fps should %f Timescale %f" % (duration, self.fps, self.timescale)
        #parray = pygame.surfarray.pixels2d(surface)
        for thing in self.things:
            thing.update()
        self.timestamp += 1
        self.lasttime = time.time()

def main():
    """test"""
    try:
        fps = 255
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        # create universe
        universe = Universe(surface, number=50, speed=0.01)
        clock = pygame.time.Clock()
        # for 3d projection
        fov = 1
        max_running_time = time.time() + 30
        viewer_distance = 256
        pause = False
        starttime = time.time()
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
                    break
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
                universe.update(viewer_distance=viewer_distance, fov=fov)
                pygame.display.flip()
            if time.time() > max_running_time:
                break
        print "Last observed universe timestamp %d" % universe.timestamp
        print "Took %f seconds" % (time.time() - starttime)
        print "Took %f per frame at %f fps" % ((time.time() - starttime) / universe.timestamp, universe.timestamp/(time.time() - starttime))
    except KeyboardInterrupt:
        print 'shutting down'

if __name__ == "__main__":
    cProfile.run("main()")
    #main()
