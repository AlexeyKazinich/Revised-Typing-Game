# imports
import pygame as pg
import time
import numpy as np
import threading
import math

#custom class imports
from screens import *
from userData import *
from fpsCounter import *

#custom class imports

pg.init()

#window definitions
window = pg.display.set_mode((500,500))
pg.display.set_caption('typging game')

#other variables for the game game_loop
clock = pg.time.Clock()
is_running = True
class Game_States:
    def __init__(self) -> None:
        #state 
        self._state = "LoginScreen" 
        
        #screens
        self._loginscreen = LoginScreen(window)
        self._mainmenu = MainMenuScreen(window)
        self._difficultySelectScreen = DifficultySelectScreen(window)
        self._gameScreen = GameScreen(window)
        #all data for the user after logging in
        self._user = User()
        self._data_center = DataCenter()

        #fps counter
        self.fpscounter = FPSCounter(window)
    def loginscreen_state(self) -> None:
        #events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                is_running = False

            #checks if login or signup is pressed, and then checks if the credentials are valid
            #fix this so it runs through the screen class rather than here
            if(self._loginscreen.loginButton.get_pressed()):
                print("pressed login")
                if(self._data_center.login(self._loginscreen.usernameBox.text,self._loginscreen.passwordBox.text)):
                            self._user = self._data_center.user
                            self._state = "MainMenu"
            
            if(self._loginscreen.signUpButton.get_pressed()):
                print("pressed signup")
                if(self._data_center.signup(self._loginscreen.usernameBox.text,self._loginscreen.passwordBox.text)):
                            self._user = self._data_center.user

            #checks key presses 
            if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LCTRL:
                        self._loginscreen.shortcut_event_pressdown("LCTRL")
                    elif event.key == pg.K_BACKSPACE:
                        self._loginscreen.shortcut_event_pressdown("BACKSPACE")
                    elif event.key == pg.K_TAB:
                        self._loginscreen.shortcut_event_pressdown("TAB") 
                    else:
                        self._loginscreen.button_press_event(event.unicode)
            
            #checks key releases
            elif event.type == pg.KEYUP:
                if event.key == pg.K_LCTRL:
                    self._loginscreen.shortcut_event_release("LCTRL")
                elif event.key == pg.K_BACKSPACE:
                    self._loginscreen.shortcut_event_release("BACKSPACE")


        #drawing everything
        self._loginscreen.draw()
        
    def mainmenu_state(self) -> None:
        self._mainmenu.update_user(self._user)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                is_running = False
            
            if self._mainmenu.quitButton.get_pressed():
                pg.quit()
                is_running = False
            elif self._mainmenu.logoutButton.get_pressed():
                self._state = "LoginScreen"
                
            elif self._mainmenu.startGameButton.get_pressed():
                self._state = "DifficultySelectScreen"
        #drawing everything
        self._mainmenu.draw()
    
    def difficultyscreen_state(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                is_running = False

            if self._difficultySelectScreen.backButton.get_pressed():
                self._state = "MainMenu"
            elif self._difficultySelectScreen.easyButton.get_pressed():
                self._gameScreen = GameScreen(window) #new instance
                self._gameScreen.dictionary = MyDictionary()
                self._gameScreen.dictionary.set_difficulty("easy")
                self._state = "GameScreen"
            elif self._difficultySelectScreen.mediumButton.get_pressed():
                pass
            elif self._difficultySelectScreen.hardButton.get_pressed():
                pass
        #drawing everything
        self._difficultySelectScreen.draw()
        
        
    def gamescreen_state(self) -> None:
        #event loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                is_running = False
                
        #check if the user failed        
        if self._gameScreen.failed:
            self._state = "DifficultySelectScreen"
        #draw
        self._gameScreen.draw()
        
        
    def state_controller(self) -> None:
        #draw the state that the game is currently in
        if(self._state == "LoginScreen"):
            self.loginscreen_state()
            
        elif(self._state == "MainMenu"):
            self.mainmenu_state()
            
        elif(self._state == "DifficultySelectScreen"):
            self.difficultyscreen_state()
            
        elif(self._state == "GameScreen"):
            self.gamescreen_state()
        
        #draw the fps counter    
        self.fpscounter.draw()
        pg.display.flip()
        self.fpscounter.count_fps() #count fps


game_state = Game_States()
while is_running:
    game_state.state_controller()
    clock.tick(60) 