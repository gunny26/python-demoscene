#!/usr/bin/python

from libc.stdlib cimport malloc, free

class Vector(object):

    def __init__(self, *args):
        cdef double *my_array = <double *>malloc(4 * sizeof(double))

    def __str__(self):
        sb = ",".join(self.my_array)
        return(sb)

    def __del__(self):
        free(my_array)
