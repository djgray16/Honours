# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 09:38:04 2022

@author: djgra
"""

import agentpy as ap
import numpy as np
import random as random
import networkx as nx

from TAG import *
from Agents import *
from Models import *

import matplotlib.pyplot as plt


reps = 20

run = 1


save = 0
filename = 'lotteryp04_me'

parameters = {
    'seed': 482,
    'steps': 500,
              'agents': 6000,
              'alpha': 1.0,
              'lottery_p': 0.4,
              'atype': Nau}


sample = ap.Sample(
    parameters,
    n=1,
    method='linspace'
)


exp = ap.Experiment(LotteryModel, sample, iterations=reps,
                    record = True)
if run:
    results = exp.run()

props = results.variables.LotteryModel.groupby(['t']).mean()

colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',\
           'tab:pink','tab:olive', 'tab:cyan', 'tab:gray' ]
markers =['o', '*', 'x', 'p', 's', 'd', 'p', 'h']

for i in range(len(props.columns)):
    y = props[props.columns[i]]
    x = props.index
    plt.plot(x,y, c= colours[i], marker = markers[i], markevery = 0.05, ms = 4, linewidth = 1.5)
    
#plt.legend(props.columns)
plt.xlabel('Generation')
plt.ylabel('Count of Agents')
plt.ylim(0,parameters['agents'])
plt.title(f'Replicator Dynamics, p=0.4')

if save: 
    plt.savefig(f'Overleaf/images/{filename}.png')
