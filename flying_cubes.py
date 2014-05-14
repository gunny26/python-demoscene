#!/usr/bin/python3

import pygame
import sys
import math
import time
import numpy as np
# own modules
import Utils3d
import Transformer
from Mesh import Mesh as Mesh

def test():
    """test"""
    try:
        total_starttime = time.time()
        #fps = 150
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        cube = Utils3d.get_cube_polygons()
        objects = []
        for y in range(100, 500, 50):
            for x in range(100, 500, 50):
                objects.append(
                    Mesh(
                        surface,
                        origin=(300, 300), 
                        transformations = Transformer.flying_cubes_t(x, y),
                        polygons = cube)
                )
        clock = pygame.time.Clock()       
        pause = False
        color = pygame.Color(255, 255, 255, 255)
        print "Matrix precalculations done in %s seconds" % (time.time()-total_starttime)
        anim_starttime = time.time()
        frames = 100
        while frames > 0:
            #clock.tick(fps)
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
                # clear screen
                surface.fill((0, 0, 0, 255))
                for thing in objects:
                    thing.update()
                pygame.display.flip()
            frames -= 1
        duration = time.time() - anim_starttime
        print "Done 100 Frames in %f seonds, average %f fps" % (duration, 100/duration)
        print "Whole program duration %f seconds" % (time.time()-total_starttime)
    except KeyboardInterrupt:
        print 'shutting down'

if __name__ == "__main__":
    test()
    sys.exit(0)
    import cProfile
    import pstats
    profile = "profiles/%s.profile" % sys.argv[0].split(".")[0]
    cProfile.runctx( "test()", globals(), locals(), filename=profile)
    s = pstats.Stats(profile)
    s.sort_stats('time')
    s.print_stats()

