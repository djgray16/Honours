# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 09:37:45 2022

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

save = 1 #save the figure
run =1

trim = 1


filename = 'Rep_BA_node_groups_m_8_phi_6'


phis = [4,6,8]

ms = [4,6,8]
with open (f'{filename}.pickle', 'rb') as handle:
     pickle_in = pickle.load( handle)

counts = pickle_in['counts']
end_coop = pickle_in['end_coop']
agg_coop = pickle_in['agg_coop']
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

#fname = 'Rep_BA_node_groups_m_' + str(m) + '_phi_' + str(phi)
if save: 
    plt.savefig(f'Overleaf/images/{filename}.pdf')
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

fname = filename+'_trimmed'
if save: 
    plt.savefig(f'Overleaf/images/{fname}.pdf')
    print('saved')