#!/usr/bin/python3

import pygame
import sys
import math
# own modules
from Vector import Vector as Vector
from Vector import Matrix3d as Matrix3d
from Vector import Utils3d as Utils3d
from Vector import Polygon as Polygon


class Mesh(object):
    """abstract class to represent mesh of polygons"""

    def __init__(self, surface, origin, transformations=None, polygons=None):
        """
        pygame surface to draw on
        center positon of mesh in 2d space
        """
        self.surface = surface
        self.origin = origin
        self.frames = 0
        if transformations is None:
            self.transformations = []
            self.initialize_transformations()
        else:
            self.transformations = transformations
        if polygons is None:
            self.faces = []
            self.initialize_points()
        else:
            self.faces = polygons
        # initialze mash
        #self.initialize_points()
        # initialize a number of transformations on every polygon

    def initialize_points(self):
        """
        fills self.faces with polygons
        """
        pass

    def initialize_transformations(self):
        """
        fill self.transformations with transformation
        matrices applied to every polygon.
        one transformation matrix for every frame
        """
        pass

    def update(self):
        """
        called on every frame
        apply transformation matrix and project every polygon to 2d
        for color avg_z function is used
        polygons are sorted on avg_z value

        finally painting on surface is called
        """
        # apply linear transformations to vetices
        for face in sorted(self.faces, reverse=True):
            newface = face.transform(self.transformations[self.frames % len(self.transformations)])
            # light from above
            light_position = Vector(0, 0, 10, 1)
            pos_vec = newface.get_position_vector()
            v_light = pos_vec - light_position
            normal = newface.get_normal()
            light_angle = normal.angle_to(v_light)

            # angle to light source in radians, between 0 and math.pi
            normal_color = int(light_angle * 255/math.pi)
            avg_z = max(min(abs(int(newface.get_avg_z() * 10)), 255), 0) 
            color = pygame.Color(normal_color, normal_color, normal_color, 255)
            pygame.draw.polygon(self.surface, color, newface.projected(shift=self.origin), 0)
        self.frames += 1 


class Transformer(object):

    @staticmethod
    def get_pyramid_polygons():
        polygons = []
        # front
        face = Polygon(Utils3d.get_triangle_points())
        face.itransform(Utils3d.get_rot_x_matrix(-math.pi/4))
        face.itransform(Utils3d.get_shift_matrix(0, 0, 1))
        polygons.append(face)
        # back
        face = Polygon(Utils3d.get_triangle_points())
        face.itransform(Utils3d.get_rot_x_matrix(math.pi/4))
        face.itransform(Utils3d.get_shift_matrix(0, 0, -1))
        polygons.append(face)
        # left
        face = Polygon(Utils3d.get_triangle_points())
        face.itransform(Utils3d.get_rot_x_matrix(-math.pi/4))
        face.itransform(Utils3d.get_rot_y_matrix(-math.pi/2))
        face.itransform(Utils3d.get_shift_matrix(1, 0, 0))
        polygons.append(face)
        # right
        face = Polygon(Utils3d.get_triangle_points())
        face.itransform(Utils3d.get_rot_x_matrix(-math.pi/4))
        face.itransform(Utils3d.get_rot_y_matrix(math.pi/2))
        face.itransform(Utils3d.get_shift_matrix(-1, 0, 0))
        polygons.append(face)

    @staticmethod
    def get_cube_polygons():
        # a cube consist of six faces
        # left
        polygons = []
        face = Polygon(Utils3d.get_rectangle_points())
        face.itransform(Utils3d.get_rot_y_matrix(math.pi/2))
        face.itransform(Utils3d.get_shift_matrix(-1, 0, 0))
        polygons.append(face)
        # right
        face = Polygon(Utils3d.get_rectangle_points())
        face.itransform(Utils3d.get_rot_y_matrix(math.pi/2))
        face.itransform(Utils3d.get_shift_matrix(1, 0, 0))
        polygons.append(face)
        # bottom
        face = Polygon(Utils3d.get_rectangle_points())
        face.itransform(Utils3d.get_rot_x_matrix(math.pi/2))
        face.itransform(Utils3d.get_shift_matrix(0, -1, 0))
        polygons.append(face)
        # top
        face = Polygon(Utils3d.get_rectangle_points())
        face.itransform(Utils3d.get_rot_x_matrix(math.pi/2))
        face.itransform(Utils3d.get_shift_matrix(0, 1, 0))
        polygons.append(face)
        # front
        face = Polygon(Utils3d.get_rectangle_points())
        face.itransform(Utils3d.get_shift_matrix(0, 0, -1))
        polygons.append(face)
        # back
        face = Polygon(Utils3d.get_rectangle_points())
        face.itransform(Utils3d.get_shift_matrix(0, 0, 1))
        polygons.append(face)
        return(polygons)

    @staticmethod
    def get_scale_rot_matrix(scale, shift, aspect):
        """
        create a affinde transformation matrix
    
        scale is of type tuple (200, 200, 1)
        shift is of type tuple (0, 0, -10)
        degreees of type tuple for everx axis steps in degrees
        aspect of type tuple to correct aspect ratios
        steps is of type int

        rotates around x/y/z in 1 degree steps and precalculates
        360 different matrices
        """
        # scale and change basis, and shift
        assert len(scale) == 3
        assert len(shift) == 3
        assert len(aspect) == 2
        scale_matrix = Utils3d.get_scale_matrix(*scale)
        shift_matrix = Utils3d.get_shift_matrix(*shift)
        aspect_ratio = aspect[0] / aspect[1]
        alt_basis = Matrix3d(
            Vector(1, 0, 0, 0),
            Vector(0, aspect_ratio, 0, 0),
            Vector(0, 0, 1, 0),
            Vector(0 ,0 ,0 ,1),
            )
        alt_basis_inv = alt_basis.inverse()
        # combine scale and change of basis to one transformation
        # static matrix
        static_transformation = shift_matrix.mul_matrix(alt_basis_inv.mul_matrix(scale_matrix))
        return(static_transformation)

    @staticmethod
    def get_rot_matrix(static_transformation, degrees, steps):
        """
        static_transformation of type Matrix3d, will be applied to every step
        degrees of type tuple, for every axis one entry in degrees
        steps of type int, how many steps to precalculate
        """
        assert len(degrees) == 3
        assert type(steps) == int
        assert isinstance(static_transformation, Matrix3d)
        transformations = []
        for step in range(steps):
            angle_x = step * degrees[0] * math.pi / 180
            angle_y = step * degrees[1] * math.pi / 180
            angle_z = step * degrees[2] * math.pi / 180
            # this part of tranformation is calculate on every step
            transformation = Utils3d.get_rot_z_matrix(angle_z).mul_matrix(
                    Utils3d.get_rot_x_matrix(angle_x).mul_matrix(
                        Utils3d.get_rot_y_matrix(angle_y)))
            # combine with static part of transformation
            transformations.append(static_transformation.mul_matrix(transformation))
        return(transformations)


def test():
    """test"""
    try:
        fps = 50
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        cube = Transformer.get_cube_polygons()
        objects = []
        for y in range(100, 500, 50):
            for x in range(100, 500, 50):
                objects.append(
                    Mesh(
                        surface,
                        origin=(x, y), 
                        transformations=
                            Transformer.get_rot_matrix(
                                Transformer.get_scale_rot_matrix(
                                    scale=(200,200,1), 
                                    shift=(0, 0, -20), 
                                    aspect=(16, 9)),
                                degrees=((x-y)/50, (y-x)/50, 3),
                                steps=360),
                        polygons = cube)
                )
        objects1 = (
            #CubeRotX(surface, origin=(150, 300)),
            #CubeRotY(surface, origin=(300, 300)),
            #CubeRotZ(surface, origin=(450, 300)),
            Mesh(
                surface,
                origin=(150, 300), 
                transformations=
                    Transformer.get_rot_matrix(
                        Transformer.get_scale_rot_matrix(
                            scale=(200,200,1), 
                            shift=(0, 0, -20), 
                            aspect=(16, 9)),
                        degrees=(1, 2, 3),
                        steps=360),
                polygons = cube),
             Mesh(
                surface,
                origin=(300, 300), 
                transformations=
                    Transformer.get_rot_matrix(
                        Transformer.get_scale_rot_matrix(
                            scale=(220, 220, 1), 
                            shift=(0, 0, -10), 
                            aspect=(16, 9)),
                        degrees=(3, 2, 1),
                        steps=360),
                polygons = cube),
            
            #CubeRotXYZ(surface, origin=(300, 450)),
            #TriangleRotXYZ(surface, origin=(150, 450)),
            #PyramideRotXYZ(surface, origin=(350, 450)),
            )
        clock = pygame.time.Clock()       
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
                # clear screen
                surface.fill((0, 0, 0, 255))
                for thing in objects:
                    thing.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'

if __name__ == "__main__":
    test()
