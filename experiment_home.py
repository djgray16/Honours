# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 19:38:13 2022

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

parameters = {
    'steps': 400, #number of time periods
    'agent_n': 600,
    'phi':ap.Values(2,3,4,5,6,7,8), #multiplier for common contributions
    'graph_m' : 6,
    'graph_alpha': 0.3,
    'graph_p':0.05,
    'gtype': 'WS',
    'atype': ReplicatorLocal,
    'replicator_alpha': 1.0, #1 is pure replicator, 0 is imitation
    'plot_G': 0 #gives the summary plot of the graph for each experiment
}


sample = ap.Sample(
    parameters,
    n=4,
    method='linspace'
)


exp = ap.Experiment(WealthModel, sample, iterations=10,
                    record = True)
results = exp.run()


phis = results.parameters.sample.phi
coops = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).mean()
ts = coops.index
ts = ts.get_level_values(0).unique()

df = results.parameters.sample
coops2 = coops.to_frame().join(df)

phi_graph = coops2.groupby(['t', 'phi']).mean()

#m_graph = coops2.groupby(['t', 'graph_m']).mean()

for i in phis.unique():
    y = phi_graph.Cooperation_Level.iloc[phi_graph.index.get_level_values('phi') == i]
    x = phis.index
    #plt.legend(phis.unique())
    plt.plot(ts,y)
    
plt.legend(phis.unique())
plt.title(f'Parameters: {parameters["agent_n"]} agents, \
graph: {parameters["gtype"]}, agents: {parameters["atype"]}, graph_alpha: {parameters["graph_alpha"]}, m: {parameters["graph_m"]}: replicator_alpha: {parameters["replicator_alpha"]} '
          )
    
    

            