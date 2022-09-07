# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 10:46:44 2022

@author: djgra
"""


import agentpy as ap
import numpy as np
import random as random
import networkx as nx
import IPython

from TAG import *
from Agents import *
from Models import *

# Visualization
#import seaborn as sns

import matplotlib.pyplot as plt


def animation_plot(m, axs):
    color_dict = {0: 'r', 1: 'g'}
    print(m.agents.contribute)
    colors = [color_dict[c] for c in m.agents.contribute]
    #print(m.network.graph)
    nx.draw_circular(m.network.graph, node_color = colors, node_size = 50, ax = axs)

fig, axs = plt.subplots(figsize = (8,8))


parameters = {
    'seed':52,
    'steps': 10, #number of time periods
    'agent_n': 10,
    'phi':3.0,#ap.Values(2.0,2.5,3.0,3.5), # #multiplier for common contributions
    'graph_m' : 4,
    'graph_alpha': 0,# ap.Values(0.01,0.1,0.25,0.5, 0.75,1.0),
    'graph_p':0,#ap.Values(0.1,0.2,0.3,0.4,0.5),
    'power_p': 0,#ap.Values(0.1, 0.2,0.3,0.4,0.5),#ap.Values(0.01,0.2,0.4,0.6,0.8),
    'gtype': 'WS', #ap.Values('WS', 'TAG', 'BA', 'RRG'),
    'atype': ReplicatorLocal,
    'replicator_alpha': 1.0, #1 is pure replicator, 0 is imitation
    'plot_G': 1, #gives the summary plot of the graph for each experiment
    'extended_reporting': 0
}



model = WealthModel(parameters)
results = model.run()
#%matplotlib qt
#animation = ap.animate(WealthModel(parameters), fig, axs, animation_plot)

