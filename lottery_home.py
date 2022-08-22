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


reps = 120

run = 1

MeansOnly = False
save = 0
filename = 'lotteryp04_me'

parameters = {
    'seed': 16,
    'steps': 1000,
              'agents': 6000,
              'alpha': 0.0,
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

pct_up = results.variables.LotteryModel.groupby(['t']).quantile(0.975)
pct_down = results.variables.LotteryModel.groupby(['t']).quantile(0.025)
#pct_up = pct_up.rename('q_up')
#pct_down = pct_up.rename('q_down')
colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',\
           'tab:pink','tab:olive', 'tab:cyan', 'tab:gray' ]
markers =['o', '*', 'x', 'p', 's', 'd', 'p', 'h']




for i in range(len(props.columns)):
    y = props[props.columns[i]]
    y1 = pct_up[props.columns[i]]
    y2 = pct_down[props.columns[i]]
    x = props.index
    plt.plot(x,y, c= colours[i], marker = markers[i], markevery = 0.05, ms = 4, linewidth = 1.5)
    if not MeansOnly:
        plt.plot(x,y1, c = colours[i], linestyle = 'dashed', marker = markers[i], markevery = 0.1,ms = 4, alpha = 0.6)
        plt.plot(x,y2,c = colours[i],linestyle = 'dashed', marker = markers[i], markevery = 0.1, ms = 4,alpha = 0.6)
#plt.legend(props.columns)
plt.xlabel('Generation')
plt.ylabel('Count of Agents')
plt.ylim(0,parameters['agents'])
plt.title(f'Imitation Dynamics, 2.5%, 97.5% Empirical Quantiles, p={parameters["lottery_p"]}')

if save: 
    plt.savefig(f'Overleaf/images/{filename}.png')
