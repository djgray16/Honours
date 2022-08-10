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

parameters = {'steps': 500,
              'agents': 6000,
              'alpha': 0.0,
              'lottery_p': 0.4,
              'atype': Nau}


sample = ap.Sample(
    parameters,
    n=4,
    method='linspace'
)


exp = ap.Experiment(LotteryModel, sample, iterations=20,
                    record = True)
results = exp.run()

props = results.variables.LotteryModel.groupby(['t']).mean()

for i in props.columns:
    y = props[str(i)]
    x = props.index
    plt.plot(x,y)
    
plt.legend(props.columns)
plt.xlabel('Generation')
plt.ylabel('Count of Agents')
plt.ylim(0,parameters['agents'])
plt.title(f'Lottery Game with update alpha {parameters["alpha"]} and lottery win prob {parameters["lottery_p"]}')