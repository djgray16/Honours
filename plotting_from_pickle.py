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

MeansOnly = 1
CI = 0
legend = 1
size = 'high'
gmodel = 'BA'
filename = 'graph_m_medBA' #+'_home'
title = f'Comparing Mean Degree, BA Model, Replicator Dynamics'




control_board = {'run': run, 'v2': v2, 'save': save,'title': title,
                 'filename': filename, 'reps': reps, 'MeansOnly': MeansOnly, 
                 'CI': CI, 'legend': legend}




fname = filename
with open (f'pickles/{fname}.pickle', 'rb') as handle:
     pickle_in = pickle.load( handle)
     
fig, axs = plot_one(pickle_in, control_board, 5.75)

## need to save here

save_now = 1
filename = 'presentation_graph_m_rep_legend' 
if save_now: 
    plt.savefig(f'Overleaf/images/{filename}.pdf')
    print(f'saved fig: {title} as {filename}')
     
     