#!/usr/bin/python

import pygame
import sys
import os
import math
import time
from SinusText import SinusText as SinusText
from Plasma import Plasma as Plasma
from PlasmaFractal import PlasmaFractal as PlasmaFractal
from CoffeeBean import CoffeeDraw as CoffeeDraw
import Utils3d
from Mesh import Mesh as Mesh

def test():
    try:
        fps = 50
        surface = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
        print pygame.display.Info()
        pygame.init()
        things = (
                {"start" : 0, "stop" : 10,
                    "class" : SinusText(surface, "SimpleDemo by GunnerySergeant", 200, 20, 1, pygame.Color(0,255,255))},
                {"start" : 10, "stop" : 20,
                    "class" : SinusText(surface, "Start with some Plasma Effect", 200, 30, 2, pygame.Color(0,255,255)),},
                {"start" : 20, "stop": 30,
                    "class" : Plasma(surface, scale=4),},
                {"start" : 30, "stop" : 40,
                    "class" : SinusText(surface, "a nice PlasmaFractal Effect", 200, 30, 2, pygame.Color(0,255,255)),},
                {"start" : 40, "stop": 50,
                    "class" : PlasmaFractal(surface, scale=4),},
                {"start" : 50, "stop" : 60,
                    "class" : SinusText(surface, "some sice coffeebean graphics, don't know why its so called, do you?", 200, 30, 2, pygame.Color(0,255,255)),},
                {"start" : 70, "stop" : 80,
                    "class" : CoffeeDraw(surface),},
                {"start" : 90, "stop" : 100,
                    "class" : SinusText(surface, "no demo without rotating cubes ...", 200, 20, 2, pygame.Color(0,128,255)),},
                {"start" : 90, "stop" : 100,
                    "class" : SinusText(surface, "no demo without rotating cubes ...", 190, 30, 4, pygame.Color(0,128,255)),},
                {"start" : 100, "stop": 110,
                    "class" :
                    Mesh(
                        surface,
                        origin=(300, 300), 
                        transformations=
                            Utils3d.get_rot_matrix(
                                Utils3d.get_scale_rot_matrix(
                                    scale_tuple=(600,600,1), 
                                    aspect_tuple=(16, 9),
                                    shift_tuple=(0, 0, -10)),
                                degrees=(1, 2, 3),
                                steps=360),
                        polygons = Utils3d.get_cube_polygons())},
                {"start" : 109, "stop" : 120,
                "class" : SinusText(surface, "greetings to all, who are better demomakers than i", 200, 30, 2, pygame.Color(0,255,255)),},
         
            )
        clock = pygame.time.Clock()       
        # mark pause state 
        pause = False
        # fill background
        surface.fill((0, 0, 0, 255))
        running = True
        frames = 0
        starttime = time.time()
        while running:
            # limit to FPS
            clock.tick(fps)
            # Event Handling
            events = pygame.event.get()  
            for event in events:  
                if event.type == pygame.QUIT:  
                    running = False
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                # print keyinput
                if keyinput[pygame.K_ESCAPE]:
                    running = False
            runtime = int(time.time() - starttime)
            # Update Graphics
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                for thing in things:
                    if thing["start"] < runtime < thing["stop"]:
                        thing["class"].update()
                pygame.display.update()
                # pygame.display.flip()
            frames += 1
        duration = time.time() - starttime
        print "Done %s frames in %s seconds, %s frames/s" % (frames, duration, frames/duration)
    except KeyboardInterrupt:
        print 'shutting down'

if __name__ == "__main__":
    test()
    sys.exit(1)
    import pstats
    import cProfile
    profile = "Plasma.profile"
    cProfile.runctx( "test()", globals(), locals(), filename=profile)
    s = pstats.Stats(profile)
    s.sort_stats('time')
    s.print_stats(1.0)
    os.unlink(profile)
