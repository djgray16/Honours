# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 20:43:50 2022

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
import pickle as pickle
## Control board

run = 1
CI = True #true is when assume normal distribution, false is empirical quantiles

MeansOnly = True

save = 1 #save the figure

gtype = 'RRG'

fname = f'final_val_hists_Rep_{gtype}_55'

phiz = str(5.5)
phi = 5.5
phin = str(phi).replace('.', '')

with open (f'pickles/{fname}.pickle', 'rb') as handle:
           final_vals = pickle.load( handle)
fig, ax = plt.subplots()
ax.hist(final_vals, density = 0,bins = 25, range = [0,1])
phiz = str(phi)
fig.suptitle(f'Final Contribution Level, {gtype} Model, r = {phiz}, Replicator Dynamics')
ax.set_xlabel('Final Contribution')
ax.set_ylabel('Count')
fname = f'Rep_coop_histo_{gtype}_{phin}'
if save: 
    plt.savefig(f'Overleaf/images/{fname}.pdf')
    print(f'saved {fname}')