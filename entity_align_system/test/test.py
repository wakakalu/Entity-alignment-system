# -*- coding:utf-8 -*-
from numpy import *

w=array(zeros((3,5)))
for i in range(3):
    for j in range(5):
        w[i][j]= i*j

print w[0].min()