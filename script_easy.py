# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 12:20:41 2022

@author: s4482670
"""
import pickle as pickle
fname = 'results_script_test2'

#results = [i for i in range(1000)]
with open (f'{fname}.pickle', 'rb') as handle:
     tt = pickle.load( handle)