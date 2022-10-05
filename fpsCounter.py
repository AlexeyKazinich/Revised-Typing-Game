import pygame as pg
import multiprocessing as mp
import time
import numpy as np
import threading
import math


class fpsCounter:
    def __init__(self,window)-> None:
        self.cSec = 0
        self.cFrame = 0
        self.FPS= 0
        self.deltatime = 0
        self.font_fps = pg.font.Font(None,12)
        self.color_fps = pg.Color(0,255,0)
        self.area = window.get_rect()
        self.window = window
        self.tickrate = 100
        

    def count_fps(self)-> None:
        if self.cSec == time.strftime("%S"):
            self.cFrame +=1
        else:
            self.FPS = self.cFrame
            self.cFrame = 0
            self.cSec = time.strftime("%S")
            if self.FPS > 0:
                self.deltatime = 1 / self.FPS

    def draw(self)-> None:
        self.FPS_counter_surface = self.font_fps.render(str(math.floor(self.FPS))+"FPS",True,self.color_fps)
        self.window.blit(self.FPS_counter_surface,(self.area.width-self.FPS_counter_surface.get_width(),0))