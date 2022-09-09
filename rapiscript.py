# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 14:25:11 2022

@author: s4482670
"""

import agentpy as ap
import numpy as np
import random as random
import networkx as nx

from TAG import *
from Agents import *
from Models import *
from experiment_functions import *
import math

# Visualization
#import seaborn as sns

import matplotlib.pyplot as plt



run = 1
save = 1
reps = 100
v2 = 'gtype'
filename = 'replicator_graphs_low'
title = 'Comparing Graph Models: Replicator Dynamics'




control_board = {'run': run, 'v2': v2, 'save': save,'title': title,
                 'filename': filename, 'reps': reps}


parameters = {
    'seed':42,
    'steps': 200, #number of time periods
    'agent_n': 500,
    'phi':ap.Values(2.0,2.5,3.0,3.5), # #multiplier for common contributions
    'graph_m' : 6,#ap.Values(4,6,8,10,12),
    'graph_alpha': 0.3,# ap.Values(0.01,0.1,0.25,0.5, 0.75,1.0),
    'graph_p':0.1,#ap.Values(0.1,0.2,0.3,0.4,0.5),
    'power_p': 0, #ap.Values(0.1, 0.2,0.3,0.4,0.5),#ap.Values(0.01,0.2,0.4,0.6,0.8),
    'gtype': ap.Values('WS', 'TAG', 'BA', 'RRG'),
    'atype': ReplicatorLocal,
    'replicator_alpha': 1.0, #1 is pure replicator, 0 is imitation
    'plot_G': 0, #gives the summary plot of the graph for each experiment
    'step_reporting':0,
    'end_reporting':0
}

compare_two(parameters, control_board)

control_board['filename'] = 'replicator_graphs_med'
parameters['phi'] = ap.Values(4.0,4.5,5.0,5.5)

compare_two(parameters, control_board)

control_board['filename'] = 'replicator_graphs_high'
parameters['phi'] = ap.Values(6.0,6.5,7.0,7.5)

compare_two(parameters, control_board)



