#!/usr/bin/python3

import pygame
import sys
import math
# own modules
from Vec2d import Vec2d
from Vec3d import Vec3d


class Circle(object):
    """a Circle in 3D Space"""

    def __init__(self, surface, color, center=Vec3d(0, 0, 0), size=Vec3d(1, 1, 1), steps=36.0, viewer_distance=256, fov=2):
        self.surface = surface
        self.color = color
        self.size = size
        self.center = center
        self.steps = steps
        self.viewer_distance = viewer_distance
        self.fov = fov
        # class variables
        self.circle_raw_points = []
        self.circle = None
        self.transformed_circle = None
        # generate master circle radius 1.0 no rotation
        self.generate()
        self.resize_and_center()

    def generate(self):
        """generate master circle"""
        radius = 1.0
        # draw circle in x-z plane at y=0
        y = 0.0
        for angle in self.step_generator(0, 2 * math.pi, self.steps):
            x = math.cos(angle) * radius
            z = math.sin(angle) * radius
            self.circle_raw_points.append(Vec3d(x, y, z))
        
    def resize_and_center(self):
        """recenter and resize master circle"""
        self.circle = []
        for point in self.circle_raw_points:
            self.circle.append(point * self.size + self.center)

    def set_color(self, color):
        """setter for self.color"""
        self.color = color

    def set_size(self, size=Vec3d(1, 1, 1)):
        """sets size and resizes circle"""
        self.size = size
        self.resize_and_center()

    def set_center(self, center=Vec3d(0, 0, 0)):
        """sets center and recenters circle"""
        self.center = center
        self.resize_and_center()

    def rotate(self, dx, dy, dz, offset2d=Vec2d(0, 0)):
        """rotates circle points and generates tranformed point array in 2d"""
        # rotate and project every point to 2d
        self.transformed_circle = []
        for point in self.circle:
            new_point = point.rotated_around_x(dx).rotated_around_y(dy).rotated_around_z(dz)
            transformed = new_point.project(self.surface.get_width(), self.surface.get_height(), self.viewer_distance, self.fov)
            self.transformed_circle.append((transformed.x + offset2d.x, transformed.y + offset2d.y))
                
    def update(self, viewer_distance, fov):
        """drawing"""
        self.viewer_distance = viewer_distance
        self.fov = fov
        pygame.draw.polygon(self.surface, self.color, self.transformed_circle, 1)

    @staticmethod
    def step_generator(start, stop, steps):
        """yields steps values between start and stop for float values"""
        distance = stop - start
        step = float(distance) / float(steps)
        value = float(start)
        while value <= stop:
            yield value
            value += step


def test():
    """test"""
    try:
        fps = 50
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        theta = 1
        step = math.pi / 180
        spheres = (
            Circle(surface, (100, 0, 0), Vec3d(-1.5, -1.5, 1.5), Vec3d(1, 1, 1)),
            )
        clock = pygame.time.Clock()       
        # for 3d projection
        fov = 1
        viewer_distance = 256
        pause = False
        color = pygame.Color(255, 255, 255, 255)
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
                    # rotate
                    thing.rotate(dx=theta, dy=theta, dz=0.0, offset2d=Vec2d(0, 0))
                    theta += step * 16
                    # color changing
                    thing.set_color(color=color)
                    # draw
                    thing.update(viewer_distance=viewer_distance, fov=fov)
                pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'

if __name__ == "__main__":
    test()
