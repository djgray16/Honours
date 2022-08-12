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
import math

# Visualization
#import seaborn as sns

import matplotlib.pyplot as plt
#random.seed(2)
'''
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


exp = ap.Experiment(WealthModel, sample, iterations=40,
                    record = True)
results = exp.run()



'''

### PLotting 




CI = True #whether to do parametric CI or empirical quantiles at 5% LOS

phis = results.parameters.sample.phi

colours = ['b', 'g', 'r', 'y', 'k', 'c', 'm']
colours = colours[:len(phis)]


coops = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).mean()

pct_up = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).quantile(0.975)
if CI:
    pct_up = coops + 1/math.sqrt(40)*1.96*results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).std()
pct_up = pct_up.rename('q_up')
pct_down = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).quantile(0.025)
if CI:
    pct_down = coops - 1/math.sqrt(40)*1.96*results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).std()

pct_down = pct_down.rename('q_down')

ts = coops.index
ts = ts.get_level_values(0).unique()

df = results.parameters.sample
coops2 = coops.to_frame().join(df).join(pct_up).join(pct_down)

phi_graph = coops2.groupby(['t', 'phi']).mean()

#m_graph = coops2.groupby(['t', 'graph_m']).mean()
plt.figure(figsize = (8,8))
for i in range(len(phis)):
    y1 = phi_graph.Cooperation_Level.iloc[phi_graph.index.get_level_values('phi') == phis[i]]
    y2 = phi_graph.q_down.iloc[phi_graph.index.get_level_values('phi') == phis[i]]
    y3 = phi_graph.q_up.iloc[phi_graph.index.get_level_values('phi') == phis[i]]
    x = phis.index
    #plt.legend(phis.unique())
    plt.plot(ts,y1, colours[i], label = f'r = {phis[i]}')
    plt.plot(ts,y2,  colours[i] + ':', label = f'_5th Percentile of {phis[i]}', alpha = 0.6 )
    plt.plot(ts,y3,  colours[i] + ':', label = f'_95th Percentile of {phis[i]}' , alpha = 0.6)
    

plt.legend( loc='upper left')

#plt.rcParams["figure.figsize"] = (10,10)
plt.title(f' {parameters["agent_n"]} agents,' \
f'graph: {parameters["gtype"]}, agents: {parameters["atype"]}, graph_alpha: ' \
    f'{parameters["graph_alpha"]}, m: {parameters["graph_m"]}: replicator_alpha:'\
        f' {parameters["replicator_alpha"]}, CI: {CI}'
          )
    
    

            