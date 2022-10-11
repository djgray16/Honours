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
save = 1
reps = 100
v2 = 'graph_m'

MeansOnly = 0
CI = 0
legend = 0
size = 'high'
gmodel = 'BA'
filename = 'Imitation_graph_m_highRRG' #+'_home'
title = f'Empirical Quantiles, Comparing Models, Imitation Dynamics'




control_board = {'run': run, 'v2': v2, 'save': save,'title': title,
                 'filename': filename, 'reps': reps, 'MeansOnly': MeansOnly, 
                 'CI': CI, 'legend': legend}




fname = filename
with open (f'{fname}.pickle', 'rb') as handle:
     pickle_in = pickle.load( handle)
     
plot_compare_two_from_pickle(pickle_in, control_board)

## need to save here

save_now = 0
filename = 'ID_graph_p_' +size
if save_now: 
    plt.savefig(f'Overleaf/images/{filename}.pdf')
    print(f'saved fig: {title} as {filename}')
     
     