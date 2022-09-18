# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 16:50:56 2022

@author: djgra
"""

import pickle as pickle
import agentpy as ap
import numpy as np
import random as random
import networkx as nx

from TAG import *
from Agents import *
from Models import *
import math
from experiment_functions import *

# Visualization
#import seaborn as sns

import matplotlib.pyplot as plt

import pickle as pickle
run = 1
save = 0
reps = 100
v2 = 'graph_p'
filename = 'graph_p_low_new'
title = 'Varying rewiring p, WS Model, Replicator Dynamics'
MeansOnly = 1
CI = 1
legend = 0



control_board = {'run': run, 'v2': v2, 'save': save,'title': title,
                 'filename': filename, 'reps': reps, 'MeansOnly': MeansOnly, 
                 'CI': CI, 'legend': legend}
fname = 'graph_p_low_new'
with open (f'{fname}.pickle', 'rb') as handle:
     pickle_in = pickle.load( handle)
     
plot_compare_two_from_pickle(pickle_in, control_board)

     
     