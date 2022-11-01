# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 12:20:41 2022

@author: s4482670
"""
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
v2 = 'graph_p'
filename = 'graph_p_low_new'
title = 'Varying rewiring p, WS Model, Replicator Dynamics'
MeansOnly = 1
CI = 0
legend = 0



control_board = {'run': run, 'v2': v2, 'save': save,'title': title,
                 'filename': filename, 'reps': reps, 'MeansOnly': MeansOnly, 
                 'CI': CI, 'legend': legend}

fname = 'graph_p_high_new'

#results = [i for i in range(1000)]
with open (f'{fname}.pickle', 'rb') as handle:
     results = pickle.load( handle)

     
fig, axs = plot_compare_two(results, control_board)


if save: 
    plt.savefig(f'Overleaf/images/{fname}.pdf')
    print(f'saved fig: {title} as {fname}')
    #plt.close(fig)