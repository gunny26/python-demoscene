#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
# own modules
from Vector import Vector as Vector
from Matrix3d import Matrix3d as Matrix3d
from Polygon import Polygon as Polygon

cpdef project(vec1, int win_width, int win_height, double fov, double viewer_distance):
    cdef double factor
    cdef double x
    cdef double y
    factor = fov / (viewer_distance + vec1[2])
    x = vec1[0] * factor + win_width / 2
    y = -vec1[1] * factor + win_height / 2
    return(Vector.from_tuple(x, y, 1))

cpdef get_identity_matrix():
    return(Matrix3d(np.eye(3, dtype=np.float32)))

cpdef get_rot_x_matrix(double theta):
    """return rotation matrix around x axis
    return rotated version of self around X-Axis
    theta should be given in radians
    http://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
    |1     0           0| |x|   |        x        |   |x'|
    |0   cos θ    -sin θ| |y| = |y cos θ - z sin θ| = |y'|
    |0   sin θ     cos θ| |z|   |y sin θ + z cos θ|   |z'|
    """
    cdef double cos
    cdef double sin
    cos = math.cos(theta)
    sin = math.sin(theta)
    return(Matrix3d.from_row_vectors(
        Vector.from_tuple(1,    0,   0),
        Vector.from_tuple(0,  cos, sin),
        Vector.from_tuple(0, -sin, cos)))

cpdef get_rot_z_matrix(double theta):
    """
    return rotated version of self around Z-Axis
    theta should be given in radians
    http://stackoverflow.com/questions/1 4607640/rotating-a-vector-in-3d-space
    |cos θ   -sin θ   0| |x|   |x cos θ - y sin θ|   |x'|
    |sin θ    cos θ   0| |y| = |x sin θ + y cos θ| = |y'|
    |  0       0      1| |z|   |        z        |   |z'|
    """
    cdef double cos
    cdef double sin
    cos = math.cos(theta)
    sin = math.sin(theta)
    return(Matrix3d.from_row_vectors(
        Vector.from_tuple(cos, -sin, 0),
        Vector.from_tuple(sin,  cos, 0),
        Vector.from_tuple(  0,    0, 1)))

cpdef get_rot_y_matrix(double theta):
    """
    return rotated version of self around Y-Axis
    theta should be given in radians
    http://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
    | cos θ    0   sin θ| |x|   | x cos θ + z sin θ|   |x'|
    |     0    1       0| |y| = |         y        | = |y'|
    |-sin θ    0   cos θ| |z|   |-x sin θ + z cos θ|   |z'|
    """
    cdef double cos
    cdef double sin
    cos = math.cos(theta)
    # substitute sin with cos, but its not clear if this is faster
    # sin² + cos² = 1
    # sin = sqrt(1.0 - cos)
    sin = math.sin(theta)
    return(Matrix3d.from_row_vectors(
        Vector.from_tuple( cos, 0, sin),
        Vector.from_tuple(   0, 1,   0),
        Vector.from_tuple(-sin, 0, cos)
        ))

cpdef get_rot_align(vector1, vector2):
    """
    return rotation matrix to rotate vector1 such that

    T(vector1) = vector2

    remember order of vectors:
    vector1 is the vector to be transformed, not vector 2

    so vector1 is aligned with vector2
    to do this efficiently, vector1 and vector2 have to be unit vectors
    look at this website to get detailed explanation of what is done here
    http://www.iquilezles.org/www/articles/noacos/noacos.htm
    """
    # make sure, that bot vectors are unit vectors
    #assert vector1.length_sqrd() == 1
    #assert vector2.length_sqrd() == 1
    cdef double dot
    cdef double k
    cross = vector2.cross(vector1)
    dot = vector2.dot(vector1)
    k = 1.0 / (1.0 + dot)
    return(Matrix3d.from_row_vectors(
        Vector.from_tuple(cross[0] * cross[0] * k + dot    , cross[1] * cross[0] * k - cross[2], cross[2] * cross[0] * k + cross[1]),
        Vector.from_tuple(cross[1] * cross[1] * k + cross[2], cross[1] * cross[1] * k + dot    , cross[2] * cross[1] * k - cross[0]),
        Vector.from_tuple(cross[2] * cross[2] * k - cross[1], cross[1] * cross[2] * k + cross[0], cross[2] * cross[2] * k + dot),
        ))

cpdef get_shift_matrix(double x, double y, double z):
    """
    return transformation matrix to shift vector
    | 0  0  0  x|
    | 0  0  0  y|
    | 0  0  0  z|
    | 0  0  0  1|
    """
    return(Matrix3d.from_row_vectors(
        Vector.from_tuple( x, 0, 0),
        Vector.from_tuple( 0, y, 0),
        Vector.from_tuple( 0, 0, z),
        ))

cpdef get_shift_vector(double x, double y, double z):
    """
    return transformation matrix to shift vector
    | 0  0  0  x|
    | 0  0  0  y|
    | 0  0  0  z|
    | 0  0  0  1|
    """
    return(Vector.from_tuple( x, y, z))

cpdef get_scale_matrix(double x, double y, double z):
    """
    return transformation matrix to scale vector
    | x  0  0  0|
    | 0  y  0  0|
    | 0  0  z  0|
    | 0  0  0  1|
    """
    return(Matrix3d.from_row_vectors(
        Vector.from_tuple( x, 0, 0),
        Vector.from_tuple( 0, y, 0),
        Vector.from_tuple( 0, 0, z),
        ))

cpdef get_rectangle_points():
    """basic rectangle vertices"""
    points = [
        Vector.from_tuple(-1,  1, 0),
        Vector.from_tuple( 1,  1, 0),
        Vector.from_tuple( 1, -1, 0),
        Vector.from_tuple(-1, -1, 0),
        Vector.from_tuple(-1,  1, 0),
        ]
    return(points)

cpdef get_triangle_points():
    """basic triangle vertices"""
    points = [
        Vector.from_tuple(-1,  0, 0),
        Vector.from_tuple( 0,  1, 0),
        Vector.from_tuple( 1,  0, 0),
        Vector.from_tuple(-1,  0, 0),
        ]
    return(points)

cpdef get_pyramid_polygons():
    cdef list polygons = []
    # front
    face = Polygon(get_triangle_points())
    face.itransform(get_rot_x_matrix(-math.pi/4))
    face.itransform(get_shift_matrix(0, 0, 1))
    polygons.append(face)
    # back
    face = Polygon(get_triangle_points())
    face.itransform(get_rot_x_matrix(math.pi/4))
    face.itransform(get_shift_matrix(0, 0, -1))
    polygons.append(face)
    # left
    face = Polygon(get_triangle_points())
    face.itransform(get_rot_x_matrix(-math.pi/4))
    face.itransform(get_rot_y_matrix(-math.pi/2))
    face.itransform(get_shift_matrix(1, 0, 0))
    polygons.append(face)
    # right
    face = Polygon(get_triangle_points())
    face.itransform(get_rot_x_matrix(-math.pi/4))
    face.itransform(get_rot_y_matrix(math.pi/2))
    face.itransform(get_shift_matrix(-1, 0, 0))
    polygons.append(face)

cpdef get_cube_polygons():
    # a cube consist of six faces
    # left
    cdef list polygons = []
    face = Polygon(get_rectangle_points())
    face.itransform(get_rot_y_matrix(math.pi/2))
    face.itransform(get_shift_matrix(-1, 0, 0))
    polygons.append(face)
    # right
    face = Polygon(get_rectangle_points())
    face.itransform(get_rot_y_matrix(math.pi/2))
    face.itransform(get_shift_matrix(1, 0, 0))
    polygons.append(face)
    # bottom
    face = Polygon(get_rectangle_points())
    face.itransform(get_rot_x_matrix(math.pi/2))
    face.itransform(get_shift_matrix(0, -1, 0))
    polygons.append(face)
    # top
    face = Polygon(get_rectangle_points())
    face.itransform(get_rot_x_matrix(math.pi/2))
    face.itransform(get_shift_matrix(0, 1, 0))
    polygons.append(face)
    # front
    face = Polygon(get_rectangle_points())
    face.itransform(get_shift_matrix(0, 0, -1))
    polygons.append(face)
    # back
    face = Polygon(get_rectangle_points())
    face.itransform(get_shift_matrix(0, 0, 1))
    polygons.append(face)
    return(polygons)

cpdef get_scale_rot_matrix(scale, shift, aspect):
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
    # assert len(scale) == 3
    # assert len(shift) == 3
    # assert len(aspect) == 2
    cdef double aspect_ratio
    scale_matrix = get_scale_matrix(*scale)
    shift_matrix = get_shift_matrix(*shift)
    aspect_ratio = aspect[0] / aspect[1]
    alt_basis = Matrix3d.from_row_vectors(
        Vector.from_tuple(1, 0, 0),
        Vector.from_tuple(0, aspect_ratio, 0),
        Vector.from_tuple(0, 0, 1),
        )
    alt_basis_inv = alt_basis.inverse()
    # combine scale and change of basis to one transformation
    # static matrix
    static_transformation = shift_matrix + alt_basis_inv.mul_matrix(scale_matrix)
    return(static_transformation)

cpdef get_rot_matrix(static_transformation, tuple degrees, int steps):
    """
    static_transformation of type Matrix3d, will be applied to every step
    degrees of type tuple, for every axis one entry in degrees
    steps of type int, how many steps to precalculate
    """
    #assert len(degrees) == 3
    #assert type(steps) == int
    #assert isinstance(static_transformation, Matrix3d)
    cdef double angle_x
    cdef double angle_y
    cdef double angle_z
    cdef int step
    cdef list transformations
    cdef double deg2rad = math.pi / 180
    cdef double factor
    transformations = []
    for step in range(steps):
        factor = step * deg2rad
        angle_x = degrees[0] * factor
        angle_y = degrees[1] * factor
        angle_z = degrees[2] * factor
        # this part of tranformation is calculate on every step
        transformation = get_rot_z_matrix(angle_z).mul_matrix(
                get_rot_x_matrix(angle_x).mul_matrix(
                    get_rot_y_matrix(angle_y)))
        # combine with static part of transformation
        transformations.append(static_transformation.mul_matrix(transformation))
    return(transformations)


