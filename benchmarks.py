#!/usr/bin/python
import random
import array
import sys
import time

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
    global point1
    point1 = list((Point(random.random() * 800, random.random() * 600) for _ in xrange(amount)))
    global point2
    point2 = list(((random.random() * 800, random.random() * 600) for _ in xrange(amount)))
    global point3
    point3 = list((array.array("f", (random.random() * 800, random.random() * 600)) for _ in xrange(amount)))
    global point4
    point4 = list((Point2(random.random() * 800, random.random() * 600) for _ in xrange(amount)))
    global point5
    point5 = list(([random.random() * 800, random.random() * 600] for _ in xrange(amount)))
    global point6
    point6 = list(({"x" : random.random() * 800, "y" : random.random() * 600} for _ in xrange(amount)))

def calculate1(*args, **kwds):
    for point in point1:
        point += Point(1.0, 1.0)

def calculate2(*args, **kwds):
    for point in point2:
        point = (point[0] + 1.0, point[1] + 1.0)

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

def calculate6(*args, **kwds):
    for point in point6:
        point["x"] += 1
        point["y"] += 1

def calculate6a(*args, **kwds):
    for point in point6:
        point = {"x" : point["x"] + 1, "y" : point["y"] + 1}


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
    print "generating"
    generate()
    print "Point Class List, size %s" % sys.getsizeof(point1)
    print "Tuple List, size %s" % sys.getsizeof(point2)
    print "Array List, size %s" % sys.getsizeof(point3)
    print "Point Class with slots List, size %s" % sys.getsizeof(point4)
    print "List of Lists, size %s" % sys.getsizeof(point5)
    print "calculating"
    run_and_stop("Point Class List", calculate1)
    run_and_stop("Tuple List", calculate2)
    run_and_stop("Array List", calculate3)
    run_and_stop("Point class with slots", calculate4)
    run_and_stop("List of lists", calculate5)
    run_and_stop("List of dicts, inplace", calculate6)
    run_and_stop("List of dicts, new dicts", calculate6a)
