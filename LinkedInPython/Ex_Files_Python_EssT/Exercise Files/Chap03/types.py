#!/usr/bin/env python3
# Copyright 2009-2017 BHG http://bw.org/

x = (1, 2.0, 'two', [4, 5])
y = (1, 2, 4)
z = [1, 2, 3]
z[1] = 5
print('x is {}'.format(x))
print(type(x[1]))
print(type(y[1]))
print(type(z[1]))