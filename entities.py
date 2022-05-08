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

    def moveLeft(self,x):
        self.x -= x

    def moveRight(self,x):
        self.x += x

    def moveUp(self,y):
        self.y -= y

    def moveDown(self,y):
        self.y += y