#imports
import pygame as pg
import multiprocessing as mp
import time
import numpy as np
import threading
from myDictionary import myDictionary
import random
#importing custom made classes
from userData import User



class Rectangle:
    def __init__(self,x,y,width,height,window)-> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = pg.Color(255,255,255)
        self.__rect = pg.Rect(x,y,width,height)
        self.window = window
    
    def set_color(self,R,G,B)-> None:
        self.color = pg.Color(R,G,B)

    def set_color(self,color: str)-> None:
        self.color = pg.Color(str(color))

    def draw(self)-> None:
        pg.draw.rect(self.window,self.color,(self.x,self.y,self.width,self.height))
    
    def draw_box(self)-> None:
        pg.draw.rect(self.window,self.color,(self.x,self.y,self.width,self.height),2)

    def collidepoint(self,locations) -> bool:
        self.__rect = pg.Rect(self.x,self.y,self.width,self.height)
        if(self.__rect.collidepoint(locations)):
            return True
        else:
            return False

class ProgressBar:
    def __init__(self,x,y,width,height,backgroundColor,fillColor,window)-> None:
        
        #rectangles
        self.backgroundRectangle = Rectangle(x,y,width,height,window)
        self.fillRectangle = Rectangle(x,y,0,height,window)

        #colors
        self.backgroundColor = backgroundColor
        self.fillColor = fillColor

        #setting rectangle colors
        self.backgroundRectangle.set_color(backgroundColor)
        self.fillRectangle.set_color(fillColor)

        #progress variables
        self.totalProgress = 100.0 
        self.progress = 0.0

    def update_progress(self,progress: float, totalProgress: float)-> None:
        try:
            self.fillRectangle.width = int((progress / totalProgress)*self.backgroundRectangle.width)
        except ZeroDivisionError:
            print("ZeroDivisionError")
        print(self.progress)


    def draw(self)-> None:
        self.backgroundRectangle.draw()
        self.fillRectangle.draw()

class textBox:
    def __init__(self,x,y,width,height,window)-> None:

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.window = window
        self.color = pg.Color(255,255,255)
        self.isActive = False
        self.text = ""
        self.font = pg.font.Font(None,32)
        self.textColor = pg.Color('lightskyblue3')
        self.__rectangle = Rectangle(self.x,self.y,self.width,self.height,window)
        self.__rectangle.set_color('lightskyblue3')
        self.holdingCtrl = False
        self.focused = False

    def set_active(self)-> None:
        self.color = pg.Color('dodgerblue2')
        self.textColor = pg.Color('dodgerblue2')
        self.__rectangle.set_color('dodgerblue2')
        self.isActive = True
        self.focused = True

    def set_deactive(self)-> None:
        self.color = pg.Color('lightskyblue3')
        self.textColor = pg.Color('lightskyblue3')
        self.__rectangle.set_color('lightskyblue3')
        self.isActive = False
        self.focused = False
    
    def set_color(self,R,G,B)-> None:
        self.color = pg.Color(R,G,B)
        self.textColor = pg.Color(R,G,B)

    def set_color(self,color)-> None:
        self.color = pg.Color(color)
        self.textColor = pg.Color(color)
    
    def append_text(self,text)-> None:
        self.text += text

    def backspace(self)-> None:
        if(len(self.text) != 0):
            self.text = self.text[:-1]

    def cntrl_backspace(self)-> None:
        self.text = ""

    def __update_width(self)-> None:
        #check if the width of the box is smaller than the width of the text
        if(self.__rectangle.width < self.textRender.get_width()):
            self.__rectangle.width = self.textRender.get_width() + 10
        elif (self.__rectangle.width > self.width):
            self.__rectangle.width = self.textRender.get_width() + 10

    def draw(self)-> None:
        #render the text
        self.textRender = self.font.render(self.text,True,self.textColor)

        #draw text
        self.window.blit(self.textRender,(self.x+5,self.y+5)) 

        self.__update_width()
        #draw rectangle
        self.__rectangle.draw_box()

        self.check_click()
    

    def check_click(self)-> None:
        #gets mouse position, and checks if textbox was clicked
        mouse_pos = pg.mouse.get_pos()
        if(pg.mouse.get_pressed()[0]):
            if(self.__rectangle.collidepoint(mouse_pos)):
                self.focused = True
                self.set_active()
            else:
                self.focused = False
                self.set_deactive()

class Button:
    def __init__(self,x,y,width,height,text,window)-> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = pg.Color('lightskyblue3')
        self.textColor = pg.Color('lightskyblue3')
        self.hoverColor = pg.Color('deepskyblue1')
        self.font = pg.font.Font(None,32)
        self.__rectangle = Rectangle(self.x,self.y,self.width,self.height,window)
        self.__rectangle.set_color('lightskyblue3')
        self.window = window

        #mouse events
        self.pressed = False
        self.confirmed = False


    #checks if the button was pressed, sets the value to false to prevent the button from staying pressed
    def get_pressed(self)-> None:
        temp = self.pressed
        self.pressed = False
        return temp
        

    def set_active(self)-> None:
        self.color = pg.Color('dodgerblue2')
        self.textColor = pg.Color('dodgerblue2')
        self.__rectangle.set_color('dodgerblue2')

    def set_deactive(self)-> None:
        self.color = pg.Color('lightskyblue3')
        self.textColor = pg.Color('lightskyblue3')
        self.__rectangle.set_color('lightskyblue3')
    
    def set_hover(self)-> None:
        self.color = self.hoverColor
        self.textColor = self.hoverColor
        self.__rectangle.set_color('deepskyblue1')

    def set_color(self,color)-> None:
        self.color = pg.Color(color)
        self.textColor = pg.Color(color)


    def collidepoint(self,locations) -> bool:
        if(self.__rectangle.collidepoint(locations)):
            return True
        else:
            return False

    


    def draw(self)-> None:

        #render the current font
        self.textRender = self.font.render(self.text,True,self.textColor)

        #draw the outline
        self.__rectangle.draw_box()

        #draw the text
        self.window.blit(self.textRender,(self.x+5,self.y+5))

        self.check_click()
    
    def check_click(self)-> None:
        mouse_pos = pg.mouse.get_pos()
        if self.__rectangle.collidepoint(mouse_pos):
            if(pg.mouse.get_pressed()[0]):
                self.set_active()
                self.pressed = True
            else:
                self.pressed = False
                self.set_deactive()
        
        else:
            if(pg.mouse.get_pressed()[0] != True):
                self.set_deactive()
                self.pressed = False



class playerInfoBox:
    def __init__(self, user: User,window)-> None:
        self.user = user
        self.window = window
        self.area = window.get_rect()
        self.color_active = 'dodgerblue2'
        self.color_inactive = 'lightskyblue3'
        self.color_UncommonScore = 'LIMEGREEN'
        self.color_CommonScore = 'DARKGRAY'
        self.color_RareScore = 'ROYALBLUE'
        self.font = pg.font.Font(None,32)

        #user info
        self.userbox_performance = str(self.user.Performance)+ "pp"
        self.userbox_performance_color = self.color_UncommonScore
        self.userbox_name = self.user.username
        self.userbox_level = ("Lvl: "+ str(self.user.Level))
        self.userbox_accuracy = str(self.user.get_acc()) + "%"
        self.userbox_playerWPM = str(self.user.TopTenWPM) + "WPM"

        self.add_objects()

        #level bar
        self.level_bar = ProgressBar(self.userbox.x + self.userbox.width - 100,(self.userbox.y+self.userbox.height-11),100,10,'DARKGRAY','LIMEGREEN',self.window)
        self.level_bar.update_progress(15.0,100.0)


    def add_objects(self)-> None:
        #box for the user info
        self.userbox = Rectangle((int(self.area.width /2) -150),0,300,70,self.window)
        self.userbox.set_color(self.color_active) #set color

    


    def draw(self)-> None:
        #render
        userbox_level_surface = self.font.render(self.userbox_level,True,pg.Color(self.color_active))
        userbox_name_surface = self.font.render(self.userbox_name,True,pg.Color(self.color_active))
        userbox_accuracy_surface = self.font.render(self.userbox_accuracy,True,pg.Color(self.color_active))
        userbox_playerWPM_surface = self.font.render(self.userbox_playerWPM,True,pg.Color(self.color_active))

        #draw
        self.level_bar.draw()
        self.userbox.draw_box()

        #drawing all the user specific things
        self.window.blit(userbox_level_surface,(self.userbox.x+self.userbox.width-int(userbox_level_surface.get_width())-2,self.userbox.y+self.userbox.height-35))

        self.window.blit(userbox_name_surface,(self.userbox.x+2,self.userbox.y+self.userbox.height-25))

        self.window.blit(userbox_accuracy_surface,(self.userbox.x+self.userbox.width-int(userbox_accuracy_surface.get_width())-2,self.userbox.y+2))

class Word():
    def __init__(self,dictionary: myDictionary,window, y : int)-> None:
        self.word = ""
        self.font = pg.font.Font(None,32)
        self.color_active = 'dodgerblue2'
        self.word = dictionary.get_words().lower()
        self.window = window
        self.y = y
        self.word_surface = self.font.render(self.word,True,pg.Color(self.color_active))
        self.x = random.randint(0,self.window.get_width()-self.word_surface.get_width() - 5)

    def move(self,moveSpeed: int)-> None:
        self.y += moveSpeed
    
    def draw(self)-> None:

        #draw the word
        self.window.blit(self.word_surface,(self.x,self.y))