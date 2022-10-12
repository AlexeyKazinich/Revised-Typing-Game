import pygame as pg
from objects import *
from typing import Union
class object_manager():
    
    
    def __init__(self,window):
        #create a list of objects
        #loop through all objects and call the draw function
        #allow to add or remove objects from the object manager
        self._window = window
        
    def add_object(self, object: Union[Rectangle,ProgressBar,textBox, Button, playerInfoBox, Word, Text]) -> None:
        pass
    
    def remove_object(self, index : int) -> None:
        pass
    
    def draw(self) -> None:
        pass