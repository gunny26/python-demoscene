#!/usr/bin/python

# import the relevant libraries
import sys
import time
import pygame
import random
import string
import os
# from pygame.locals import *

CHARACTERS = list(string.letters)
# define screen size
SCREEN = (640, 480)
# control Frame Rate
CLOCK = pygame.time.Clock()
FPS = 25
# define background musicfile
BACKGROUND_MUSIC = "monkey_island_theme.mp3"
# define some fonts
pygame.font.init()
TITLE_FONT = pygame.font.Font("atari full.ttf", 32) # title
CHARACTER_FONT = pygame.font.Font(None, 48) # the falling characters
SCORE_FONT = pygame.font.Font("atari full.ttf", 24) # score
INFO_FONT = pygame.font.Font("atari full.ttf", 12) # other messages


class GameStat:
    """Holds game statistics"""

    def __init__(self):
        """ just __init__ """
        self.score = 0
        self.lifes = 50
        self.level = 1
        self.interval = 5
        self.maxtime = 50
        self.minchars = 3


class Character:
    """Controls Life of one Character"""

    def __init__(self, surface, character, character_engine):
        """just __init__"""
        self.surface = surface
        self.character = character
        self.text = CHARACTER_FONT.render(character, 1, (10, 10, 10))
        self.posx = random.random() * surface.get_width()
        self.posy = 0
        self.speed = random.random()
        # indicator if character on bottom
        self.finished = False
        # reference to parent where i life
        # if i am finished, i call delete to delete myself
        self.character_engine = character_engine

    def update(self, clickpos):
        """
        move character in y-direction by 1
        clickpos if not None is position where mouse was clicked
        check if i am clicked
        """
        if clickpos is not None:
            self.check_click(clickpos)
        self.move()

    def move(self):
        """move charactrer on screen"""
        if self.posy < self.surface.get_height():
            self.posy += self.speed
        else:
            self.finished = True
            self.character_engine.delete(self, clicked=False)
        # for debug only, draw red rectangle around charcter to show hitting area
        pygame.draw.rect(self.surface, (255, 0, 0), self.get_myrect(), 1)
        self.surface.blit(self.text, (round(self.posx), round(self.posy)))

    def get_myrect(self):
        """return rect around itself"""
        myrect = self.text.get_rect(center=(
               round(self.posx) + \
               self.text.get_width() / 2, \
               round(self.posy) + \
               self.text.get_height() / 2)
               )
        return(myrect)

    def check_click(self, clickpos):
        """checks if this character was clicked, and takes actions"""
        myrect = self.get_myrect()
        # have to sub offset of subsurface, if any to get real coordinates in top level window
        # to check real click position
        off_x, off_y = self.surface.get_abs_offset()
        if myrect.collidepoint(clickpos[0] - off_x, clickpos[1] - off_y):
            # print "i was clicked"
            self.character_engine.delete(self, clicked=True)


class CharEngine:
    """Controls Life of many characters"""

    def __init__(self, surface, gamestat):
        """just __init__"""
        self.surface = surface
        self.gamestat = gamestat
        # three sub surfaces
        self.head_surface = surface.subsurface((0, 0, self.surface.get_width(), 50))
        self.main_surface = surface.subsurface((0, 50, self.surface.get_width(), self.surface.get_height()-100))
        self.foot_surface = surface.subsurface((0, self.surface.get_height()-50, self.surface.get_width(), 50))
        # create every interval second a new character
        self.interval = self.gamestat.interval / self.gamestat.level
        # maimum time of game in seconds, after time - game over
        self.maxtime = self.gamestat.maxtime
        # minimum number of character on screen
        self.minchars = self.gamestat.minchars * self.gamestat.level
        # list to hold all character objects
        self.characters = []
        # create initial set of characters
        for i in range(5):
            self.generate()
        self.start_timestamp = time.time()
        self.last_timestamp = time.time()

    def update(self, clickpos):
        """ handle all characters an generate more if to less on screen"""
        # print time.time() - self.last_timestamp
        self.remaining_time = self.maxtime - int(time.time() - self.start_timestamp)
        # time to generate new characters ?
        if (time.time() - self.last_timestamp) > self.interval:
            self.generate()
            self.last_timestamp = time.time()
        # or too few characters on screen ?
        if len(self.characters) < self.minchars:
            self.generate()
        # update characters
        for character in self.characters:
            character.update(clickpos)
        # update messages
        self.update_header()
        self.update_footer()
        # finished ?
        if self.remaining_time <= 1:
            return("finished")
        # no more lifes left ?
        elif self.gamestat.lifes == 0 :
            return("lost")
        return("running")
        
    def update_header(self):
        """updates messages on top of screen""" 
        # top surface
        # blit score in left upper corner
        scorestring = "Score : %s" % self.gamestat.score
        scorefont = SCORE_FONT.render(scorestring, 1, (255, 255, 255))
        self.head_surface.blit(scorefont, (0, 0))
        # blit lifes right
        lifestring = "Lifes: %s" % self.gamestat.lifes
        lifefont = SCORE_FONT.render(lifestring, 1, (255, 255, 255))
        self.head_surface.blit(lifefont, (self.surface.get_width() - lifefont.get_width(), 0))

    def update_footer(self):
        """updates messages in bottom of screen"""
        # information in footer
        # blit info txt in footer
        # Level
        levelstring = "Level: %s" % self.gamestat.level
        levelfont = INFO_FONT.render(levelstring, 1, (255, 255, 255))
        self.foot_surface.blit(levelfont, (0, 0))
        # Remaining Time
        timestring = "Time remaining: %s" % self.remaining_time
        timefont = INFO_FONT.render(timestring, 1, (255, 255, 255))
        self.foot_surface.blit(timefont, (self.surface.get_width() - timefont.get_width(), 0))
        # Info Text - center - second line
        infostring = "Press ESC to quit, click all Characters to win"
        infofont = INFO_FONT.render(infostring, 1, (255, 255, 255))
        self.foot_surface.blit(infofont, (self.foot_surface.get_width() / 2 - infofont.get_width() / 2, 25))
       
    def generate(self):
        """ generates a new character and put it on the list """
        index = int(random.random() * len(CHARACTERS))
        self.characters.append(Character(self.main_surface, CHARACTERS[index], self))

    def delete(self, child, clicked):
        """deletes child from list
        if clicked is True scrore increases"""
        if clicked is True:
            self.gamestat.score += CHARACTERS.index(child.character) + 1
        else:
            # character has reached bottom
            self.gamestat.lifes -= 1
        for item in self.characters:
            if item == child:
                self.characters.remove(item)


def grayscale_image(surface):
    darker = 0.5
    width, height = surface.get_size()
    for x in range(width):
        for y in range(height):
            red, green, blue, alpha = surface.get_at((x, y))
            L = (0.3 * red + 0.59 * green + 0.11 * blue) * darker
            gs_color = (L, L, L, alpha)
            surface.set_at((x, y), gs_color)
    return surface

def ingame_loop(surface, char_engine):
    """ main ingame loop """
    clickpos = None
    while True:
        events = pygame.event.get()  
        for event in events:  
            if event.type == pygame.QUIT:  
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print "mouse clicked at (%d, %d)" % event.pos
                clickpos = event.pos
            else:
                clickpos = None
        keyinput = pygame.key.get_pressed()
        if keyinput is not None:
            # print keyinput
            if keyinput[pygame.K_ESCAPE]:
                return("lost")
        # sleep between every frame
        CLOCK.tick(FPS)
        # time.sleep( sleeptime__in_seconds )
        # blank screen
        surface.fill([100, 100, 100])
        # update everything
        state = char_engine.update(clickpos)
        # state of engine could be
        # running
        # finished - player reached end of game
        # lost - player lost game
        if state != "running" :
            return(state)
        # update the screen to show the latest screen image
        pygame.display.update()

def finished_loop(surface, gamestat, msg):
    """ shows finished screen """
    grayscale_image(surface)
    pygame.display.update()
    finished = TITLE_FONT.render(msg, 1, (255, 0, 0))
    surface.blit(finished, \
        (surface.get_width() / 2 - finished.get_width() / 2, \
        surface.get_height() / 2 + finished.get_height() / 2) \
    )
    helpmsg = INFO_FONT.render("click to play", 1, (255, 0, 0))
    # center bottom
    surface.blit(helpmsg, \
        (surface.get_width() / 2- helpmsg.get_width() /2, \
        surface.get_height() - helpmsg.get_height()) \
    )
    pygame.display.update()
    time.sleep(5)
    while True:
        events = pygame.event.get()  
        for event in events:  
            if event.type == pygame.QUIT:  
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print "mouse clicked, restarting"
                return(True)
        keyinput = pygame.key.get_pressed()
        if keyinput is not None:
            # print keyinput
            if keyinput[pygame.K_ESCAPE]:
                sys.exit(0)
        # time.sleep( sleeptime__in_seconds )

def welcome_loop(surface, gamestat):
    """ shows welcome screen """
    title = TITLE_FONT.render("Character Smasher", 1, (255, 0, 0))
    author = INFO_FONT.render("(c) gunny26", 1, (255, 0, 0))
    helpmsg = INFO_FONT.render("click to play", 1, (255, 0, 0))
    # blank screen
    surface.fill((0, 0, 0))
    # in center of screen Title
    surface.blit(title, \
        (surface.get_width() / 2 - title.get_width() / 2, \
        surface.get_height() / 2 - title.get_height()) \
    )
    surface.blit(author, \
        (surface.get_width() / 2 - author.get_width() / 2, \
        surface.get_height() / 2 + author.get_height()) \
    )
    # center bottom
    surface.blit(helpmsg, \
        (surface.get_width() / 2- helpmsg.get_width() /2, \
        surface.get_height() - helpmsg.get_height()) \
    )
    pygame.display.update()
    while True:
        events = pygame.event.get()  
        for event in events:  
            if event.type == pygame.QUIT:  
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print "mouse clicked, restarting"
                return(True)
        keyinput = pygame.key.get_pressed()
        if keyinput is not None:
            # print keyinput
            if keyinput[pygame.K_ESCAPE]:
                sys.exit(0)
        # time.sleep( sleeptime__in_seconds )

def next_level_loop(surface, gamestat):
    """ shows next level splash screen """
    nextlevel = TITLE_FONT.render("Up to Level %d !" % gamestat.level, 1, (255, 0, 0))
    surface.blit(nextlevel, \
        (surface.get_width() / 2 - nextlevel.get_width() / 2, \
        surface.get_height() / 2 + nextlevel.get_height() / 2) \
    )
    pygame.display.update()
    time.sleep(5)


def main():
    """just __main__"""
    # this is where one sets how long the script
    # sleeps for, between frames.sleeptime__in_seconds = 0.05
    # initialise the display window
    screen = pygame.display.set_mode(SCREEN)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(BACKGROUND_MUSIC)
    pygame.mixer.music.play(-1) # endless background music

    # object to hold game statistics
    gamestat = GameStat()
    # at first display welcome screen
    welcome_loop(screen, gamestat)
    while True:
        # main logic of game
        char_engine = CharEngine(screen, gamestat)
        # start game loop
        state = ingame_loop(screen, char_engine)
        # state could be
        # finished - player finished level
        # lost - player lost
        # if player click, restart will be true
        if state == "lost":
            highscore = 0
            if os.path.isfile("highscore.txt"):
                highscore = int(open("highscore.txt", "r").readline())
            if gamestat.score > highscore:
                open("highscore.txt", "w").write(str(gamestat.score))
                finished_loop(screen, gamestat, "!! New Highscore !!")
            else:
                finished_loop(screen, gamestat, "Game Over")
            # if this line is reached, restart
            gamestat = GameStat()
        elif state == "finished":
            gamestat.level += 1
            next_level_loop(screen, gamestat)

if __name__ == "__main__" :
    main()
