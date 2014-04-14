#!/usr/bin/python
"""Plasma.py -- Korruptor Jan 2001, test code for Seal Basher (v1.0)

This little doobry is based on the fast flame example by Pete Shinners
and is another novel neat hack on the surfarray module. 

The plasma algo itself is pretty simple, just a sum of four cosine values
from a pre-calculated look-up table inserted into a surf buff. It's all 
pretty easy really. The comments explain my thinking... 

This is my first hack, and not really optimised apart from what I've learnt
from Pete's example and whilst lurking on #Pygame. If you've got suggestions
for speed increases let me know..."""

import pygame, pygame.transform
from math import *
from operator import *
from pygame.surfarray import *
from pygame.locals import *
from numpy import *

# ------------------------------------------------------------------------------------
# Glob decs

# Screen resolution...
RES     = array((320,256))

# That all important math thingy...
PI  = 3.14159

# Linear array of cosine values to be indexed and summed, initialised to zero prior to pre-calc...
cos_tab = zeros(256)    

# Array of indexes to be used on our cos_tab. Could be variables I suppose. Just easier to cut_n_paste! ;-)
pnt_tab = array((0,0,0,0))

# ------------------------------------------------------------------------------------
def main():
    "Inisalises display, precalculates the cosine values, and controls the update loop"
    
    # Initialise pygame, and grab an 8bit display.
    pygame.init()
    screen_surface = pygame.display.set_mode(RES, 0, 8)

    # Numeric array (working) for the display. Do all our fun stuff here...
    plasma_buffer  = zeros(RES/8)
    
    # Pygame Surface object which will take the surfarray data and be translated into a screen blit... 
    plasma_surface = pygame.Surface((RES[0]/8, RES[1]/8), 0, 8)

    # setup the screen palette...
    set_palette(screen_surface)
        
    # apply the same palette to plasma_surface
    plasma_surface.set_palette(screen_surface.get_palette())

    # Precalculate the consine waves...
    make_cosine()   

    # Fruity loops...
    while 1:
    
        # Have we received an event to close the window?
        for e in pygame.event.get():
            if e.type in (QUIT,KEYDOWN,MOUSEBUTTONDOWN):
                return
                
        # Nope, lets sum the cosine values and update our plasma_array 
        add_cosine(plasma_buffer)
        # Now, blit the arrary to the surface, scale it...
        blit_scaled_surface(screen_surface, plasma_buffer, plasma_surface)
        # Show the results to our audience...
        pygame.display.flip()

            
# ------------------------------------------------------------------------------------
def add_cosine(plasma_buffer):
    "An Y by X loop of screen co-ords, summing the values of four cosine values to produce a colour value that'll map to the previously set surface palette."
    
    # Use working indices for the cosine table, save the real ones for later...
    t1 = pnt_tab[0]
    t2 = pnt_tab[1]
    # Loop for all Y screen coords...
    for y in range(0,RES[1]/8):

        # Save the horizontal indices for later use...
        t3 = pnt_tab[2]
        t4 = pnt_tab[3]
        # Loop accross the screen...
        for x in range(0,RES[0]/8):
            # Our colour value will equal the sum of four cos_table offsets. 
            # The preset surface palette comes in handy here! We just need to output the value...
            # We mod by 256 to prevent our index going out of range. (C would rely on 8bit byte ints and with no mod?)
            colour = cos_tab[mod(t1,256)] + cos_tab[mod(t2,256)] + cos_tab[mod(t3,256)] + cos_tab[mod(t4,256)]
                    
            # Arbitrary values, changing these will allow for zooming etc...
            t3 += 3
            t4 += 2
                        
            # Insert the calculated colour value into our working surfarray...
            plasma_buffer[x][y] = colour

        # Arbitrary values again...
        t1 += 2
        t2 += 1
        
    # Arbitrary values to move along the cos_tab. Play around for something nice...
    # Don't think I need these boundary checkings, but just in case someone decides to run this code for a couple of weeks non-stop...
    #
    if(pnt_tab[0] < 256): 
        pnt_tab[0] += 1
    else:
        pnt_tab[0] = 1
        
    if(pnt_tab[1] < 256):
        pnt_tab[1] += 2
    else:
        pnt_tab[1] = 2
        
    if(pnt_tab[2] < 256):
        pnt_tab[2] += 3
    else:
        pnt_tab[2] = 3
        
    if(pnt_tab[3] < 256):
        pnt_tab[3] += 4
    else:
        pnt_tab[3] = 4
            
# ------------------------------------------------------------------------------------
def make_cosine():
    "Knock up a little pre-calculated cosine lookup table..."
    i = 0
    for i in range (0,256):
        # Play with the values here for interesting results... I just made them up! :-)
        cos_tab[i]=60*(cos(i*PI/32))


# ------------------------------------------------------------------------------------
def set_palette(screen_surface):
    "Create something trippy... Based on Pete's cmap creator, and without doubt the thing that took the longest... Aaaargh! Decent palettes are hard to find..."
    colour_map = zeros((256, 3))
    
    i=0
    # We're trying to compress as large a range of colours into an 8bit palette as possible...
    # so we go for a typical RGB spread. 
    # A larger 2 x 2 colour range over 128 indices also works well...
    # Have a play and see what you like! :-)
    for i in range(0,64):
        colour_map[i][0] = 255
        colour_map[i][1] = i * 4
        colour_map[i][2] = 255 - (i * 4)
        
        colour_map[i+64][0] = 255 - (i * 4)     
        colour_map[i+64][1] = 255 
        colour_map[i+64][2] = (i * 4)
            
        colour_map[i+128][0] = 0     
        colour_map[i+128][1] = 255 - (i * 4)
        colour_map[i+128][2] = 255
     
        colour_map[i+192][0] = i * 4        
        colour_map[i+192][1] = 0  
        colour_map[i+192][2] = 255    
        
            
    # Apply our palette to the screen's surface...
    screen_surface.set_palette(colour_map)
    print colour_map
    
    
    
    
# ------------------------------------------------------------------------------------
def blit_scaled_surface(screen, flame, miniflame):
    "double the size of the data, and blit to screen -- Nicked from Shread's Fast Flame"
    blit_array(miniflame, flame)
    s2 = pygame.transform.scale(miniflame, screen.get_size())
    screen.blit(s2, (0,0))

# Shit captain! In the void of space we're all alone...
# Don't worry ensign. I have a plan: Fire our trippy laser!
if __name__ == '__main__': main()

# End of sauce. Pass the chips...
