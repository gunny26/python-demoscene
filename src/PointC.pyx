#!/usr/bin/python

cdef class PointC(object):

    cdef public float x
    cdef public float y

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return(PointC(self.x + other.x, self.y + other.y))

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return()
