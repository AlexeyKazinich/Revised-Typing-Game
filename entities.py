import pygame as pg
import multiprocessing as mp
import time
import numpy as np
import threading




class Player:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = pg.Color(0,0,0)
    
    def draw(self,window):
        pg.draw.rect(window,self.color,(self.x,self.y,self.width,self.height))

    def move_left(self,x):
        self.x -= x

    def move_right(self,x):
        self.x += x

    def move_up(self,y):
        self.y -= y

    def move_down(self,y):
        self.y += y