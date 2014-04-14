#!/usr/bin/python3

import pyximport
pyximport.install()
import pygame
import sys
import math
# cython to speed things up
# own modules
from Vec2d import Vec2d
from Vec3d import Vec3d
from Sphere import Sphere as Sphere
from Circle import Circle as Circle
from Starfield import Starfield as Starfield
from FireX import Fire as Fire
from Tree import Tree as Tree
from SinusText import SinusText as SinusText
from ScrollText import ScrollText as ScrollText
from InfoRenderer import InfoRenderer as InfoRenderer
from ColorGradient import ColorGradient as ColorGradient
from GradientBackground import GradientBackground as GradientBackground

def main():
    try:
        fps = 50
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        origin = (surface.get_width() / 2, surface.get_height() / 2)
        theta = 1
        step = math.pi / 180
        center_x = surface.get_width() / 2
        center_y = surface.get_height() / 2
        # Cube( surface, color, center3d, size)
        spheres = (
            Fire(surface, pygame.Rect(100, 100, 400, 200), 2), 
            Sphere(surface, (100, 0, 0), Vec3d(-1.5, -1.5, -1.5), Vec3d(1, 1, 1)),
            #Sphere(surface, (100, 0, 0), Vec3d(0, 0, 0), Vec3d(1, 1, 1)),
            #Sphere(surface, (100, 0, 0), Vec3d(1.5, 1.5, 1.5), Vec3d(1, 1, 1)),
            Circle(surface, (100, 0, 0), Vec3d(1.5, -1.5, -1.5), Vec3d(1, 1, 1)),
            Tree(surface, pygame.Color(0, 100, 100), Vec2d(300, 500), 5, 50),
            Tree(surface, pygame.Color(0, 100, 100), Vec2d(330, 500), 5, 100),
            Starfield(surface, stars=100, depth=10),
            InfoRenderer(surface, pygame.Color(0, 255, 0), pos=Vec2d(100,100), size=10),
            ScrollText(surface, "Dolor Ipsum Dolor uswef", 400, pygame.Color(255,255,0)),
            SinusText(surface, "Dolor Ipsum Dolor uswef", 200, 30, 2, pygame.Color(0,255,255)),
            )
        clock = pygame.time.Clock()       
 
        size_angle = 0
        size_angle_step = math.pi / 720
        cg = ColorGradient(0.0, 0.05, 0.05)
        background_gradient = GradientBackground(surface)
        # for 3d projection
        fov = 2
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
                #if keyinput[pygame.K_z]:
                #    theta[2] += math.pi / 180
                #if keyinput[pygame.KMOD_SHIFT | pygame.K_z]:
                #    theta[2] -= math.pi / 180
                #if keyinput[pygame.K_x]:
                #    theta[0] += math.pi / 180
                #if keyinput[pygame.KMOD_SHIFT | pygame.K_x]:
                #    theta[0] -= math.pi / 180
                #if keyinput[pygame.K_y]:
                #    theta[1] += math.pi / 180
                #if keyinput[pygame.KMOD_SHIFT | pygame.K_y]:
                #    theta[1] -= math.pi / 180
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
                background_gradient.update()
                for thing in spheres:
                    if type(thing) == InfoRenderer:
                        thing.update(lines=("viewer_distance : %f" % viewer_distance, "fov: %f" % fov))
                        continue
                    elif type(thing) == Tree:
                        thing.update()
                        continue
                    elif type(thing) in (Sphere, Circle, ):
                        # rotate
                        thing.rotate(dx=theta, dy=theta, dz=0.0, offset2d=Vec2d(0, 0))
                        theta += step * 16
                        # color changing
                        color = cg.get_color()
                        thing.set_color(color=color)
                        # size wobbling
                        # size_angle += size_angle_step
                        # thing.set_size(0.5 + math.sin(size_angle) * 0.125)
                        # draw
                        thing.update(viewer_distance=viewer_distance, fov=fov)
                        continue
                    elif type(thing) in (SinusText, ScrollText, ):
                        thing.update()
                    elif type(thing) == Tree:
                        thing.update(center=Vec2d(0, 0), viewer_distance=viewer_distance, fov=fov)
                    else:
                        thing.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'

if __name__ == '__main__':
    main()

