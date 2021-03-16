# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 23:51:56 2019

@author: Omar
"""

import random

class Numberguesser:

    
    def __init__(self):
        self.__number = random.randrange(0, 20)
    
    
    def guessTheNumber(self, i):
        
        if i == self.__number:
            print("you guessed right! congratulations smart ass")
            self.__number = random.randrange(0, 20)
            
        else:
                
            if i < self.__number:
                if self.__number - i > i:
                    print("That is way too low, dude!")
                    
                else:
                    print("Your guess is a little bit low, but close though!")
               
            else:
                if i > self.__number:
                    if 20 - i > i - self.__number:
                        print("That is way too high, dude!")
                    else:
                        print("Your guess is a little bit high, but close though!")
                            
                    
        
        