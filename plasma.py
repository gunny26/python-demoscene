#!/usr/bin/python

import pygame
import sys
import os
import math
import time
from Plasma import Plasma as Plasma

def test():
    try:
        fps = 50
        surface = pygame.display.set_mode((400, 225))
        print pygame.display.Info()
        pygame.init()
        things = (
                {   "start": 0,
                    "stop": 999,
                    "class" : Plasma(surface, scale=2),
                },
            )
        clock = pygame.time.Clock()       
        # mark pause state 
        pause = False
        # fill background
        surface.fill((0, 0, 0, 255))
        running = True
        frames = 0
        starttime = time.time()
        while running and frames < 100:
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
