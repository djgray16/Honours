# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 14:18:59 2022

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
    'steps': 300, #number of time periods
    'agent_n': 500,
    'phi':ap.Values(2,3,4,5,6,7), #multiplier for common contributions
    'graph_m' : 6,
    'graph_alpha': 0.3,
    'graph_p':0.1,
    'gtype': ap.Values('WS','TAG','BA', 'RRG'),
    'atype': AT,
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

phi_graph = coops2.groupby(['t', 'phi', 'gtype']).mean()
'''
#m_graph = coops2.groupby(['t', 'graph_m']).mean()

for i in phis.unique():
    y = phi_graph.Cooperation_Level.iloc[phi_graph.index.get_level_values('phi') == i]
    #x = phis.index
    #plt.legend(phis.unique())
    plt.plot(ts,y)
    
plt.legend(phis.unique())
plt.title(f'Parameters: {parameters["agent_n"]} agents, \
graph: {parameters["gtype"]}, agents: {parameters["atype"]}, alpha: {parameters["graph_alpha"]}, m: {parameters["graph_m"]}: alpha: {parameters["replicator_alpha"]} '
          )
    
    
'''


phi_graph = phi_graph.reset_index()
graphs = results.parameters.sample.gtype

fig,axs = plt.subplots(2,3, sharex = True, sharey = True)
fig.suptitle(f'Comparing Graph Structure with parameters N: {parameters["agent_n"]}, Degree: {parameters["graph_m"]} Agent: {parameters["atype"]}, repl_alpha: {parameters["replicator_alpha"]}')

axesx = [0,0,0,1,1,1]
axesy = [0,1,2,0,1,2]
for i in range(len(phis.unique())):
    #i=1.8
    testing =phi_graph[phi_graph.phi ==phis.unique()[i]]
    for j in graphs.unique():
        tt = testing.groupby(['t','gtype']).mean()
        ys = tt.Cooperation_Level.iloc[tt.index.get_level_values('gtype')==j]
        axs[axesx[i], axesy[i]].set_title(f' phi: {phis.unique()[i]}')
        
        axs[axesx[i], axesy[i]].plot(ts,ys, label = j)
        #axs[axesx[i], axesy[i]].legend()
        
        
handles, labels = axs[-1][-1].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower left')


for ax in axs.flat:
    ax.set(xlabel = 'Steps')
    ax.set(ylabel = 'Cooperation')
    ax.label_outer()
    
fig.set_size_inches(6,4)




        
        
            