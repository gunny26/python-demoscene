#!/usr/bin/python3

import sys
import pygame
import math
import time

class PrimeSpiral(object):

    def __init__(self, surface):
        self.surface = surface
        self.pixelarray = pygame.PixelArray(surface)
        self.initialize()

    def initialize(self):
     width = min(self.surface.get_width(), self.surface.get_height())
     max_counter = (width - 1) ** 2
     for counter, pos in enumerate(self.spiral_walk(width)):
        if counter == max_counter:
            break
        #print counter, self.is_prime(counter), pos
        if self.is_prime(counter):
            try:
                self.pixelarray[pos[0], pos[1]] = 0x00FF00
            except IndexError:
                print counter, self.is_prime(counter), pos

    @staticmethod
    def is_prime(number):
        startprimes = {
            0 : True,
            1 : True,
            2 : False,
            3 : True,
            4 : False,
            5 : True,
            6 : False,
            7 : True,
            8 : False,
        }
        if number < 9 :
            return startprimes[number]
        for i in range(2, int(math.sqrt(number)) + 1):
            #print "testing %s %% %s = %s" % (number, i, number % i)
            if number % i == 0:
                return False
        return True
    
    def spiral_walk(self, width):
        pos = [int(width/2), int(width/2)]
        vecs = [
            (1, 0),
            (0, -1),
            (-1, 0),
            (0, 1)
        ]
        counter = 0
        for length in range(1, width):
            for a in range(2):
                direction = vecs[counter % 4]
                for i in range(length):
                    yield pos
                    pos[0] += direction[0]
                    pos[1] += direction[1]
                counter += 1

    def update(self):
        pass

def main():
    """ test """
    fps = 1
    surface = pygame.display.set_mode((1024, 1024))
    pygame.init()
    clock = pygame.time.Clock()
    starttime = time.time()
    demo = PrimeSpiral(surface)
    print "cacluated prime spiral in %f seconds" % (time.time() - starttime)
    while True:
        clock.tick(fps)
        events = pygame.event.get()  
        for event in events:  
            if event.type == pygame.QUIT:  
                sys.exit(0)
        pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
        demo.update()
        pygame.display.update()

if __name__ == "__main__" :
    main()
