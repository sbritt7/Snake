"""A script that when run will allow the user to play Snake"""

#imports
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        #need to convert between grid and surface pixels
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis + centre-radius, j*dis + 8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis + 8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        #head is a cube at a given position that we define at beginning
        self.head = cube(pos)
        #we then add the head to the body
        self.body.append(self.head)
        #define initial direction, can only move in one dimension at a time
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            #need to let user quit
            if event.type == pygame.QUIT:
                pygame.quit()
            #bool list of whether key was pressed or not
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    #need to record where the turn happened so that each cube of the snake's body can turn at the right point
                    #create a new key in the turns dictionary which is the position of the head and the value is the direction of the head after the turn
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    #elif so that the user can only click one key at once
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    #[:] makes a copy so that you don't accidentally change the position of the snake when you don't want to
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        
        for i, c in enumerate(self.body):
            #get index, cube for the body list
            p = c.pos[:]
            #if the position of one of the body cubes is in the turns dict then turn
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) -1:
                    #if we are on the last cube, remove the turn otherwise it will always turn when you hit that point on the surface
                    self.turns.pop(p)
            else:
                #need to define what happens when snake isn't turning
                #defining boundaries for snakes movement
                #first condition: if the snake is moving left and the position of the cube is less than or equal to 0 we change the position so that it goes to the right of the screen
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows -1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
                #if not at edge and not at turn needs to carry on moving in the same direction
                else: c.move(c.dirnx, c.dirny)


    def reset(self, pos):
        #delete old snake and create new snake 
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        #need to check which direction the snake is travelling in when it eats the snack so the next cube can be added in the right place
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))
        #need to then give the new cube the same direction as the tail, otherwise it wouldn't move
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                #when we draw first object we want to add eyes, so True is an optional parameter which adds eyes
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawgrid(w, rows, surface):
    sizeBtwn = w // rows
    x=0
    y=0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        #draw two lines every loop of for loop, rgb, start position of line, end position of line
        #need the size between because the draw.line can't handle large integers so need to draw lines sequentially
        pygame.draw.line(surface, (255,255,255), (x,0), (x,w))
        pygame.draw.line(surface, (255,255,255), (0,y), (w,y))

def redrawWindow(surface):
    #updates display
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    pygame.display.update()
    drawgrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, item):
    #item is the snake
    positions = item.body
    while True:
        x = random.randrange(rows)
        y= random.randrange(rows) 
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)
        

def message_box(subject, content):
    root = tk.Tk()
    #make window come up on top
    root.attributes('-topmost', True)
    #make window invisible
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

#main loop
def main():
    global width, rows, s, snack
    width = 500
    height = 500
    rows = 20
    win = pygame.display.set_mode((width, height))
    #color, position for snake
    s = snake((255,0,0), (10,10))
    #generate the first snack
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    flag=True
    #makes sure that game doesn't run at more that 10 frames per second
    clock = pygame.time.Clock()
    while flag:
        #changes speed of snake - depends on speed of machine
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            #if the head of the snake hits the snack a new cube is added to the snake and a new snack is generated
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))
        #need to deal with collisions of the snake with itself
        for x in range(len(s.body)):
            #if the position of any of the cubes is equal to the positions of any of the other cubes then rest snake and display score, then break
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You suck', 'Try again, get gd ygm')
                s.reset((10,10))
                break
        redrawWindow(win)

    pass

main()