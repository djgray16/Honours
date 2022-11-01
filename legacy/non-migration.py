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
random.seed(2)

parameters = {
    'satisfaction_agents': 0,
    'steps': 40, #number of time periods
    #'seed': 41, #random seed
    'follower_agents': 0, 
    'momentum_agents': 0,
    'selfish_agents': 0,
    'AT': 150,
    'phi':ap.Values(1.2,1.8,2.0,2.2,2.4,2.6,3.0,4.0), #multiplier for common contributions
    #'pi': 2.8, #minimum acceptable contribution for satisfaction agents
    #'rho': 0.5, #minimum proportion of contributing agents for follower agents
    'graph_m' : 6,
    'graph_alpha': 0.3
    #'per_game_switch': 1 #applies if we want to normalise profit per game
}


sample = ap.Sample(
    parameters,
    n=4,
    method='linspace'
)


exp = ap.Experiment(WealthModel, sample, iterations=30, record = True)
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
plt.title('Effect of Changing phi- 50 agents,graph: connected WS, p = 0.5 ')
    

            