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

run = 0
save = 0
reps = 5
v2 = 'gtype'

MeansOnly = 0
CI = 1
legend = 0
filename = 'Replicator_new_low_quants'
title = 'Comparing Graph Models: Replicator Dynamics'




control_board = {'run': run, 'v2': v2, 'save': save,'title': title,
                 'filename': filename, 'reps': reps, 'MeansOnly': MeansOnly, 
                 'CI': CI, 'legend': legend}



run = control_board['run'] 
v2 = control_board['v2'] 
save = control_board['save'] 
title = control_board['title'] 
filename = control_board['filename'] 
reps = control_board['reps'] 
MeansOnly = control_board['MeansOnly']
CI = control_board['CI']
legend = control_board['legend']

parameters = {
    'seed':42,
    'steps': 1500, #number of time periods
    'agent_n': 100,
    'phi':ap.Values(4.0, 4.25, 4.5, 4.75), # #multiplier for common contributions
    'graph_m' : 6,#ap.Values(4,6,8,10,12),
    'graph_alpha': 0.3,# ap.Values(0.01,0.1,0.25,0.5, 0.75,1.0),
    'graph_p':0.1,#ap.Values(0.1,0.2,0.3,0.4,0.5),
    'power_p': 0, #ap.Values(0.1, 0.2,0.3,0.4,0.5),#ap.Values(0.01,0.2,0.4,0.6,0.8),
    'gtype': ap.Values('WS', 'TAG', 'BA', 'RRG'),
    'atype': ReplicatorLocal,
    'replicator_alpha': 1.0, #1 is pure replicator, 0 is imitation
    'plot_G': 0, #gives the summary plot of the graph for each experiment
    'step_reporting':0,
    'end_reporting':0
}

sample = ap.Sample(
    parameters,
    n=1,
    method='linspace'
)

assert len(parameters['phi'])==4

exp = ap.Experiment(WealthModel, sample, iterations=reps,
                record = True)

if run:
    results = exp.run()
    pass
colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',\
       'tab:pink','tab:olive', 'tab:cyan', 'tab:gray' ]


markers =['o','*', 'x', 'p', 's', 'd', 'p', 'h']
    
phis = results.parameters.sample.phi
colours = colours[:len(phis)]

coops = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).mean()


ts = coops.index
ts = ts.get_level_values(0).unique()

df = results.parameters.sample
coops2 = coops.to_frame().join(df)

phi_graph = coops2.groupby(['t', 'phi', v2]).mean()
if not MeansOnly:
    q_up = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).quantile(0.75)
    q_down = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).quantile(0.25)
    if CI:
        q_up = coops + 1.96/math.sqrt(reps)*results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).std()
        q_down = coops - 1.96/math.sqrt(reps)*results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).std()
        
    q_up = q_up.to_frame().join(df)
    q_down = q_down.to_frame().join(df)
    q_up = q_up.groupby(['t', 'phi', v2]).mean()
    q_down = q_down.groupby(['t', 'phi', v2]).mean()
    q_up = q_up.reset_index()
    q_down = q_down.reset_index()
    
phi_graph = phi_graph.reset_index()
graphs = results.parameters.sample[v2]

fig,axs = plt.subplots(2,2, sharex = True, sharey = True)
fig.suptitle(f'{title}')
    
axesx = [0,0,1,1]
axesy = [0,1,0,1]
for i in range(len(phis.unique())):
    
    testing =phi_graph[phi_graph.phi ==phis.unique()[i]]
    
    if not MeansOnly:
        quant_up = q_up[q_up.phi==phis.unique()[i]]
        
        quant_down =  q_down[q_down.phi==phis.unique()[i]]
        if CI:
            pass
            #quant_up = tt+1.96/math.sqrt(reps)*testing.groupby(['t',v2]).std()
            #quant_down = tt-1.96/math.sqrt(reps)*testing.groupby(['t',v2]).std()
            
    for j in range(len(graphs.unique())):
        tt = testing.groupby(['t',v2]).mean()
        
        
        ys = tt.Cooperation_Level.iloc[tt.index.get_level_values(v2)==graphs.unique()[j]]
        axs[axesx[i], axesy[i]].set_title(f' r: {phis.unique()[i]}')
        axs[axesx[i], axesy[i]].set_ylim(0,1)
        #axs[axesx[i], axesy[i]].plot(ts,ys,marker =markers[j], markevery = 0.1,ms = 5,linewidth = 1.75, c= colours[j], label = graphs.unique()[j])
        if not MeansOnly:
            qq_up = quant_up.groupby(['t',v2]).mean()
            qq_down = quant_down.groupby(['t',v2]).mean()
            y2s = qq_up.Cooperation_Level.iloc[tt.index.get_level_values(v2)==graphs.unique()[j]]
            print(y2s-ys)
            
            y3s = qq_down.Cooperation_Level.iloc[tt.index.get_level_values(v2)==graphs.unique()[j]]
            #print(y3s-ys)
            axs[axesx[i], axesy[i]].plot(ts,y2s,linestyle = 'dashed', c = colours[j], alpha = 0.6,linewidth = 1.75, label = 'quant_up')
            axs[axesx[i], axesy[i]].plot(ts,y3s,linestyle = 'dashed', c = colours[j], alpha = 0.6,linewidth = 1.75)
            
        
            
        
        
handles, labels = axs[-1][-1].get_legend_handles_labels()
if legend:
    fig.legend(handles, labels, loc='lower left')


for ax in axs.flat:
    ax.set(xlabel = 'Steps')
    ax.set(ylabel = 'Cooperation')
    ax.label_outer()
    ax.set_yticks(ticks = [0,0.2,0.4,0.6,0.8,1.0])
    
#fig.set_size_inches(7,5)


if save: 
    plt.savefig(f'Overleaf/images/{filename}.pdf')
    print(f'saved fig: {title} as {filename}')
    #plt.close(fig)

  