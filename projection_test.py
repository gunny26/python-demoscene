#!/usr/bin/python3

import pygame
import sys
import math
import time
import numpy as np
DTYPE = np.float64
# own modules
#from Vector import Vector as Vector
#from Matrix3d import Matrix3d as Matrix3d
#from Utils3d import Utils3d as Utils3d
import Utils3d
from Polygon import Polygon as Polygon
#from Mesh import Mesh as Mesh

class Mesh(object):
    """abstract class to represent mesh of polygons"""

    def __init__(self, surface, origin, transformations=None, polygons=None):
        """
        pygame surface to draw on
        center positon of mesh in 2d space
        """
        self.surface = surface
        (self.origin_x, self.origin_y) = origin
        self.frames = 0
        # initialze list of transformations applied to every face
        self.transformations = transformations
        self.len_transformations = len(transformations)
        # initialize list of polygons for this mesh
        self.polygons = polygons

    def update(self):
        """
        called on every frame
        apply transformation matrix and project every polygon to 2d
        for color avg_z function is used
        polygons are sorted on avg_z value

        finally painting on surface is called
        """
        # light from above
        light_position = np.array((0.0, 0.0, 10.0, 1.0), dtype=DTYPE)
        # apply linear transformations to vetices
        # daw faces fom lowe z to higher
        transformation = self.transformations[self.frames % self.len_transformations]
        color = pygame.Color(200, 200, 200, 255)
        for polygon in self.polygons:
            # apply transformation to every vertice in polygon
            newpolygon = polygon.transform(transformation)
            # get new position vector
            pos_vec = newpolygon.get_position_vector()
            # calculate vector from face to lightsource
            v_light = pos_vec - light_position
            # get the normal of the face
            normal = newpolygon.get_normal_faster()
            # calculate angle between face normal and vector to light source
            light_angle = Utils3d.angle_to(normal, v_light)
            # angle to light source in radians, between 0 and math.pi
            normal_color = int(light_angle * 255 / math.pi)
            #avg_z = max(min(abs(int(newface.get_avg_z() * 10)), 255), 0) 
            color = pygame.Color(normal_color, normal_color, normal_color, 255)
            pygame.draw.polygon(self.surface, color, newpolygon.projected(self.origin_x, self.origin_y), 1)
        self.frames += 1


def test():
    """test"""
    try:
        total_starttime = time.time()
        #fps = 150
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        cube = [Polygon(Utils3d.get_rectangle_points()), ]
        objects = []
        stepper = -0.1
        for x in range(100):
            objects.append(
                Mesh(
                    surface,
                    origin=(300, 300), 
                    transformations=(
                        Utils3d.get_shift_matrix(0, 0, stepper).dot(
                            Utils3d.get_scale_matrix(100,100,1).dot(
                                Utils3d.get_rot_z_matrix(x*math.pi/180))),),
                    polygons = cube)
            )
            stepper -= 0.1
        clock = pygame.time.Clock()       
        pause = False
        color = pygame.Color(255, 255, 255, 255)
        print "Matrix precalculations done in %s seconds" % (time.time()-total_starttime)
        anim_starttime = time.time()
        frames = 0
        while True:
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
            frames += 1 
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

