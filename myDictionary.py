import pickle
import random


class myDictionary:
    def __init__(self) -> None:
        self.dictionary = pickle.load(open("SAVE_DATA/Data/MyDictionary.txt","rb"))
        self.easyDictionary = []
        self.mediumDictionary = []
        self.hardDictionary = []
        self.dictionaryLength = len(self.dictionary)
        self.useDictionary = []
        self.make_difficulty()


    def make_difficulty(self) -> None:
        for word in self.dictionary:
            wordLength = len(word)
            if(wordLength < 5):
                self.easyDictionary.append(word)
            elif(wordLength < 7):
                self.mediumDictionary.append(word)
            elif(wordLength < 8):
                self.hardDictionary.append(word)

    def set_difficulty(self, difficult: str) -> None:
        if(difficult =="easy"):
            self.useDictionary = self.easyDictionary
        elif(difficult =="medium"):
            self.useDictionary = self.mediumDictionary
        elif(difficult =="hard"):
            self.useDictionary = self.hardDictionary

    def get_words(self) -> str:
        length = len(self.useDictionary)
        return(self.useDictionary[random.randint(0, length-1)])
