# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 23:34:48 2019

@author: Omar
"""

def fib(n):
    
    a, b = 0, 1
    
    while a < n:
        print(a, end=' ')
        a, b = b, a + b
        
    print()