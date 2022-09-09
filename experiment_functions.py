# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 12:43:43 2022

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

# Visualization
#import seaborn as sns

import matplotlib.pyplot as plt



def experiment(parameters, control_board):
    

    ''' needs parameters for the experiment, control board for everything else
    '''
    
    
    run = control_board['run'] 
    v2 = control_board['v2'] 
    save = control_board['save'] 
    title = control_board['title'] 
    filename = control_board['filename'] 
    reps = control_board['reps']
    CI = control_board['CI']
    MeansOnly = control_board['MeansOnly']
        
    sample = ap.Sample(
        parameters,
        n=1,
        method='linspace'
        )
    
    exp = ap.Experiment(WealthModel, sample, iterations=reps,
                    record = True)

    if run:
        results = exp.run()
        
        
    ### PLotting 
    
    
    phis = results.parameters.sample.phi
    
    colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',\
               'tab:pink','tab:olive', 'tab:cyan', 'tab:gray' ]
        
    
    markers =['o', '*', 'x', 'p', 's', 'd', 'p', 'h']
    #colours = colours[:len(phis)]
    
    
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
    
    fig.suptitle(f"{title}") #"; N: {parameters['agent_n']} "\
              #f"k: {parameters['graph_m']}, T: {reps}, alpha: {parameters['graph_alpha']} ")
        
    '''   
    plt.title(f' {parameters["agent_n"]} agents,' \
    f'graph: {parameters["gtype"]}, agents: {parameters["atype"]}, graph_alpha: ' \
        f'{parameters["graph_alpha"]}, m: {parameters["graph_m"]}: replicator_alpha:'\
            f' {parameters["replicator_alpha"]}, CI: {CI}'
              )No 
        
    '''   
    
    
    if save: 
        plt.savefig(f'Overleaf/images/{filename}.pdf')
        print(f'saved fig: {title} as {filename}')
    return 

def compare_two(parameters, control_board):
    '''to make the 4 subplots graph. needs parameters as usual
    then a control board consisting of 
    run, v2, save,title, filename, reps = control_board
    '''


    run = control_board['run'] 
    v2 = control_board['v2'] 
    save = control_board['save'] 
    title = control_board['title'] 
    filename = control_board['filename'] 
    reps = control_board['reps'] 
    
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
        
    phi_graph = phi_graph.reset_index()
    graphs = results.parameters.sample[v2]
    
    fig,axs = plt.subplots(2,2, sharex = True, sharey = True)
    fig.suptitle(f'{title}')
        
    axesx = [0,0,1,1]
    axesy = [0,1,0,1]
    for i in range(len(phis.unique())):
        
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
        plt.savefig(f'Overleaf/images/{filename}.pdf')
        print(f'saved fig: {title} as {filename}')
    return
    
    

