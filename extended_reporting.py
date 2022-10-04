# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 09:32:47 2022

@author: djgra
"""

import pickle as pickle
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
run =1

trim = 1


#filename = 'BA_degree_groups_45_1000_trimmed_6'


phis = [4,6,8]

ms = [4,6,8]





for phi in phis:
    for m in ms:
        

        parameters = {
            'seed':52,
            'steps': 2000, #number of time periods
            'agent_n': 100,
            'phi':phi, #change here    #ap.Values(2.0,2.5,3.0,3.5), # #multiplier for common contributions
            'graph_m' : m, #change here
            'graph_alpha': 0,# ap.Values(0.01,0.1,0.25,0.5, 0.75,1.0),
            'graph_p':0,#ap.Values(0.1,0.2,0.3,0.4,0.5),
            'power_p': 0,#ap.Values(0.1, 0.2,0.3,0.4,0.5),#ap.Values(0.01,0.2,0.4,0.6,0.8),
            'gtype': 'BA', #ap.Values('WS', 'TAG', 'BA', 'RRG'),
            'atype': 'ReplicatorLocal',
            'replicator_alpha': 0.0, #1 is pure replicator, 0 is imitation
            'plot_G': 0, #gives the summary plot of the graph for each experiment
            'step_reporting': 0,
            'end_reporting': 1
        }
    
    
        sample = ap.Sample(
            parameters,
            n=1,
            method='linspace'
        )
        #assert len(parameters['phi'])==4
        
        reps = 1000
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
        
        if save:
            fname = 'ID_BA_node_groups_m_' + str(m) + '_phi_' + str(phi)
            pickle_in ={'counts': counts, 'end_coop': end_coop, 'agg_coop': agg_coop}
            with open (f'{fname}.pickle', 'wb') as handle:
                pickle.dump(pickle_in, handle)
                print('pickled')
        
        ### checking can read back
        '''
        
        agg_coop_end = agg_coop.values[parameters['steps']]
        log_counts = np.log(counts)
        fig, bar_ax = plt.subplots()
        bar_ax.hist(counts.index, weights = counts, log = 1, density = 0, alpha = 0.6, bins  =len(counts.index) )# list(counts.index)+[max(counts.index)+1])
        bar_ax.set_xlabel('Degree Size')
        bar_ax.set_ylabel('Count of Nodes')
        line_ax = bar_ax.twinx()
        line_ax.plot(end_coop.index,end_coop, marker = 'o', color = 'black')
        line_ax.set_ylim([0,1])
        line_ax.hlines(agg_coop_end,end_coop.index.min(), end_coop.index.max(), color = 'r', linewidth = 3, linestyle = 'dashed')
        line_ax.set_ylabel('Final Cooperation')
        
        fig.suptitle('Final Cooperation vs Node Degree: BA Model')
        
        fname = 'Rep_BA_node_groups_m_' + str(m) + '_phi_' + str(phi)
        if save: 
            plt.savefig(f'Overleaf/images/{fname}.pdf')
            print('saved')
        
        ### trimming
        
        if trim:
            new_counts = counts[counts>5]
            end_coop = end_coop[counts>5]
            counts = new_counts
        fig, bar_ax = plt.subplots()
        
        bar_ax.hist(counts.index, weights = counts, log = 1, density = 0, alpha = 0.6, bins  = len(counts.index))#+[max(counts.index)+1])
        bar_ax.set_xlabel('Degree Size')
        bar_ax.set_ylabel('Count of Nodes')
        line_ax = bar_ax.twinx()
        line_ax.plot(end_coop.index,end_coop, marker = 'o', color = 'black')
        line_ax.set_ylim([0,1])
        line_ax.hlines(agg_coop_end,end_coop.index.min(), end_coop.index.max(), color = 'r', linewidth = 3, linestyle = 'dashed')
        line_ax.set_ylabel('Final Cooperation')
        
        fig.suptitle('Final Cooperation vs Node Degree: BA Model, Trimmed')
        
        
        #
        
        fname = 'Rep_BA_node_groups_m_' + str(m) + '_phi_' + str(phi)+'_trimmed'
        if save: 
            plt.savefig(f'Overleaf/images/{fname}.pdf')
            print('saved')
        '''
#plt.show()

