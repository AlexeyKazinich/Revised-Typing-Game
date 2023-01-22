from cgitb import text
import pygame as pg
import multiprocessing as mp
import numpy as np
from typing import Union
#module import
from myDictionary import MyDictionary
from objects import *
from userData import *




class Screen:
    #called by all child classes
    def __init__(self,window)-> None:
        #colors
        self.activeColor = 'dodgerblue2'
        self.inactiveColor = 'lightskyblue3'
        #window
        self.window = window


    def draw(self)-> None:
        self.window.fill((0,0,0))




class LoginScreen(Screen):
    
    def add_objects(self)-> None:

        #text boxes
        self.usernameBox = TextBox(100,100,140,32,self.window)
        self.usernameBox.set_color(self.inactiveColor)

        self.passwordBox = TextBox(100,164,140,32,self.window, True)
        self.passwordBox.set_color(self.inactiveColor)

        self.rectangles.append(self.usernameBox)
        self.rectangles.append(self.passwordBox)

        #buttons
        self.loginButton = Button(340,164,90,32,'login',self.window)
        self.signUpButton = Button(340,100,90,32,'signup',self.window)
    
        #modifier
        self.holding_LCTRL = False

    def __init__(self,window)-> None:
        super().__init__(window)
        self.rectangles = []
        self.add_objects() #adds textboxes and buttons
        self.__allUsers = [] #array of users
        self.user = User() #creats a default user
        self.__read_from_file() #loads allUsers


    def set_active(self, target)-> None:
        if target == "usernameBox":
            self.usernameBox.set_active()
            self.passwordBox.set_deactive()
        elif target == "passwordBox":
            self.passwordBox.set_active()
            self.usernameBox.set_deactive()
        else:
            self.passwordBox.set_deactive()
            self.usernameBox.set_deactive()

    def __write_to_file(self)-> None:
        pickle.dump(self.__allUsers,open("SAVE_DATA/Game_Data/Users.txt","wb"))

    def __read_from_file(self)-> None:
        try:
            self.__allUsers = pickle.load(open("SAVE_DATA/Game_Data/Users.txt","rb"))
        except FileNotFoundError:
            self.__write_to_file()

    def login_attempt(self) -> bool:
        for user in self.__allUsers:
            #print("username: " + user.username)
            #print("password: " + user.password)
            if(user.username == self.usernameBox.text and user.password == self.passwordBox.text):
                self.user = user
                return True
        return False

    #This takes unicode for letters and can take string for letters but not special characters
    def button_press_event(self,letter: Union[str,int]) -> None:

        #check what textbox is selected, add the letter
        if(self.usernameBox.isActive):
            self.usernameBox.append_text(letter)

        elif(self.passwordBox.isActive):
            self.passwordBox.append_text(letter)

    def shortcut_event_pressdown(self,shortcut: str)-> None:

        #checks if left ctrl is being held down
        if(shortcut == "LCTRL"):
            self.holding_LCTRL = True


        if(self.usernameBox.isActive):
            if(shortcut == "BACKSPACE"):
                if(self.holding_LCTRL):
                    self.usernameBox.cntrl_backspace()
                else:
                    self.usernameBox.backspace()
                    
            elif(shortcut == "TAB"):
                self.usernameBox.set_deactive()
                self.passwordBox.set_active()

        elif(self.passwordBox.isActive):
            if(shortcut == "BACKSPACE"):
                if(self.holding_LCTRL):
                    self.passwordBox.cntrl_backspace()
                else:
                    self.passwordBox.backspace()

            elif(shortcut == "TAB"):
                self.passwordBox.set_deactive()
        
        #checks if enter is pressed
    
    def shortcut_event_release(self,shortcut : str)-> None:
        #checks if its ctrl+backspace is released
        if(shortcut == "LCTRL"):
            self.holding_LCTRL = False

    
    def draw(self)-> None:
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
    def __init__(self,window)-> None:
        super().__init__(window)
        self.area = window.get_rect()
        self.buttons = []
        self.add_buttons()
        self.data_center = DataCenter.get_instance()
        self.userInfo = PlayerInfoBox(self.data_center.user,self.window) #type: ignore

    def add_buttons(self)-> None:
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
    
    def update_user(self)-> None:
        self.userInfo = PlayerInfoBox(self.data_center.user,self.window) #type: ignore
    
    def draw(self)-> None:
        self.update_user()
        self.window.fill((30,30,30))

        self.userInfo.draw()
        for button in self.buttons:
            button.draw()


class DifficultySelectScreen(Screen):
    def __init__(self,window)-> None:
        super().__init__(window)
        self.area = window.get_rect()
        self.buttons = []
        self.add_buttons() #adds the buttons
        self.add_user_box() #this is what shows the player stats

    def add_buttons(self)-> None:
        self.easyButton = Button(self.area.width/2 -150,self.area.height*1/6,150,32,"Easy Mode",self.window)
        self.mediumButton = Button(self.area.width/2 -150,self.area.height*2/6,150,32,"Normal Mode",self.window)
        self.hardButton = Button(self.area.width/2 -150,self.area.height*3/6,150,32,"Hard Mode",self.window)
        self.backButton = Button(self.area.width/2 -150,self.area.height*4/6,150,32,"back",self.window)

        self.buttons.append(self.easyButton)
        self.buttons.append(self.mediumButton)
        self.buttons.append(self.hardButton)
        self.buttons.append(self.backButton)
    
    def add_user_box(self)-> None:
        pass

    def draw(self)-> None:
        self.window.fill((30,30,30))
        for button in self.buttons:
            button.draw()
        
class GameScreen(Screen):
    
    def __init__(self,window,difficulty: str = "easy")-> None:
        super().__init__(window)
        self.dictionary = MyDictionary()
        self.words = []
        self.window = window
        self.area = self.window.get_rect()
        self.failed = False
        self.typeBox = TextBox(int(self.area.width/2-100),int(self.area.height-50),80,30,self.window)
        self.typeBox.set_active()
        
        self.data_center = DataCenter.get_instance()

        self.moveSpeed = 1 #speed for word movement
        self.speed = 1 #speed for score calculation
        self.accuracy = [0,0,100.0] #hit #miss #acc
        self.score = 10 #current player score
        self.current_performance = 0 #shows the pp on screen
        self.difficulty_mult = 0.0
        
        self.set_difficulty(difficulty)

        #onscreen text
        self._accuracy_text = Text(f"{self.accuracy[2]}%",0,0,window)

    def set_difficulty(self, difficulty : str):
        self.dictionary.set_difficulty(difficulty)
        self.difficulty_mult = self.dictionary.get_difficulty_float()

    #function runs whenever space is pressed or backspace
    def _calculate_acc(self):
        #update the accuracy
        try: 
            self.accuracy[2] = round((self.accuracy[0] / (self.accuracy[0] + self.accuracy[1])) * 100,2)
        except:
            self.accuracy[2] = 100.0
            
        #update the accuracy text
        self._accuracy_text.update_text(f"{self.accuracy[2]}%")
    
    #runs when the game ends
    #this function saves everything to the user
    def _failed(self):
        _xp_earned = self.score * self.accuracy[2] *450
        self.data_center.user.increase_xp(_xp_earned) #type: ignore
        self.data_center.user.completed_game(self.score,self.accuracy[2],self.speed,self.difficulty_mult) #type: ignore
        self.failed = True
    
    #function runs if the word was written wrong
    def _correct_input(self,word : Word):
        self.score = self.score + 1
        self.accuracy[0] += len(word.word) #adds to the correct index
        
        self._calculate_acc()
        
    #function runs if the word was written correctly
    def _incorrect_input(self):
        self.accuracy[1] += len(self.typeBox.text) #adds to the miss index
        self._calculate_acc()
        
    #function runs when space is clicking
    def check_word(self)-> None:
        _is_correct = False
        for word in self.words:
            if(self.typeBox.text == word.word):
                #remove word
                self.words.remove(word)
                self.typeBox.text = ""
                self._correct_input(word)
                _is_correct = True
        
        if(not _is_correct):
            self._incorrect_input()
            
        self.typeBox.text = ""
    
    
    
    def draw(self)-> None:
        if(len(self.words) < 4):
            self.words.append(Word(self.dictionary,self.window,0 - len(self.words)*25))
        
        
        self.window.fill((30,30,30))
        for word in self.words:
            word.draw()
            word.move(self.moveSpeed)
            #if word below screen 
            
        for word in self.words:
            if(word.y >= self.area.height):
                self._failed()
        self.typeBox.draw() #draw textbox
        
        self._accuracy_text.draw() #draw the accuracy text
        
        
    def button_press_event(self,letter: Union[str,int]) -> None:

        #check what textbox is selected, add the letter
            self.typeBox.append_text(letter)

    def shortcut_event_pressdown(self,shortcut: str)-> None:

        #checks if left ctrl is being held down
        if(shortcut == "SPACE"):
            self.check_word()
        elif(shortcut == "BACKSPACE"):
            self.typeBox.backspace()
            self.accuracy[1] += 1
            self._calculate_acc()

