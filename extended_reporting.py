# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 09:32:47 2022

@author: djgra
"""


import agentpy as ap
import numpy as np
import random as random
import networkx as nx

from TAG import *
from Agents import *
from Models import *

# Visualization
#import seaborn as sns

import matplotlib.pyplot as plt
#random.seed(2)


#### control box
save = 1 #save the figure
run =0



filename = 'BA_degree_groups_45'
 #TODO test phi large, then test WS p over phi, then examine cooperation
 # of BA grouped by node degree. also rewrite the markov ODE part of before




parameters = {
    'seed':52,
    'steps': 200, #number of time periods
    'agent_n': 500,
    'phi':4.5,#ap.Values(2.0,2.5,3.0,3.5), # #multiplier for common contributions
    'graph_m' : 6,
    'graph_alpha': 0,# ap.Values(0.01,0.1,0.25,0.5, 0.75,1.0),
    'graph_p':0,#ap.Values(0.1,0.2,0.3,0.4,0.5),
    'power_p': 0,#ap.Values(0.1, 0.2,0.3,0.4,0.5),#ap.Values(0.01,0.2,0.4,0.6,0.8),
    'gtype': 'BA', #ap.Values('WS', 'TAG', 'BA', 'RRG'),
    'atype': ReplicatorLocal,
    'replicator_alpha': 1.0, #1 is pure replicator, 0 is imitation
    'plot_G': 0, #gives the summary plot of the graph for each experiment
    'extended_reporting': 1
}


sample = ap.Sample(
    parameters,
    n=1,
    method='linspace'
)
#assert len(parameters['phi'])==4

reps = 80
exp = ap.Experiment(WealthModel, sample, iterations=reps,
                    record = True)

if run:
    results = exp.run()

colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',\
           'tab:pink','tab:olive', 'tab:cyan', 'tab:gray' ]
    
markers = ['2', '3','1','8','^','s','p','X','h','d']
markers =['o','*', 'x', 'p', 's', 'd', 'p', 'h']



counts =  results.variables.ReplicatorLocal.groupby(['degree']).count().next_contribute

end_coop =  results.variables.ReplicatorLocal.groupby(['degree']).mean().next_contribute
agg_coop = results.variables.WealthModel.groupby(['t']).mean()

agg_coop_end = agg_coop.values[200]
log_counts = np.log(counts)
fig, bar_ax = plt.subplots()


bar_ax.hist(counts.index, weights = counts, log = 1, density = 0, alpha = 0.6, bins = 50)
bar_ax.set_xlabel('Degree Size')
bar_ax.set_ylabel('Count of Nodes')
line_ax = bar_ax.twinx()
line_ax.plot(end_coop, marker = 'o', color = 'black')
line_ax.hlines(agg_coop_end,end_coop.index.min(), end_coop.index.max(), color = 'r', linewidth = 3, linestyle = 'dashed')
line_ax.set_ylabel('Final Cooperation')

fig.suptitle('Final Cooperation vs Node Degree: BA Model')


#

if save: 
    plt.savefig(f'Overleaf/images/{filename}.png')
    
plt.show()

