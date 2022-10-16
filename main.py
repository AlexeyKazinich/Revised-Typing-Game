#imports
import pygame as pg
import time
import numpy as np
import threading
import math

#custom class imports
from screens import *
from objects import *
from userData import *
from fpsCounter import *


pg.init()


#window definitions
window = pg.display.set_mode((500,500))
pg.display.set_caption('typing game')


#REPLACE THIS WITH GAMESTATE
#keeps track of current game state
class State:
    def __init__(self):
        self.__state = "LoginScreen"
    
    def change_state(self, state):
        self.__state = state

    def get_state(self):
        return self.__state


#Main class
class Game:
    def __init__(self):
        #keeps track of the screen
        self.state = State()
        
        #fps
        self.fpscounter = FPSCounter(window)

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
        self.game_loop()

    #main loop
    def game_loop(self):
        self.run = True
        while self.run:

            #listen to clicks
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.dataCenter.save_to_file()
                    self.run = False
                
                #all buttons and other checks with logic for LoginScreen
                if(self.state.get_state() == "LoginScreen"):
                    if(self.loginScreen.loginButton.get_pressed()):
                        if(self.dataCenter.login(self.loginScreen.usernameBox.text,self.loginScreen.passwordBox.text)):
                                self.user = self.dataCenter.user
                                self.state.change_state("MainMenu")
                        
                    elif(self.loginScreen.signUpButton.get_pressed()):
                        if(self.dataCenter.signup(self.loginScreen.usernameBox.text,self.loginScreen.passwordBox.text)):
                            self.user = self.dataCenter.user
                            self.state.change_state("MainMenu")

                    
                
                    if event.type == pg.KEYDOWN:  
                        if(self.loginScreen.usernameBox.focused):
                            #print(self.loginScreen.usernameBox.text)
                            #print(self.loginScreen.usernameBox.holdingCtrl)
                            if event.key == pg.K_BACKSPACE:
                                if(self.loginScreen.usernameBox.holdingCtrl == True):
                                    self.loginScreen.usernameBox.cntrl_backspace()
                                else:
                                    self.loginScreen.usernameBox.backspace()
                            elif event.key == pg.K_LCTRL:
                                self.loginScreen.usernameBox.holdingCtrl = True
                            elif event.key == pg.K_TAB:
                                self.loginScreen.usernameBox.set_deactive()
                                self.loginScreen.passwordBox.set_active()
                            else:
                                self.loginScreen.usernameBox.append_text(event.unicode)
                        
                        elif(self.loginScreen.passwordBox.focused):
                            if event.key == pg.K_BACKSPACE:
                                self.loginScreen.passwordBox.backspace()
                            else:
                                self.loginScreen.passwordBox.append_text(event.unicode)
                    

                    #if a key was released
                    elif event.type == pg.KEYUP:
                        #if current box thats active is usernameBox
                        if(self.loginScreen.usernameBox.isActive):
                            #if the key that was released was left ctrl
                            if event.key == pg.K_LCTRL:
                                self.loginScreen.usernameBox.holdingCtrl = False #set holding control to false
                elif(self.state.get_state() == "GameScreen"):
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            self.gameScreen.typeBox.backspace()
                        elif event.key == pg.K_SPACE:
                            #do the check
                            self.gameScreen.check_word()
                        else:
                            self.gameScreen.typeBox.append_text(event.unicode)
                    
                #if the gamestate is in mainMenu
                elif(self.state.get_state() == "MainMenu"):
                    if(self.mainMenu.startGameButton.get_pressed()):
                        self.state.change_state("DifficultySelectScreen")
                    
                    elif(self.mainMenu.settingsButton.get_pressed()):
                        pass
                    
                    elif(self.mainMenu.leaderboardButton.get_pressed()):
                        pass

                    elif(self.mainMenu.logoutButton.get_pressed()):
                        self.state.change_state("LoginScreen")

                    elif(self.mainMenu.quitButton.get_pressed()):
                        self.dataCenter.save_to_file()
                        self.run = False

                #if the gamestate is in gameScreen    
                elif(self.state.get_state() == "GameScreen"):
                    pass

                #if the gamestate is in DifficultySelectScreen
                elif(self.state.get_state() == "DifficultySelectScreen"):
                    if(self.difficultySelectScreen.backButton.get_pressed()):
                        self.state.change_state("MainMenu")
                    
                    elif(self.difficultySelectScreen.easyButton.get_pressed()):
                        self.gameScreen.dictionary = MyDictionary()
                        self.gameScreen.dictionary.set_difficulty("easy")
                        self.state.change_state("GameScreen")
                    
                    elif(self.difficultySelectScreen.mediumButton.get_pressed()):
                        self.gameScreen.dictionary = MyDictionary()
                        self.gameScreen.dictionary.set_difficulty("medium")
                        self.state.change_state("GameScreen")
                    
                    elif(self.difficultySelectScreen.hardButton.get_pressed()):
                        self.gameScreen.dictionary = MyDictionary()
                        self.gameScreen.dictionary.set_difficulty("hard")
                        self.state.change_state("GameScreen")

            ##################
            # Screen Drawing #
            ##################

            #if loginScreen is active draw that
            if (self.state.get_state() == "LoginScreen"):                 

                self.loginScreen.draw()
                if(self.mouseFocus != 0):
                    if(self.loginScreen.loginButton.collidepoint(event.pos)):
                        self.loginScreen.loginButton.set_hover()
            
            if (self.state.get_state() == "MainMenu"):
                self.mainMenu.update_user(self.user)
                self.mainMenu.draw()
            
            #if GameScreen is active draw GameScreen
            if(self.state.get_state() == "GameScreen"):
                if(self.gameScreen.failed == False):
                    self.gameScreen.draw()
                else:
                    self.state.change_state("DifficultySelectScreen")
                    self.gameScreen.failed = False
                    #remove all words
                    self.gameScreen.words = []
                    self.user.increase_xp(500)

            if(self.state.get_state() == "DifficultySelectScreen"):
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