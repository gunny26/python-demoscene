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

    def __init__(self, surface, origin):
        """
        pygame surface to draw on
        center positon of mesh in 2d space
        """
        self.surface = surface
        self.origin = origin
        self.frames = 0
        self.transformations = []
        self.faces = []
        # initialze mash
        self.initialize_points()
        # initialize a number of transformations on every polygon
        self.initialize_transformations()

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
        apply transormation matrix and project every polygon to 2d
        for color avg_z function is used
        polygons are sorted on avg_z value
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
            color = pygame.Color(normal_color, normal_color, avg_z, 255)
            pygame.draw.polygon(self.surface, color, newface.projected(shift=self.origin), 0)
        self.frames += 1 

class TriangleBase(Mesh):

    def __init__(self, surface, origin):
        Mesh.__init__(self, surface, origin)

    def initialize_points(self):
        face = Polygon(Utils3d.get_triangle_points())
        self.faces.append(face)


class PyramideBase(Mesh):

    def __init__(self, surface, origin):
        Mesh.__init__(self, surface, origin)

    def initialize_points(self):
        # front
        face = Polygon(Utils3d.get_triangle_points())
        face.itransform(Utils3d.get_rot_x_matrix(-math.pi/4))
        face.itransform(Utils3d.get_shift_matrix(0, 0, 1))
        self.faces.append(face)
        # back
        face = Polygon(Utils3d.get_triangle_points())
        face.itransform(Utils3d.get_rot_x_matrix(math.pi/4))
        face.itransform(Utils3d.get_shift_matrix(0, 0, -1))
        self.faces.append(face)
        # left
        face = Polygon(Utils3d.get_triangle_points())
        face.itransform(Utils3d.get_rot_x_matrix(-math.pi/4))
        face.itransform(Utils3d.get_rot_y_matrix(-math.pi/2))
        face.itransform(Utils3d.get_shift_matrix(1, 0, 0))
        self.faces.append(face)
        # right
        face = Polygon(Utils3d.get_triangle_points())
        face.itransform(Utils3d.get_rot_x_matrix(-math.pi/4))
        face.itransform(Utils3d.get_rot_y_matrix(math.pi/2))
        face.itransform(Utils3d.get_shift_matrix(-1, 0, 0))
        self.faces.append(face)

class PyramideRotXYZ(PyramideBase):

    def __init__(self, surface, origin):
        PyramideBase.__init__(self, surface, origin)

    def initialize_transformations(self):
        """
        this method can be subclassed to apply different transformations
        to original cube vertices

        in this example there are 360 transformations
        """
        # scale and change basis, and shift
        scale_matrix = Utils3d.get_scale_matrix(300, 300, 1)
        shift_matrix = Utils3d.get_shift_matrix(0, 0, -20)
        alt_basis = Matrix3d(
            Vector(1, 0, 0, 0),
            Vector(0, 16/9, 0, 0),
            Vector(0, 0, 1, -10),
            Vector(0 ,0 ,0 ,1),
            )
        alt_basis_inv = alt_basis.inverse()
        # combine scale and change of basis to one transformation
        # static matrix
        static_transformation = alt_basis_inv.mul_matrix(scale_matrix)
        for angle in range(360):
            rectangle = []
            rad_angle = angle * math.pi / 180
            # this part of tranformation is calculated on every step
            transformation = Utils3d.get_rot_y_matrix(rad_angle)
            # combine with static part of transformation
            self.transformations.append(static_transformation.mul_matrix(transformation))



class TriangleRotXYZ(TriangleBase):

    def __init__(self, surface, origin):
        TriangleBase.__init__(self, surface, origin)

    def initialize_transformations(self):
        """
        this method can be subclassed to apply different transformations
        to original cube vertices

        in this example there are 360 transformations
        """
        # scale and change basis, and shift
        scale_matrix = Utils3d.get_scale_matrix(400, 400, 1)
        shift_matrix = Utils3d.get_shift_matrix(0, 0, -15)
        alt_basis = Matrix3d(
            Vector(1, 0, 0, 0),
            Vector(0, 16/9, 0, 0),
            Vector(0, 0, 1, -10),
            Vector(0 ,0 ,0 ,1),
            )
        alt_basis_inv = alt_basis.inverse()
        # combine scale and change of basis to one transformation
        # static matrix
        static_transformation = alt_basis_inv.mul_matrix(scale_matrix)
        for angle in range(360):
            rectangle = []
            rad_angle = angle * math.pi / 180
            # this part of tranformation is calculated on every step
            transformation = Utils3d.get_rot_z_matrix(rad_angle).mul_matrix(
                    Utils3d.get_rot_x_matrix(rad_angle).mul_matrix(
                        Utils3d.get_rot_y_matrix(rad_angle)))
            # combine with static part of transformation
            self.transformations.append(static_transformation.mul_matrix(transformation))


class CubeBase(Mesh):
    """
    cube is a specific representation of Mesh
    this clas only defines faces for cube
    transformations are done in specific classes
    """

    def __init__(self, surface, origin):
        Mesh.__init__(self, surface, origin)

    def initialize_points(self):
        # a cube consist of six faces
        # left
        face = Polygon(Utils3d.get_rectangle_points())
        face.itransform(Utils3d.get_rot_y_matrix(math.pi/2))
        face.itransform(Utils3d.get_shift_matrix(-1, 0, 0))
        self.faces.append(face)
        # right
        face = Polygon(Utils3d.get_rectangle_points())
        face.itransform(Utils3d.get_rot_y_matrix(math.pi/2))
        face.itransform(Utils3d.get_shift_matrix(1, 0, 0))
        self.faces.append(face)
        # bottom
        face = Polygon(Utils3d.get_rectangle_points())
        face.itransform(Utils3d.get_rot_x_matrix(math.pi/2))
        face.itransform(Utils3d.get_shift_matrix(0, -1, 0))
        self.faces.append(face)
        # top
        face = Polygon(Utils3d.get_rectangle_points())
        face.itransform(Utils3d.get_rot_x_matrix(math.pi/2))
        face.itransform(Utils3d.get_shift_matrix(0, 1, 0))
        self.faces.append(face)
        # front
        face = Polygon(Utils3d.get_rectangle_points())
        face.itransform(Utils3d.get_shift_matrix(0, 0, -1))
        self.faces.append(face)
        # back
        face = Polygon(Utils3d.get_rectangle_points())
        face.itransform(Utils3d.get_shift_matrix(0, 0, 1))
        self.faces.append(face)


class CubeRotXYZ(CubeBase):
    """a Circle in 3D Space"""

    def __init__(self, surface, origin):
        CubeBase.__init__(self, surface, origin)

    def initialize_transformations(self):
        """
        this method can be subclassed to apply different transformations
        to original cube vertices

        in this example there are 360 transformations
        """
        # scale and change basis, and shift
        scale_matrix = Utils3d.get_scale_matrix(400, 400, 1)
        shift_matrix = Utils3d.get_shift_matrix(0, 0, -15)
        alt_basis = Matrix3d(
            Vector(1, 0, 0, 0),
            Vector(0, 16/9, 0, 0),
            Vector(0, 0, 1, -5),
            Vector(0 ,0 ,0 ,1),
            )
        alt_basis_inv = alt_basis.inverse()
        # combine scale and change of basis to one transformation
        # static matrix
        static_transformation = alt_basis_inv.mul_matrix(scale_matrix)
        for angle in range(360):
            rectangle = []
            rad_angle = angle * math.pi / 180
            # this part of tranformation is calculated on every step
            transformation = Utils3d.get_rot_z_matrix(rad_angle).mul_matrix(
                    Utils3d.get_rot_x_matrix(rad_angle).mul_matrix(
                        Utils3d.get_rot_y_matrix(rad_angle)))
            # combine with static part of transformation
            self.transformations.append(static_transformation.mul_matrix(transformation))


class CubeRotX(CubeBase):

    def __init__(self, surface, origin):
        CubeBase.__init__(self, surface, origin)

    def initialize_transformations(self):
        """
        this method can be subclassed to apply different transformations
        to original cube vertices

        in this example there are 360 transformations
        """
        # scale and change basis, and shift
        scale_matrix = Utils3d.get_scale_matrix(200, 200, 1)
        alt_basis = Matrix3d(
            Vector(1, 0, 0, 0),
            Vector(0, 16/9, 0, 0),
            Vector(0, 0, 1, -10),
            Vector(0 ,0 ,0 ,1),
            )
        alt_basis_inv = alt_basis.inverse()
        # combine scale and change of basis to one transformation
        # static matrix
        static_transformation = alt_basis_inv.mul_matrix(scale_matrix)
        for angle in range(360):
            rectangle = []
            rad_angle = angle * math.pi / 180
            # this part of tranformation is calculate on every step
            transformation = Utils3d.get_rot_x_matrix(rad_angle)
            # combine with static part of transformation
            self.transformations.append(static_transformation.mul_matrix(transformation))

class CubeRotY(CubeBase):

    def __init__(self, surface, origin):
        CubeBase.__init__(self, surface, origin)

    def initialize_transformations(self):
        """
        this method can be subclassed to apply different transformations
        to original cube vertices

        in this example there are 360 transformations
        """
        # scale and change basis, and shift
        scale_matrix = Utils3d.get_scale_matrix(200, 200, 1)
        alt_basis = Matrix3d(
            Vector(1, 0, 0, 0),
            Vector(0, 16/9, 0, 0),
            Vector(0, 0, 1, -10),
            Vector(0 ,0 ,0 ,1),
            )
        alt_basis_inv = alt_basis.inverse()
        # combine scale and change of basis to one transformation
        # static matrix
        static_transformation = alt_basis_inv.mul_matrix(scale_matrix)
        for angle in range(360):
            rectangle = []
            rad_angle = angle * math.pi / 180
            # this part of tranformation is calculate on every step
            transformation = Utils3d.get_rot_y_matrix(rad_angle)
            # combine with static part of transformation
            self.transformations.append(static_transformation.mul_matrix(transformation))

class CubeRotZ(CubeBase):

    def __init__(self, surface, origin):
        CubeBase.__init__(self, surface, origin)

    def initialize_transformations(self):
        """
        this method can be subclassed to apply different transformations
        to original cube vertices

        in this example there are 360 transformations
        """
        # scale and change basis, and shift
        scale_matrix = Utils3d.get_scale_matrix(200, 200, 1)
        alt_basis = Matrix3d(
            Vector(1, 0, 0, 0),
            Vector(0, 16/9, 0, 0),
            Vector(0, 0, 1, -10),
            Vector(0 ,0 ,0 ,1),
            )
        alt_basis_inv = alt_basis.inverse()
        # combine scale and change of basis to one transformation
        # static matrix
        static_transformation = alt_basis_inv.mul_matrix(scale_matrix)
        for angle in range(360):
            rectangle = []
            rad_angle = angle * math.pi / 180
            # this part of tranformation is calculate on every step
            transformation = Utils3d.get_rot_z_matrix(rad_angle)
            # combine with static part of transformation
            self.transformations.append(static_transformation.mul_matrix(transformation))


def test():
    """test"""
    try:
        fps = 50
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        objects = (
            #CubeRotX(surface, origin=(150, 300)),
            #CubeRotY(surface, origin=(300, 300)),
            #CubeRotZ(surface, origin=(450, 300)),
            CubeRotXYZ(surface, origin=(300, 150)),
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
