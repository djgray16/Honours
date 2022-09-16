# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 12:03:11 2022

@author: djgra
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
CI = 0
MeansOnly = 1

filename = 'ID_RRG_long_100'

title = ' Imitation Dynamics: RRG model'

legend = 0


control_board = {'run': run, 'save': save,'title': title,
                 'filename': filename, 'reps': reps, 'CI': CI,
                 'MeansOnly': MeansOnly, 'legend': legend}


parameters = {
    'seed':42,
    'steps': 10_000, #number of time periods
    'agent_n': 100,
    'phi':ap.Values(6.0,6.25,6.5,6.75,7,7.25,7.5,7.75), # #multiplier for common contributions
    'graph_m' : 6,#ap.Values(4,6,8,10,12),
    'graph_alpha': 0.3,# ap.Values(0.01,0.1,0.25,0.5, 0.75,1.0),
    'graph_p':0.1,#ap.Values(0.1,0.2,0.3,0.4,0.5),
    'power_p': 0, #ap.Values(0.1, 0.2,0.3,0.4,0.5),#ap.Values(0.01,0.2,0.4,0.6,0.8),
    'gtype': 'RRG',
    'atype': ReplicatorLocal,
    'replicator_alpha': 0.0, #1 is pure replicator, 0 is imitation
    'plot_G': 0, #gives the summary plot of the graph for each experiment
    'step_reporting':0,
    'end_reporting':0
}

experiment(parameters, control_board)
aa

#################################################################
control_board['title'] = 'Replication of Figure 5a'

control_board['filename'] = 'TAfig5a'

parameters['graph_alpha'] = 0.0

#experiment(parameters, control_board)



#################################################################
control_board['title'] = 'Replication of Figure 5b'

control_board['filename'] = 'TAfig5b'

parameters['graph_alpha'] = 1.0

experiment(parameters, control_board)


######################################################################
control_board['title'] = 'Empirical 2.5%, 97.5% Quantiles for TA Model: alpha = 0.3'

control_board['filename'] = 'sensitivity2'

parameters['graph_alpha'] = 0.3

control_board['MeansOnly'] = 0
control_board['CI'] = 0



experiment(parameters, control_board)


######################################################################
control_board['title'] = '95% Confidence Interval for TA Model: alpha = 0.3'

control_board['filename'] = 'sensitivity1'

parameters['graph_alpha'] = 0.3

control_board['MeansOnly'] = 0
control_board['CI'] = 1



experiment(parameters, control_board)




