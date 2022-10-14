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

## Control board

run = 1
CI = True #true is when assume normal distribution, false is empirical quantiles

MeansOnly = True

save = 0 #save the figure

filename = 'TAfig4b'

parameters = {
    'seed': 42,
    'steps': 100, #number of time periods
    'agent_n': 100,
    'phi':5.5, #multiplier for common contributions
    'graph_m' : 6,
    'graph_alpha': 1.0,
    'graph_p':0.1,
    'gtype': 'BA',
    'atype': 'ReplicatorLocal',
    'replicator_alpha': 1.0, #1 is pure replicator, 0 is imitation
    'plot_G': 0, #gives the summary plot of the graph for each experiment
    'step_reporting': 0,
    'end_reporting': 0
}


sample = ap.Sample(
    parameters,
    n=1,
    method='linspace'
)

reps = 50
exp = ap.Experiment(WealthModel, sample, iterations=reps,
                    record = True)

if run:

    results = exp.run()




### PLotting 



'''


phis = results.parameters.sample.phi

colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',\
           'tab:pink','tab:olive', 'tab:cyan', 'tab:gray' ]
    
markers = ['2', '3','1','8','^','s','p','X','h','d']
markers =['o', '*', 'x', 'p', 's', 'd', 'p', 'h']
colours = colours[:len(phis)]


coops = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).mean()

pct_up = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).quantile(0.975)
if CI:
    pct_up = coops + 1/math.sqrt(reps)*1.96*results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).std()
pct_up = pct_up.rename('q_up')
pct_down = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).quantile(0.025)
if CI:
    pct_down = coops - 1/math.sqrt(reps)*1.96*results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).std()

pct_down = pct_down.rename('q_down')

ts = coops.index
ts = ts.get_level_values(0).unique()

df = results.parameters.sample
coops2 = coops.to_frame().join(df).join(pct_up).join(pct_down)

phi_graph = coops2.groupby(['t', 'phi']).mean()

#m_graph = coops2.groupby(['t', 'graph_m']).mean()
#plt.figure(figsize = (8,8))
fig, ax = plt.subplots()
for i in range(len(phis)):
    y1 = phi_graph.Cooperation_Level.iloc[phi_graph.index.get_level_values('phi') == phis[i]]
    y2 = phi_graph.q_down.iloc[phi_graph.index.get_level_values('phi') == phis[i]]
    y3 = phi_graph.q_up.iloc[phi_graph.index.get_level_values('phi') == phis[i]]
    x = phis.index
    #plt.legend(phis.unique())
    ax.plot(ts,y1, c=colours[i],marker = markers[i], markevery = 1,ms = 4,linewidth = 1.0, label = f'r = {phis[i]}') #
    if not MeansOnly:
        ax.plot(ts,y2,  c=colours[i], linestyle = 'dashed', label = f'_5th Percentile of {phis[i]}', alpha = 0.6 )
        ax.plot(ts,y3,  c=colours[i], linestyle =  'dashed', label = f'_95th Percentile of {phis[i]}' , alpha = 0.6)
    

ax.legend( loc='lower right')
ax.set_ylabel('Mean Cooperation')
ax.set_xlabel('Round')
ax.set_yticks(ticks = [0,0.2,0.4,0.6,0.8,1.0])

#plt.rcParams["figure.figsize"] = (10,10)

fig.suptitle(f"WS Time to stability") #"; N: {parameters['agent_n']} "\
          #f"k: {parameters['graph_m']}, T: {reps}, alpha: {parameters['graph_alpha']} ")
    
  
'''



trends = results.variables.WealthModel

tfinal = parameters['steps']

final_vals = trends.iloc[trends.index.get_level_values('t') == tfinal]

plt.hist(final_vals, bins = 20)

if save: 
    plt.savefig(f'Overleaf/images/{filename}.pdf')

            