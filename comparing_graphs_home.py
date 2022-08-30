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


#### control box
save = 0 #save the figure
run =1
v2 = 'graph_p'


filename = 'graph_p_high'
 #TODO test phi large, then test WS p over phi, then examine cooperation
 # of BA grouped by node degree. also rewrite the markov ODE part of before


parameters = {
    'seed':42,
    'steps': 200, #number of time periods
    'agent_n': 500,
    'phi':ap.Values(5.0,5.5,6.0,6.5), # #multiplier for common contributions
    'graph_m' : 6,#ap.Values(4,5,6,7,8),
    'graph_alpha': 0,# ap.Values(0.01,0.1,0.25,0.5, 0.75,1.0),
    'graph_p':ap.Values(0.1,0.2,0.3,0.4,0.5),
    'power_p': 0,#ap.Values(0.1, 0.2,0.3,0.4,0.5),#ap.Values(0.01,0.2,0.4,0.6,0.8),
    'gtype': 'WS', #ap.Values('WS', 'TAG', 'BA', 'RRG'),
    'atype': ReplicatorLocal,
    'replicator_alpha': 1.0, #1 is pure replicator, 0 is imitation
    'plot_G': 0 #gives the summary plot of the graph for each experiment
}


sample = ap.Sample(
    parameters,
    n=1,
    method='linspace'
)
assert len(parameters['phi'])==4

reps = 40
exp = ap.Experiment(WealthModel, sample, iterations=reps,
                    record = True)

if run:
    results = exp.run()

colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',\
           'tab:pink','tab:olive', 'tab:cyan', 'tab:gray' ]
    
markers = ['2', '3','1','8','^','s','p','X','h','d']
markers =['o','*', 'x', 'p', 's', 'd', 'p', 'h']



phis = results.parameters.sample.phi
colours = colours[:len(phis)]

coops = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).mean()
ts = coops.index
ts = ts.get_level_values(0).unique()

df = results.parameters.sample
coops2 = coops.to_frame().join(df)

phi_graph = coops2.groupby(['t', 'phi', v2]).mean() #change here
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
graphs = results.parameters.sample[v2]

fig,axs = plt.subplots(2,2, sharex = True, sharey = True)
fig.suptitle(f'Comparing Rewiring p, WS model: Replicator Dynamics ') # N: {parameters["agent_n"]}, Degree: {parameters["graph_m"]}, Repetitions: {reps}



axesx = [0,0,1,1]
axesy = [0,1,0,1]
for i in range(len(phis.unique())):
    #i=1.8
    testing =phi_graph[phi_graph.phi ==phis.unique()[i]]
    for j in range(len(graphs.unique())):
        tt = testing.groupby(['t',v2]).mean()
        ys = tt.Cooperation_Level.iloc[tt.index.get_level_values(v2)==graphs.unique()[j]]
        axs[axesx[i], axesy[i]].set_title(f' r: {phis.unique()[i]}')
        
        axs[axesx[i], axesy[i]].plot(ts,ys,marker =markers[j], markevery = 0.1,ms = 5,linewidth = 1.75, label = graphs.unique()[j])
        #axs[axesx[i], axesy[i]].legend()
        
        
handles, labels = axs[-1][-1].get_legend_handles_labels()
#fig.legend(handles, labels, loc='lower left')


for ax in axs.flat:
    ax.set(xlabel = 'Steps')
    ax.set(ylabel = 'Cooperation')
    ax.label_outer()
    ax.set_yticks(ticks = [0,0.2,0.4,0.6,0.8,1.0])
    
#fig.set_size_inches(7,5)


if save: 
    plt.savefig(f'Overleaf/images/{filename}.png')

        
        
            