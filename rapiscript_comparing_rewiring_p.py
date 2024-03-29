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
import pickle as pickle

# Visualization
#import seaborn as sns

import matplotlib.pyplot as plt



run = 1
save = 1
reps = 100
v2 = 'graph_p'
filename = 'Rep_graph_p_superlong_low'
title = 'Varying Rewiring p, WS Model, Replicator Dynamics'
MeansOnly = 1
CI = 0
legend = 0



control_board = {'run': run, 'v2': v2, 'save': save,'title': title,
                 'filename': filename, 'reps': reps, 'MeansOnly': MeansOnly, 
                 'CI': CI, 'legend': legend}


parameters = {
    'seed':42,
    'steps': 25_000, #number of time periods
    'agent_n': 100,
    'phi':ap.Values(4.0,4.25,4.5,4.75), # #multiplier for common contributions
    'graph_m' : 6,#ap.Values(4,6,8,10,12),
    'graph_alpha': 0.3,# ap.Values(0.01,0.1,0.25,0.5, 0.75,1.0),
    'graph_p':ap.Values(0.1,0.2,0.3,0.4,0.5),
    'power_p': 0, #ap.Values(0.1, 0.2,0.3,0.4,0.5),#ap.Values(0.01,0.2,0.4,0.6,0.8),
    'gtype': 'WS', #ap.Values('WS', 'TAG', 'BA', 'RRG'),
    'atype': 'ReplicatorLocal',
    'replicator_alpha': 1.0, #1 is pure replicator, 0 is imitation
    'plot_G': 0, #gives the summary plot of the graph for each experiment
    'step_reporting':0,
    'end_reporting':0
}
'''
results = run_compare_two(parameters, control_board)

fname = control_board['filename']
with open (f'{fname}.pickle', 'wb') as handle:
    pickle.dump(results, handle)
'''

####################################################################



control_board['filename'] = 'Rep_graph_p_superlong_med'

parameters['phi'] = ap.Values(5.0,5.25,5.5,5.75)

results = run_compare_two(parameters, control_board)

fname = control_board['filename']
with open (f'{fname}.pickle', 'wb') as handle:
    pickle.dump(results, handle)


#####################################################################

control_board['filename'] = 'Rep_graph_p_superlong_high'

parameters['phi'] = ap.Values(6.0,6.25,6.5,6.75)

results = run_compare_two(parameters, control_board)

fname = control_board['filename']
with open (f'{fname}.pickle', 'wb') as handle:
    pickle.dump(results, handle)


#######################################################################


