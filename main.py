#imports
import pygame as pg
import multiprocessing as mp
import time
import numpy as np
import threading
import math

#custom class imports
from screens import *
from objects import *
from entities import *
from userData import *
from fpsCounter import *

pg.init()


#window definitions
window = pg.display.set_mode((500,500))
pg.display.set_caption('typing game')


#keeps track of current game state
class State:
    def __init__(self):
        self.__state = "LoginScreen"
    
    def change_state(self, state):
        self.__state = state

    def getState(self):
        return self.__state


#Main class
class Game:
    def __init__(self):
        #keeps track of the screen
        self.state = State()
        
        #fps
        self.fpscounter = fpsCounter(window)

        #User info
        self.dataCenter = DataCenter()
        self.user = User()

        #Screens
        self.loginScreen = LoginScreen(window)
        self.gameScreen = GameScreen(window)
        self.mainMenu = MainMenuScreen(window)
        self.difficultySelectScreen = DifficultySelectScreen(window)

        
        
        self.clock = pg.time.Clock()
        self.mouseFocus = pg.mouse.get_focused()

    

    def start(self):
        #starts the main loop
        self.gameLoop()

    #main loop
    def gameLoop(self):
        self.run = True
        while self.run:

            #listen to clicks
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.dataCenter.SaveToFile()
                    self.run = False
                
                #all buttons and other checks with logic for LoginScreen
                if(self.state.getState() == "LoginScreen"):
                    if(self.loginScreen.loginButton.getPressed()):
                        if(self.dataCenter.login(self.loginScreen.usernameBox.text,self.loginScreen.passwordBox.text)):
                                self.user = self.dataCenter.user
                                self.state.change_state("MainMenu")
                        
                    elif(self.loginScreen.signUpButton.getPressed()):
                        if(self.dataCenter.signup(self.loginScreen.usernameBox.text,self.loginScreen.passwordBox.text)):
                            self.user = self.dataCenter.user
                            self.state.change_state("MainMenu")

                    
                
                    if event.type == pg.KEYDOWN:  
                        if(self.loginScreen.usernameBox.focused):
                            #print(self.loginScreen.usernameBox.text)
                            #print(self.loginScreen.usernameBox.holdingCtrl)
                            if event.key == pg.K_BACKSPACE:
                                if(self.loginScreen.usernameBox.holdingCtrl == True):
                                    self.loginScreen.usernameBox.cntrlBackspace()
                                else:
                                    self.loginScreen.usernameBox.backspace()
                            elif event.key == pg.K_LCTRL:
                                self.loginScreen.usernameBox.holdingCtrl = True
                            elif event.key == pg.K_TAB:
                                self.loginScreen.usernameBox.setDeactive()
                                self.loginScreen.passwordBox.setActive()
                            else:
                                self.loginScreen.usernameBox.appendText(event.unicode)
                        
                        elif(self.loginScreen.passwordBox.focused):
                            if event.key == pg.K_BACKSPACE:
                                self.loginScreen.passwordBox.backspace()
                            else:
                                self.loginScreen.passwordBox.appendText(event.unicode)
                    

                    #if a key was released
                    elif event.type == pg.KEYUP:
                        #if current box thats active is usernameBox
                        if(self.loginScreen.usernameBox.isActive):
                            #if the key that was released was left ctrl
                            if event.key == pg.K_LCTRL:
                                self.loginScreen.usernameBox.holdingCtrl = False #set holding control to false
                elif(self.state.getState() == "GameScreen"):
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            self.gameScreen.typeBox.backspace()
                        elif event.key == pg.K_SPACE:
                            #do the check
                            self.gameScreen.check_word()
                        else:
                            self.gameScreen.typeBox.appendText(event.unicode)
                    
                #if the gamestate is in mainMenu
                elif(self.state.getState() == "MainMenu"):
                    if(self.mainMenu.startGameButton.getPressed()):
                        self.state.change_state("DifficultySelectScreen")
                    
                    elif(self.mainMenu.settingsButton.getPressed()):
                        pass
                    
                    elif(self.mainMenu.leaderboardButton.getPressed()):
                        pass

                    elif(self.mainMenu.logoutButton.getPressed()):
                        self.state.change_state("LoginScreen")

                    elif(self.mainMenu.quitButton.getPressed()):
                        self.dataCenter.SaveToFile()
                        self.run = False

                #if the gamestate is in gameScreen    
                elif(self.state.getState() == "GameScreen"):
                    pass

                #if the gamestate is in DifficultySelectScreen
                elif(self.state.getState() == "DifficultySelectScreen"):
                    if(self.difficultySelectScreen.backButton.getPressed()):
                        self.state.change_state("MainMenu")
                    
                    elif(self.difficultySelectScreen.easyButton.getPressed()):
                        self.gameScreen.dictionary = myDictionary()
                        self.gameScreen.dictionary.setDifficulty("easy")
                        self.state.change_state("GameScreen")
                    
                    elif(self.difficultySelectScreen.mediumButton.getPressed()):
                        self.gameScreen.dictionary = myDictionary()
                        self.gameScreen.dictionary.setDifficulty("medium")
                        self.state.change_state("GameScreen")
                    
                    elif(self.difficultySelectScreen.hardButton.getPressed()):
                        self.gameScreen.dictionary = myDictionary()
                        self.gameScreen.dictionary.setDifficulty("hard")
                        self.state.change_state("GameScreen")

            ##################
            # Screen Drawing #
            ##################

            #if loginScreen is active draw that
            if (self.state.getState() == "LoginScreen"):                 

                self.loginScreen.draw()
                if(self.mouseFocus != 0):
                    if(self.loginScreen.loginButton.collidepoint(event.pos)):
                        self.loginScreen.loginButton.setHover()
            
            if (self.state.getState() == "MainMenu"):
                self.mainMenu.updateUser(self.user)
                self.mainMenu.draw()
            
            #if GameScreen is active draw GameScreen
            if(self.state.getState() == "GameScreen"):
                if(self.gameScreen.failed == False):
                    self.gameScreen.draw()
                else:
                    self.state.change_state("DifficultySelectScreen")
                    self.gameScreen.failed = False
                    #remove all words
                    self.gameScreen.words = []

            if(self.state.getState() == "DifficultySelectScreen"):
                self.difficultySelectScreen.draw()
            

            #draw the fps for all screns
            self.fpscounter.draw()
            #update the screen with new objects
            pg.display.flip()

            self.fpscounter.count_fps()
            self.clock.tick(self.fpscounter.tickrate)


#main loop
game = Game()
game.start()

pg.quit()