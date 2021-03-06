from cgitb import text
import pygame as pg
import multiprocessing as mp
import time
import numpy as np
import threading

#module import
from entities import *
from myDictionary import myDictionary
from objects import *
from userData import *




class Screen:
    #called by all child classes
    def __init__(self,window):
        #colors
        self.activeColor = 'dodgerblue2'
        self.inactiveColor = 'lightskyblue3'
        #window
        self.window = window


    def draw(self):
        self.window.fill((0,0,0))




class LoginScreen(Screen):
    
    def add_objects(self):

        #text boxes
        self.usernameBox = textBox(100,100,140,32,self.window)
        self.usernameBox.set_color(self.inactiveColor)

        self.passwordBox = textBox(100,164,140,32,self.window)
        self.passwordBox.set_color(self.inactiveColor)

        self.rectangles.append(self.usernameBox)
        self.rectangles.append(self.passwordBox)

        #buttons
        self.loginButton = Button(340,164,90,32,'login',self.window)
        self.signUpButton = Button(340,100,90,32,'signup',self.window)
    
    def __init__(self,window):
        super().__init__(window)
        self.rectangles = []
        self.add_objects() #adds textboxes and buttons
        self.__allUsers = [] #array of users
        self.user = User() #creats a default user
        self.__read_from_file() #loads allUsers


    def set_active(self, target):
        if target == "usernameBox":
            self.usernameBox.set_active()
            self.passwordBox.set_deactive()
        elif target == "passwordBox":
            self.passwordBox.set_active()
            self.usernameBox.set_deactive()
        else:
            self.passwordBox.set_deactive()
            self.usernameBox.set_deactive()

    def __write_to_file(self):
        pickle.dump(self.__allUsers,open("SAVE_DATA/Game_Data/Users.txt","wb"))

    def __read_from_file(self):
        try:
            self.__allUsers = pickle.load(open("SAVE_DATA/Game_Data/Users.txt","rb"))
        except FileNotFoundError:
            self.__write_to_file()
    
    def sign_up(self):
        self.user.Signup(self.usernameBox.text,self.passwordBox.text)
        self.__allUsers.append(self.user)
        return self.user

    def login(self):
        pass

    def login_attempt(self):
        for user in self.__allUsers:
            #print("username: " + user.username)
            #print("password: " + user.password)
            if(user.username == self.usernameBox.text and user.password == self.passwordBox.text):
                self.user = user
                return True
        return False



    
    def draw(self):
        #background
        self.window.fill((30,30,30))

        #fill in boxes
        if(len(self.rectangles) > 0):
            for R in self.rectangles:
                R.draw()
        
        #buttons
        self.loginButton.draw()
        self.signUpButton.draw()
        


class MainMenuScreen(Screen):
    def __init__(self,window):
        super().__init__(window)
        self.area = window.get_rect()
        self.buttons = []
        self.add_buttons()
        self.user = User()
        self.userInfo = playerInfoBox(self.user,self.window)

    def add_buttons(self):
        self.startGameButton = Button(int(self.area.width/2)-75,int(self.area.height/6),150,32,"Start Game",self.window)
        self.settingsButton = Button(int(self.area.width/2)-75,int(self.area.height/6)*2,150,32,"Settings",self.window)
        self.leaderboardButton = Button(int(self.area.width/2)-75,int(self.area.height/6)*3,150,32,"Leaderboard",self.window)
        self.quitButton = Button(int(self.area.width/2)-75,int(self.area.height/6)*5,150,32,"Quit",self.window)
        self.logoutButton = Button(int(self.area.width/2)-75,int(self.area.height/6)*4,150,32,"Logout",self.window)
        self.buttons.append(self.startGameButton)
        self.buttons.append(self.settingsButton)
        self.buttons.append(self.leaderboardButton)
        self.buttons.append(self.quitButton)
        self.buttons.append(self.logoutButton)
    
    def update_user(self,newuser : User):
        self.user = newuser
        self.userInfo = playerInfoBox(self.user,self.window)
    
    def draw(self):

        self.window.fill((30,30,30))

        self.userInfo.draw()
        for button in self.buttons:
            button.draw()


class DifficultySelectScreen(Screen):
    def __init__(self,window):
        super().__init__(window)
        self.area = window.get_rect()
        self.buttons = []
        self.add_buttons() #adds the buttons
        self.add_user_box() #this is what shows the player stats

    def add_buttons(self):
        self.easyButton = Button(self.area.width/2 -150,self.area.height*1/6,150,32,"Easy Mode",self.window)
        self.mediumButton = Button(self.area.width/2 -150,self.area.height*2/6,150,32,"Normal Mode",self.window)
        self.hardButton = Button(self.area.width/2 -150,self.area.height*3/6,150,32,"Hard Mode",self.window)
        self.backButton = Button(self.area.width/2 -150,self.area.height*4/6,150,32,"back",self.window)

        self.buttons.append(self.easyButton)
        self.buttons.append(self.mediumButton)
        self.buttons.append(self.hardButton)
        self.buttons.append(self.backButton)
    
    def add_user_box(self):
        pass

    def draw(self):
        self.window.fill((30,30,30))
        for button in self.buttons:
            button.draw()
        
class GameScreen(Screen):
    
    def __init__(self,window):
        super().__init__(window)
        self.dictionary = myDictionary()
        self.words = []
        self.moveSpeed = 1
        self.window = window
        self.area = self.window.get_rect()
        self.failed = False
        self.typeBox = textBox(int(self.area.width/2-100),int(self.area.height-50),80,30,self.window)

        self.accuracy = [0,0,0] #hit #miss #total
        self.score = 0
        self.pp = 0
        self.highScore = 0

    def update_userstate(self, user: User):
        self.highScore = user.Highscore


    def check_word(self):
        for word in self.words:
            if(self.typeBox.text == word.word):
                #remove word
                self.words.remove(word)
                self.typeBox.text = ""
        
        self.typeBox.text = ""
    

    
    def draw(self):
        if(len(self.words) < 4):
            self.words.append(Word(self.dictionary,self.window,0 - len(self.words)*25))
        
        
        self.window.fill((30,30,30))
        for word in self.words:
            word.draw()
            word.move(self.moveSpeed)
            #if word below screen 
            
        for word in self.words:
            if(word.y >= self.area.height):
                self.failed = True
        self.typeBox.draw()


