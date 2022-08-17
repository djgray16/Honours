# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 19:36:48 2022

@author: djgra
"""

import numpy as np
import math

x1 = -math.sqrt(3/5)
x2 = -1/2
x3 = -math.sqrt(3/20)
mu = (1+-math.sqrt(5/3))/2
lam = (1+-math.sqrt(15))/2



a = np.array([[2*(mu-lam), 0, 0, -2*x1, 2*x1 ], 
             [0, 2*(mu-lam), 0, -2*x2, 2*x2-2 ],
             [0,0, 2*(mu-lam), -2*x3, 2*x3 ],
             [2*x1, 2*x2, 2*x3, 0, 0],
             [2*x1, 2*x2-2, 2*x3, 0, 0]])


det = np.linalg.det(a)
print(det) ##30.98386676965935