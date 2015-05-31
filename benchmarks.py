#!/usr/bin/python
import random
import array
import sys
import time
from PointC import PointC as PointC

class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return(Point(self.x + other.x, self.y + other.y))

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return()


class Point2(object):

    __slots__ = ["x", "y"]

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return(Point2(self.x + other.x, self.y + other.y))

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return()


def generate():
    amount = 2000000
    starttime = time.time()
    global point1
    point1 = list((Point(random.random() * 800, random.random() * 600) for _ in xrange(amount)))
    print "creating point1 in %f s" % (time.time()-starttime)
    starttime = time.time()
    global point2
    point2 = list(((random.random() * 800, random.random() * 600) for _ in xrange(amount)))
    print "creating point2 in %f s" % (time.time()-starttime)
    starttime = time.time()
    global point3
    point3 = list((array.array("f", (random.random() * 800, random.random() * 600)) for _ in xrange(amount)))
    print "creating point3 in %f s" % (time.time()-starttime)
    starttime = time.time()
    global point4
    point4 = list((Point2(random.random() * 800, random.random() * 600) for _ in xrange(amount)))
    print "creating point4 in %f s" % (time.time()-starttime)
    starttime = time.time()
    global point5
    point5 = list(([random.random() * 800, random.random() * 600] for _ in xrange(amount)))
    print "creating point5 in %f s" % (time.time()-starttime)
    starttime = time.time()
    global point6
    point6 = list(({"x" : random.random() * 800, "y" : random.random() * 600} for _ in xrange(amount)))
    print "creating point6 in %f s" % (time.time()-starttime)
    starttime = time.time()
    global point7
    point7 = list((Point2(random.random() * 800, random.random() * 600) for _ in xrange(amount)))
    print "creating point7 in %f s" % (time.time()-starttime)
    global point8
    point8 = list((PointC(random.random() * 800, random.random() * 600) for _ in xrange(amount)))
    print "creating point8 in %f s" % (time.time()-starttime)


def calculate1(*args, **kwds):
    for point in point1:
        point += Point(1.0, 1.0)

def calculate1a(*args, **kwds):
    for point in point1:
        point = point + Point(1.0, 1.0)

def calculate2(*args, **kwds):
    for point in point2:
        point = (point[0] + 1.0, point[1] + 1.0)

def calculate2a(*args, **kwds):
    map(lambda a: (a[0] + 1.0, a[1] + 1.0), point2)

def calculate3(*args, **kwds):
    for point in point3:
        point = array.array("f", (point[0] + 1.0, point[1] + 1.0))

def calculate4(*args, **kwds):
    for point in point4:
        point += Point(1.0, 1.0)

def calculate5(*args, **kwds):
    for point in point5:
        point[0] += 1.0
        point[1] += 1.0

def calculate5a(*args, **kwds):
    for point in point5:
        point = [point[0] + 1.0, point[1] + 1.0]

def calculate6(*args, **kwds):
    for point in point6:
        point["x"] += 1.0
        point["y"] += 1.0

def calculate6a(*args, **kwds):
    for point in point6:
        point = {"x" : point["x"] + 1.0, "y" : point["y"] + 1.0}

def calculate7(*args, **kwds):
    for point in point7:
        point += Point2(1.0, 1.0)

def calculate7a(*args, **kwds):
    for point in point7:
        point = point + Point2(1.0, 1.0)

def calculate8(*args, **kwds):
    for point in point8:
        point += PointC(1.0, 1.0)

def calculate8a(*args, **kwds):
    for point in point8:
        point = point + PointC(1.0, 1.0)

def run_and_stop(name, func, args=None, kwds=None):
    starttime = time.time()
    func(args, kwds)
    print "%s Duration %f s" % (name, time.time() - starttime)

if __name__ == "__main__":
    point1 = None
    point2 = None
    point3 = None
    point4 = None
    point5 = None
    point6 = None
    point7 = None
    point8 = None
    print "generating"
    generate()
    print "calculating"
    run_and_stop("Point Class List, __iadd__", calculate1)
    run_and_stop("Point Class List, __add__", calculate1a)
    run_and_stop("Tuple List", calculate2)
    run_and_stop("Tuple List, map function", calculate2a)
    run_and_stop("Array List", calculate3)
    run_and_stop("Point class with slots", calculate4)
    run_and_stop("List of lists", calculate5)
    run_and_stop("List of lists, inplace", calculate5a)
    run_and_stop("List of dicts, inplace", calculate6)
    run_and_stop("List of dicts, new dicts", calculate6a)
    run_and_stop("Point Class List with __slots__, __iadd__", calculate7)
    run_and_stop("Point Class List with __slots__, __add__", calculate7a)
    run_and_stop("Cython Point Class List, __iadd__", calculate8)
    run_and_stop("Cython Point Class List, __add__", calculate8a)
