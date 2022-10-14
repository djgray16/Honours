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

save = 1 #save the figure

filename = 'TAfig4b'

phis = [5.0, 5.25, 5.5, 5.75]

gtypes = ['BA', 'WS', 'TAG', 'RRG']

for phi in phis:
    for gtype in gtypes:
        
        parameters = {
            'seed': 42,
            'steps': 5000, #number of time periods
            'agent_n': 100,
            'phi':phi, #multiplier for common contributions
            'graph_m' : 6,
            'graph_alpha': 0.3,
            'graph_p':0.1,
            'gtype': gtype,
            'atype': 'ReplicatorLocal',
            'replicator_alpha': 0.0, #1 is pure replicator, 0 is imitation
            'plot_G': 0, #gives the summary plot of the graph for each experiment
            'step_reporting': 0,
            'end_reporting': 0
        }
        
        
        sample = ap.Sample(
            parameters,
            n=1,
            method='linspace'
        )
        
        reps = 100
        exp = ap.Experiment(WealthModel, sample, iterations=reps,
                            record = True)
        
        if run:
        
            results = exp.run()
        
        
        
        
        ### PLotting 
        
        
        
        
        
        trends = results.variables.WealthModel
        
        tfinal = parameters['steps']
        
        final_vals = trends.iloc[trends.index.get_level_values('t') == tfinal]
        fig, ax = plt.subplots()
        ax.hist(final_vals, bins = 25)
        phiz = str(phi)
        fig.suptitle(f'Final Cooperation level, {gtype} Model, r = {phiz}, Imitation Dynamics')
        phin = str(phi).replace('.', '')
        fname = f'ID_coop_histo_{gtype}_{phin}'
        if save: 
            plt.savefig(f'Overleaf/images/{fname}.pdf')

            