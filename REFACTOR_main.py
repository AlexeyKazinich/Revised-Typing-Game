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
        
        #all data for the user after logging in
        self._user = User()
        self._data_center = DataCenter()

        #fps counter
        self.fpscounter = fpsCounter(window)
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
        pass

    def state_controller(self) -> None:
        if(self._state == "LoginScreen"):
            self.loginscreen_state()
        elif(self._state == "MainMenu"):
            self.mainmenu_state()

        self.fpscounter.draw()
        pg.display.flip()
        self.fpscounter.count_fps()


game_state = Game_States()
while is_running:
    game_state.state_controller()
    clock.tick(60) 