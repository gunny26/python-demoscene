#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
cimport numpy as np
DTYPE = np.float64
ctypedef np.float64_t DTYPE_t
# own modules
from Polygon import Polygon as Polygon

cpdef np.ndarray project(vec1, int win_width, int win_height, double fov, double viewer_distance):
    cdef double factor
    cdef double x
    cdef double y
    factor = fov / (viewer_distance + vec1[2])
    x = vec1[0] * factor + win_width / 2
    y = -vec1[1] * factor + win_height / 2
    return(np.array((x, y, 1), dtype=DTYPE))

cpdef np.ndarray get_identity_matrix():
    return(np.eye(4))

cpdef np.ndarray get_rot_x_matrix(double theta):
    """return rotation matrix around x axis
    return rotated version of self around X-Axis
    theta should be given in radians
    http://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
    |1     0           0| |x|   |        x        |   |x'|
    |0   cos θ    -sin θ| |y| = |y cos θ - z sin θ| = |y'|
    |0   sin θ     cos θ| |z|   |y sin θ + z cos θ|   |z'|
    """
    cdef double cos = math.cos(theta)
    cdef double sin = math.sin(theta)
    return(np.array((
        (1,    0,   0, 0),
        (0,  cos, sin, 0),
        (0, -sin, cos, 0),
        (0,    0,   0, 1)
        ), dtype=DTYPE))

cpdef np.ndarray get_rot_z_matrix(double theta):
    """
    return rotated version of self around Z-Axis
    theta should be given in radians
    http://stackoverflow.com/questions/1 4607640/rotating-a-vector-in-3d-space
    |cos θ   -sin θ   0| |x|   |x cos θ - y sin θ|   |x'|
    |sin θ    cos θ   0| |y| = |x sin θ + y cos θ| = |y'|
    |  0       0      1| |z|   |        z        |   |z'|
    """
    cdef double cos = math.cos(theta)
    cdef double sin = math.sin(theta)
    return(np.array((
        (cos, -sin, 0, 0),
        (sin,  cos, 0, 0),
        (  0,    0, 1, 0),
        (  0,    0, 0, 1)
        ), dtype=DTYPE))

cpdef np.ndarray get_rot_y_matrix(double theta):
    """
    return rotated version of self around Y-Axis
    theta should be given in radians
    http://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
    | cos θ    0   sin θ| |x|   | x cos θ + z sin θ|   |x'|
    |     0    1       0| |y| = |         y        | = |y'|
    |-sin θ    0   cos θ| |z|   |-x sin θ + z cos θ|   |z'|
    """
    cdef double cos = math.cos(theta)
    cdef double sin =  math.sin(theta)
    # substitute sin with cos, but its not clear if this is faster
    # sin² + cos² = 1
    # sin = sqrt(1.0 - cos)
    return(np.array((
        ( cos, 0, sin, 0),
        (   0, 1,   0, 0),
        (-sin, 0, cos, 0),
        (   0, 0,   0, 1)
        ), dtype=DTYPE))

cpdef np.ndarray get_rot_align(vector1, vector2):
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
    return(np.array((
        (cross[0] * cross[0] * k + dot     , cross[1] * cross[0] * k - cross[2], cross[2] * cross[0] * k + cross[1], 0),
        (cross[1] * cross[1] * k + cross[2], cross[1] * cross[1] * k + dot     , cross[2] * cross[1] * k - cross[0], 0),
        (cross[2] * cross[2] * k - cross[1], cross[1] * cross[2] * k + cross[0], cross[2] * cross[2] * k + dot,      0),
        (                                 0,                                  0,                                     1)
        ), dtype=DTYPE))

cpdef np.ndarray get_shift_matrix(double x, double y, double z):
    """
    return transformation matrix to shift vector
    | 1  0  0  sx| |x| |x+sx|
    | 0  1  0  sy| |y| |y+sy|
    | 0  0  1  sz|.|z|=|z+sz|
    | 0  0  0   1| |1| |   1|
    """
    return(np.array((
        (1, 0, 0, x), 
        (0, 1, 0, y), 
        (0, 0, 1, z),
        (0, 0, 0, 1)
        ), dtype=DTYPE))

cpdef np.ndarray get_scale_matrix(double x, double y, double z):
    """
    return transformation matrix to scale vector
    | x  0  0  0|
    | 0  y  0  0|
    | 0  0  z  0|
    | 0  0  0  1|
    """
    return(np.array((
        (x, 0, 0, 0),
        (0, y, 0, 0),
        (0, 0, z, 0),
        (0, 0, 0, 1)
        ), dtype=DTYPE))

cpdef np.ndarray get_rectangle_points():
    """basic rectangle vertices"""
    points = np.array([
        (-1,  1, 0, 1),
        ( 1,  1, 0, 1),
        ( 1, -1, 0, 1),
        (-1, -1, 0, 1),
        (-1,  1, 0, 1),
        ], dtype=DTYPE)
    return(points)

cpdef np.ndarray get_triangle_points():
    """basic triangle vertices"""
    points = np.array([
        (-1,  0, 0, 1),
        ( 0,  1, 0, 1),
        ( 1,  0, 0, 1),
        (-1,  0, 0, 1),
        ], dtype=DTYPE)
    return(points)

cpdef list get_pyramid_polygons():
    cdef list polygons = []
    # front
    face = get_triangle_points()
    transform = get_shift_matrix(0, 0, 1).dot(get_rot_x_matrix(-math.pi/4))
    face = face.dot(transform)
    face = face.dot(get_shift_matrix(0, 0, 1))
    polygons.append(Polygon(face))
    # back
    face = get_triangle_points()
    face = face.dot(get_rot_x_matrix(math.pi/4))
    face = face.dot(get_shift_matrix(0, 0, -1))
    polygons.append(Polygon(face))
    # left
    face = get_triangle_points()
    face = face.dot(get_rot_x_matrix(-math.pi/4))
    face = face.dot(get_rot_y_matrix(-math.pi/2))
    face = face.dot(get_shift_matrix(1, 0, 0))
    polygons.append(Polygon(face))
    # right
    face = get_triangle_points()
    face = face.dot(get_rot_x_matrix(-math.pi/4))
    face = face.dot(get_rot_y_matrix(math.pi/2))
    face = face.dot(get_shift_matrix(-1, 0, 0))
    polygons.append(face)
    return(polygons)

cpdef list get_cube_polygons():
    # a cube consist of six faces
    # left
    cdef list polygons = []
    rec = Polygon(get_rectangle_points())
    t = get_shift_matrix(-1, 0, 0).dot(get_rot_y_matrix(math.pi/2))
    polygons.append(rec.transform(t))
    # right
    t = get_shift_matrix(1, 0, 0).dot(get_rot_y_matrix(math.pi/2))
    polygons.append(rec.transform(t))
    # bottom
    t = get_shift_matrix(0, -1, 0).dot(get_rot_x_matrix(math.pi/2))
    polygons.append(rec.transform(t))
    # top
    t = get_shift_matrix(0, 1, 0).dot(get_rot_x_matrix(math.pi/2))
    polygons.append(rec.transform(t))
    # front
    t = get_shift_matrix(0, 0, -1)
    polygons.append(rec.transform(t))
    # back
    t = get_shift_matrix(0, 0, 1)
    polygons.append(rec.transform(t))
    return(polygons)

cpdef np.ndarray get_scale_rot_matrix(scale_tuple, aspect_tuple, shift_tuple):
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
    cdef double aspect_ratio = aspect_tuple[0] / aspect_tuple[1]
    cdef np.ndarray scale_matrix = get_scale_matrix(*scale_tuple)
    cdef np.ndarray shift_matrix = get_shift_matrix(*shift_tuple)
    cdef np.ndarray alt_basis = np.array((
        (1, 0, 0, 0),
        (0, aspect_ratio, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1)
        ), dtype=DTYPE)
    cdef np.ndarray alt_basis_inv = np.linalg.inv(alt_basis)
    # combine scale and change of basis to one transformation
    # static matrix
    cdef np.ndarray static_transformation = shift_matrix.dot(alt_basis_inv.dot(scale_matrix))
    return(static_transformation)

cpdef list get_rot_matrix(static_transformation, tuple degrees, int steps):
    """
    static_transformation of type Matrix3d, will be applied to every step
    degrees of type tuple, for every axis one entry in degrees
    steps of type int, how many steps to precalculate
    """
    cdef double angle_x
    cdef double angle_y
    cdef double angle_z
    cdef int step
    cdef double deg2rad = math.pi / 180
    cdef double factor
    cdef np.ndarray transformation
    cdef list transformations
    transformations = []
    for step in range(steps):
        factor = step * deg2rad
        angle_x = degrees[0] * factor
        angle_y = degrees[1] * factor
        angle_z = degrees[2] * factor
        # this part of tranformation is calculate for every step
        transformation = get_rot_z_matrix(angle_z).dot(
                get_rot_x_matrix(angle_x).dot(
                    get_rot_y_matrix(angle_y)))
        # combine with static part of transformation,
        # which does scaling, shifting and aspect ration correction
        # to get affine transformation matrix
        transformation = static_transformation.dot(transformation)
        transformations.append(transformation)
    return(transformations)

cpdef np.ndarray normalized(np.ndarray vector):
    """
    return self with length=1, unit vector
    """
    return(vector / np.linalg.norm(vector))
unit = normalized

cpdef tuple project2d(np.ndarray vector, tuple shift_vec):
    """
    project self to 2d
    simply divide x and y with z value
    """
    shifted = vector / vector.data[2]
    return((shifted[0] + shift_vec[0], shifted[1] + shift_vec[1]))

cpdef double angle_to(vector, other):
    """
    angle between self and other Vector object
    to calculate this, the dot product of self and other is used
    """
    cdef np.ndarray v1
    cdef np.ndarray v2
    v1 = vector / np.linalg.norm(vector)
    v2 = other / np.linalg.norm(other)
    # print "%s dot %s" % (v1, v2)
    cdef double dotproduct = v1.dot(v2)
    return(math.acos(dotproduct))

cpdef double angle_to_unit(vector, other):
    """this version assumes that these two vectors are unit vectors"""
    return(math.acos(vector.dot(other)))

cpdef double length(vector):
    """length"""
    return(np.linalg.norm(vector))

cpdef double length_sqrd(vector):
    """length squared"""
    return(vector.dot(vector))


