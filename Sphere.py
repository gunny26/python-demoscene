#!/usr/bin/python3

import pygame
import sys
import math
from Vec2d import Vec2d
from Vec3d import Vec3d

class Sphere(object):
    """Object represents a sphere"""

    def __init__(self, surface, color, center=Vec3d(0, 0, 0), size=Vec3d(1, 1, 1), steps=10.0, viewer_distance=256, fov=2):
        """just init"""
        # get parameters
        self.surface = surface
        self.color = color
        self.center = center
        self.size = size
        self.steps = steps
        self.viewer_distance = viewer_distance
        self.fov = fov
        # set parameters and variables
        self.sphere_raw_points = []
        self.generate()
        self.sphere_points = None
        self.transformed_sphere = None
        self.resize_and_center()

    def generate(self):
        """generate normalized array of sphere points"""
        radius = 0.0
        for y in self.step_generator(-1, 1, self.steps):
            circle = []
            # c**2 = a**2 + b**2
            radius = math.sqrt(1 - y**2)
            for angle in self.step_generator(0, 2 * math.pi, self.steps):
                x = math.cos(angle) * radius
                z = math.sin(angle) * radius
                circle.append(Vec3d(x, y, z))
            self.sphere_raw_points.append(circle)
        

    def resize_and_center(self):
        """calculate actual sphere from normalized array"""
        self.sphere_points = []
        for circle in self.sphere_raw_points:
            new_circle = []
            for point in circle:
                new_circle.append(point * self.size + self.center)
            self.sphere_points.append(new_circle)

    def set_color(self, color):
        """set color"""
        self.color = color

    def set_size(self, size=Vec3d(1, 1, 1)):
        """set size of sphere"""
        self.size = size
        self.resize_and_center()

    def set_center(self, center=Vec3d(0, 0, 0)):
        """set center of sphere"""
        self.center = center
        self.resize_and_center()

    def rotate(self, dx, dy, dz, offset2d=Vec2d(0, 0)):
        """rotate sphere and generate transformed 2d point array for polygon"""
        # rotate and project every point to 2d
        self.transformed_sphere = []
        for circle in self.sphere_points:
            transformed_circle = []
            for point in circle:
                new_point = point.rotated_around_x(dx).rotated_around_y(dy).rotated_around_z(dz)
                transformed = new_point.project(self.surface.get_width(), self.surface.get_height(), self.viewer_distance, self.fov)
                transformed_circle.append((transformed.x + offset2d.x, transformed.y + offset2d.y))
            self.transformed_sphere.append(transformed_circle)
                
    def update(self, viewer_distance, fov):
        """update every frame, given transformation parameters"""
        # draw every face of the cube
        self.viewer_distance = viewer_distance
        self.fov = fov
        for circle in self.transformed_sphere:
            pygame.draw.polygon(self.surface, self.color, circle, 1)
        for point_index in range(len(self.transformed_sphere[0])):
            points = []
            for circle_index in range(len(self.transformed_sphere)):
                points.append(self.transformed_sphere[circle_index][point_index])
            pygame.draw.polygon(self.surface, self.color, points, 1)

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
            Sphere(surface, (100, 0, 0), Vec3d(-1.5, -1.5, 1.5), Vec3d(1, 1, 1)),
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
