# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 15:51:56 2022

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

# Visualization
#import seaborn as sns

import matplotlib.pyplot as plt

import pickle as pickle

### need mean, std, quantiles, plus phi_graph

fname = 'Replicator_new_low_long_home'


''' 
to do 











'''

#results = [i for i in range(1000)]
with open (f'{fname}.pickle', 'rb') as handle:
     results = pickle.load( handle)
     
psample =  results.parameters.sample #need this as a key



def q_low(data):
    return data.quantile(q=0.025)
def q_high(data):
    return data.quantile(q=0.975)


summary = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).agg([np.mean, np.std, lambda x: x.quantile(0.025), lambda x:x.quantile(0.975)])

summary.rename(columns = {'mean': 'avg', 'std': 'dev','<lambda_0>': 'q_low', '<lambda_1>': 'q_high'}, inplace = True)

pickle_save = {'psample': psample, 'summary': summary}


#fname = 'summary_demo'
with open (f'{fname}.pickle', 'wb') as handle:
    pickle.dump(pickle_save, handle)

