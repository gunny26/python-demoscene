#!/usr/bin/python3

from __future__ import division
import pygame
import sys
import math
import time
import numpy as np
# own modules
#from Vector import Vector as Vector
#from Matrix3d import Matrix3d as Matrix3d
#from Utils3d import Utils3d as Utils3d
import Utils3d
#from Polygon import Polygon as Polygon
from Mesh import Mesh as Mesh

def test():
    """test"""
    try:
        total_starttime = time.time()
        fps = 15
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        cube = Utils3d.get_cube_polygons()
        objects = []
        objects.append(
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
                polygons = cube)
        )
        clock = pygame.time.Clock()       
        pause = False
        color = pygame.Color(255, 255, 255, 255)
        print "Matrix precalculations done in %s seconds" % (time.time()-total_starttime)
        anim_starttime = time.time()
        frames = 1000
        while frames > 0:
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

