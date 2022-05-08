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
    def __init__(self,x,y,width,height,window):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = pg.Color(255,255,255)
        self.__rect = pg.Rect(x,y,width,height)
        self.window = window
    
    def setColor(self,R,G,B):
        self.color = pg.Color(R,G,B)

    def setColor(self,color: str):
        self.color = pg.Color(str(color))

    def draw(self):
        pg.draw.rect(self.window,self.color,(self.x,self.y,self.width,self.height))
    
    def drawBox(self):
        pg.draw.rect(self.window,self.color,(self.x,self.y,self.width,self.height),2)

    def collidepoint(self,locations):
        self.__rect = pg.Rect(self.x,self.y,self.width,self.height)
        if(self.__rect.collidepoint(locations)):
            return True
        else:
            return False

class ProgressBar:
    def __init__(self,x,y,width,height,backgroundColor,fillColor,window):
        
        #rectangles
        self.backgroundRectangle = Rectangle(x,y,width,height,window)
        self.fillRectangle = Rectangle(x,y,0,height,window)

        #colors
        self.backgroundColor = backgroundColor
        self.fillColor = fillColor

        #setting rectangle colors
        self.backgroundRectangle.setColor(backgroundColor)
        self.fillRectangle.setColor(fillColor)

        #progress variables
        self.totalProgress = 100.0 
        self.progress = 0.0

    def updateProgress(self,progress: float, totalProgress: float):
        try:
            self.fillRectangle.width = int((progress / totalProgress)*self.backgroundRectangle.width)
        except ZeroDivisionError:
            print("ZeroDivisionError")
        print(self.progress)


    def draw(self):
        self.backgroundRectangle.draw()
        self.fillRectangle.draw()

class textBox:
    def __init__(self,x,y,width,height,window):

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
        self.__rectangle.setColor('lightskyblue3')
        self.holdingCtrl = False
        self.focused = False

    def setActive(self):
        self.color = pg.Color('dodgerblue2')
        self.textColor = pg.Color('dodgerblue2')
        self.__rectangle.setColor('dodgerblue2')
        self.isActive = True
        self.focused = True

    def setDeactive(self):
        self.color = pg.Color('lightskyblue3')
        self.textColor = pg.Color('lightskyblue3')
        self.__rectangle.setColor('lightskyblue3')
        self.isActive = False
        self.focused = False
    
    def setColor(self,R,G,B):
        self.color = pg.Color(R,G,B)
        self.textColor = pg.Color(R,G,B)

    def setColor(self,color):
        self.color = pg.Color(color)
        self.textColor = pg.Color(color)
    
    def appendText(self,text):
        self.text += text

    def backspace(self):
        if(len(self.text) != 0):
            self.text = self.text[:-1]

    def cntrlBackspace(self):
        self.text = ""

    def __updateWidth(self):
        #check if the width of the box is smaller than the width of the text
        if(self.__rectangle.width < self.textRender.get_width()):
            self.__rectangle.width = self.textRender.get_width() + 10
        elif (self.__rectangle.width > self.width):
            self.__rectangle.width = self.textRender.get_width() + 10

    def draw(self):
        #render the text
        self.textRender = self.font.render(self.text,True,self.textColor)

        #draw text
        self.window.blit(self.textRender,(self.x+5,self.y+5)) 

        self.__updateWidth()
        #draw rectangle
        self.__rectangle.drawBox()

        self.check_click()
    

    def check_click(self):
        #gets mouse position, and checks if textbox was clicked
        mouse_pos = pg.mouse.get_pos()
        if(pg.mouse.get_pressed()[0]):
            if(self.__rectangle.collidepoint(mouse_pos)):
                self.focused = True
                self.setActive()
            else:
                self.focused = False
                self.setDeactive()

class Button:
    def __init__(self,x,y,width,height,text,window):
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
        self.__rectangle.setColor('lightskyblue3')
        self.window = window

        #mouse events
        self.pressed = False
        self.confirmed = False


    #checks if the button was pressed, sets the value to false to prevent the button from staying pressed
    def getPressed(self):
        temp = self.pressed
        self.pressed = False
        return temp
        

    def setActive(self):
        self.color = pg.Color('dodgerblue2')
        self.textColor = pg.Color('dodgerblue2')
        self.__rectangle.setColor('dodgerblue2')

    def setDeactive(self):
        self.color = pg.Color('lightskyblue3')
        self.textColor = pg.Color('lightskyblue3')
        self.__rectangle.setColor('lightskyblue3')
    
    def setHover(self):
        self.color = self.hoverColor
        self.textColor = self.hoverColor
        self.__rectangle.setColor('deepskyblue1')

    def setColor(self,color):
        self.color = pg.Color(color)
        self.textColor = pg.Color(color)


    def collidepoint(self,locations):
        if(self.__rectangle.collidepoint(locations)):
            return True
        else:
            return False

    


    def draw(self):

        #render the current font
        self.textRender = self.font.render(self.text,True,self.textColor)

        #draw the outline
        self.__rectangle.drawBox()

        #draw the text
        self.window.blit(self.textRender,(self.x+5,self.y+5))

        self.check_click()
    
    def check_click(self):
        mouse_pos = pg.mouse.get_pos()
        if self.__rectangle.collidepoint(mouse_pos):
            if(pg.mouse.get_pressed()[0]):
                self.setActive()
                self.pressed = True
            else:
                self.pressed = False
                self.setDeactive()
        
        else:
            if(pg.mouse.get_pressed()[0] != True):
                self.setDeactive()
                self.pressed = False



class playerInfoBox:
    def __init__(self, user: User,window):
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
        self.userbox_accuracy = str(self.user.getAcc()) + "%"
        self.userbox_playerWPM = str(self.user.TopTenWPM) + "WPM"

        self.addObjects()

        #level bar
        self.level_bar = ProgressBar(self.userbox.x + self.userbox.width - 100,(self.userbox.y+self.userbox.height-11),100,10,'DARKGRAY','LIMEGREEN',self.window)
        self.level_bar.updateProgress(15.0,100.0)


    def addObjects(self):
        #box for the user info
        self.userbox = Rectangle((int(self.area.width /2) -150),0,300,70,self.window)
        self.userbox.setColor(self.color_active) #set color

    


    def draw(self):
        #render
        userbox_level_surface = self.font.render(self.userbox_level,True,pg.Color(self.color_active))
        userbox_name_surface = self.font.render(self.userbox_name,True,pg.Color(self.color_active))
        userbox_accuracy_surface = self.font.render(self.userbox_accuracy,True,pg.Color(self.color_active))
        userbox_playerWPM_surface = self.font.render(self.userbox_playerWPM,True,pg.Color(self.color_active))

        #draw
        self.level_bar.draw()
        self.userbox.drawBox()

        #drawing all the user specific things
        self.window.blit(userbox_level_surface,(self.userbox.x+self.userbox.width-int(userbox_level_surface.get_width())-2,self.userbox.y+self.userbox.height-35))

        self.window.blit(userbox_name_surface,(self.userbox.x+2,self.userbox.y+self.userbox.height-25))

        self.window.blit(userbox_accuracy_surface,(self.userbox.x+self.userbox.width-int(userbox_accuracy_surface.get_width())-2,self.userbox.y+2))

class Word():
    def __init__(self,dictionary: myDictionary,window, y : int):
        self.word = ""
        self.font = pg.font.Font(None,32)
        self.color_active = 'dodgerblue2'
        self.word = dictionary.getWords().lower()
        self.window = window
        self.y = y
        self.word_surface = self.font.render(self.word,True,pg.Color(self.color_active))
        self.x = random.randint(0,self.window.get_width()-self.word_surface.get_width() - 5)

    def move(self,moveSpeed: int):
        self.y += moveSpeed
    
    def draw(self):

        #draw the word
        self.window.blit(self.word_surface,(self.x,self.y))