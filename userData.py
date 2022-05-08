import pygame as pg
import multiprocessing as mp
import time
import numpy as np
import threading
import pickle


class DataCenter:
    def __init__(self):
        #load all data in
        self.allusers = []
        self.user = User()
        self.read_from_file()

    def login(self, username, password):
        for user in self.allusers:
            if(user.username == username and user.password == password):
                if(len(user.username) != 0):
                    print("Success")
                    self.user = user
                    return True
                
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
            #print("USERNAME: "+user.username+" PASSWORD: "+user.password)
            pass



#user object itself
class User:
    def __init__(self):
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



    def get_acc(self):
        num = 0.0
        if(len(self.TopTenAcc) != 0):
            for a in self.TopTenAcc:
                num += a

            return num / (self.TopTenAcc)
        
        else: return 0.0





    

