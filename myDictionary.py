import pickle
import random


class MyDictionary:
    def __init__(self) -> None:
        self.dictionary = pickle.load(open("SAVE_DATA/Data/MyDictionary.txt","rb"))
        self.easyDictionary = []
        self.mediumDictionary = []
        self.hardDictionary = []
        self.dictionaryLength = len(self.dictionary)
        self.useDictionary = []
        self.make_difficulty()
        self._difficulty = ""
        self._difficulty_float = 0.0

    def get_difficulty(self) -> str:
        return self._difficulty
    
    def get_difficulty_float(self) -> float:
        return self._difficulty_float

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
            self._difficulty = "easy"
            self._difficulty_float = 1.5
        elif(difficult =="medium"):
            self.useDictionary = self.mediumDictionary
            self._difficulty = "medium"
            self._difficulty_float = 2.0
        elif(difficult =="hard"):
            self.useDictionary = self.hardDictionary
            self._difficulty_float = 4.0

    def get_words(self) -> str:
        length = len(self.useDictionary)
        return(self.useDictionary[random.randint(0, length-1)])
