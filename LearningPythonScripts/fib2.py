# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 23:42:14 2019

@author: Omar
"""
def fib2(n):
    
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a + b
        
    return result
