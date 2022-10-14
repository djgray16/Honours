# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 12:08:37 2022

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
import math
from experiment_functions import *
import seaborn as sb

# Visualization
#import seaborn as sns

import matplotlib.pyplot as plt

import pickle as pickle

size = 'high'

fname = 'Replicator_new_'+size+'_long' +'_home'

with open (f'{fname}.pickle', 'rb') as handle:
     pickle_in = pickle.load( handle)
     
     
summary = pickle_in['summary']

psample = pickle_in['psample']    

tfinal = 10_000

'''
for i in psample.index:
    print(psample.loc[i].phi, psample.loc[i].gtype, round(summary.loc[(tfinal, i)].dev, 3))
    
'''

ID_dev = pd.read_excel('ID_dev.xlsx')
Rep_dev = pd.read_excel('Rep_dev.xlsx')

#Rep_dev = Rep_dev.rename({'Unnamed: 0': 'phi'})

ID_dev = ID_dev.set_index('phi')
Rep_dev = Rep_dev.set_index('phi')


fig, ax = plt.subplots()

sb.heatmap(Rep_dev, cmap = 'coolwarm', vmin = 0, vmax = 0.502, annot = True, yticklabels=3)

#im = ax.imshow(ID_dev, cmap = 'coolwarm', vmin = 0, vmax = 0.502)

ax.set_xticklabels(ID_dev.columns)

#ax.set_title('Imitation Dynamics, Sample Standard Deviation at Final Generation')
#ax.xaxis.set_xticks(ID_dev.columns)
#ax.set_yticklabels(ID_dev.index)
ax.set_xlabel('Graph Type')
ax.set_ylabel('r')
#ax.set_ytickslabels( labels=ID_dev.index)
save = 1
if save:
    plt.savefig('Overleaf/images/Rep_dev_heatmap.pdf')