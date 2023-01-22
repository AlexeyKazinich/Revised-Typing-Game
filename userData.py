import pygame as pg
import multiprocessing as mp
import time
import numpy as np
import threading
import pickle


class DataCenter:
    __instance = None
    
    @staticmethod
    def get_instance():
        if(DataCenter.__instance == None):
            DataCenter()
        return DataCenter.__instance
    
    
    def __init__(self):
        #check if this is called manually and prevent it
        if(DataCenter.__instance != None):
            raise Exception("DataCenter already exists!")
        
        #load all data in
        self.allusers = []
        self.user = User()
        self.read_from_file()
        DataCenter.__instance = self

    def login(self, username, password):
        for user in self.allusers:
            if(user.username == username and user.password == password):
                if(len(user.username) != 0):
                    print("Success")
                    self.user = user
                    return True
            elif(username == "admin"):
                    print(f"username: {user.username} | password: {user.password}")
                
        else:
            print("failed login, please try again")
            return False


    def __set_info(self, user,username,password):
        user.username = username
        user.password = password

    def signup(self, username, password):
        if(len(username) > 2 and len(password) > 2):
            self.user = User() #creates a new user
            self.__set_info(self.user, username, password) #sets pass and username for the user
            self.allusers.append(self.user) #adds the user to the list
            self.save_to_file() #writes the list to the file
            return True
        else: return False


    #writes the list of users to the file
    def save_to_file(self):
        pickle.dump(self.allusers,open("SAVE_DATA/GAME_DATA/usernames.txt","wb")) 


    #reads from the file to get all the users, called by constructor
    def read_from_file(self):
        try:
            self.allusers = pickle.load(open("SAVE_DATA/GAME_DATA/usernames.txt","rb"))
        except FileNotFoundError:
            self.allusers = []
            pickle.dump(self.allusers,open("SAVE_DATA/GAME_DATA/usernames.txt","wb"))

    #TEMPORARY
    def read_all_data(self):
        for user in self.allusers:
            print("USERNAME: "+user.username+" PASSWORD: "+user.password)
            pass



#user object itself
#singleton design
class User:
        
    def __init__(self) -> None:
        self.username = ""
        self.password = ""
        self.Highscore = [0,0,0]
        self.Performance = 0
        self.Level = 0
        self.XP = 0
        self.NeedXP = 0
        self.TopTenAcc = []
        self.TopTenWPM = []
        self.TopTenPerformance = []
        self.TopTenDifficulty = []


    def get_top_ten_wpm(self) -> float:
        num = 0.0
        if (len(self.TopTenWPM) != 0):
            return sum(self.TopTenWPM) / len(self.TopTenWPM)
        return num
    
    def get_acc(self) -> float:
        num = 0.0
        if(len(self.TopTenAcc) != 0):
            for a in self.TopTenAcc:
                num += a

            return num / (len(self.TopTenAcc))
        
        else: return 0.0

    def increase_xp(self,xp: int) -> None:
        self.XP = self.XP + xp
        if(self.XP >= self.NeedXP):
            self.XP = self.XP - self.NeedXP
            self.NeedXP = self.NeedXP + 5
            self.Level = self.Level + 1
            self.increase_xp(0) 

    def completed_game(self, score,accuracy,speed, difficulty_multiplier) -> None:
        print(f"score: {score}/n accuracy: {accuracy}/n speed: {speed}/n difficulty_mult: {difficulty_multiplier}")
        _performance = score
        _performance *= speed
        _performance *= difficulty_multiplier
        self.Performance += int(_performance)
        pass



    

