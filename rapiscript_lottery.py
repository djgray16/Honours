# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 15:05:42 2022

@author: djgra
"""

import agentpy as ap
import numpy as np
import random as random
import networkx as nx

from TAG import *
from Agents import *
from Models import *
from experiment_functions import *
import math

# Visualization
#import seaborn as sns

import matplotlib.pyplot as plt

reps = 100

run = 1
legend = 0
MeansOnly = 1

CI = 0
save = 1
filename = 'lottery1_me'
title = 'Replication of Lottery Game: Replicator Dynamics'
control_board = {'run': run, 'reps': reps, 'save': save, 'filename': filename,
                 'CI': CI, 'MeansOnly': MeansOnly, 'title': title, 
                 'legend': legend}



parameters = {
    'seed': 42,
    'steps': 500,
              'agents': 6000,
              'alpha': 1.0,
              'lottery_p': 0.5,
              'atype': Nau}

#lottery(parameters, control_board)


####################################################

control_board['title'] = 'Replication of Lottery Game: Imitation Dynamics'
control_board['filename'] = 'lottery2_me'

parameters['alpha'] = 0.0

#lottery(parameters, control_board)


#######################################################

control_board['title'] = 'Replication of Lottery Game: alpha = 0.5 Dynamics'
control_board['filename'] = 'lottery3_me'

parameters['alpha'] = 0.5

lottery(parameters, control_board)


##############################################################################

control_board['title'] = 'Imitation Dynamics; p=0.4'
control_board['filename'] = 'lotteryp4_me'

parameters['alpha'] = 0.0

parameters['lottery_p'] = 0.4


lottery(parameters, control_board)


##############################################################################

control_board['title'] = 'Imitation Dynamics; p=0.55'
control_board['filename'] = 'lotteryp055_me'

parameters['alpha'] = 0.0

parameters['lottery_p'] = 0.55
parameters['steps'] = 200


lottery(parameters, control_board)




##############################################################################


control_board['filename'] = 'lotteryp4_me_quantiles_empirical'

control_board['title'] = 'Imitation Dynamics: Empirical 2.5%, 97.5% Quantiles, p=0.4'

parameters['alpha'] = 0.0

parameters['lottery_p'] = 0.4

control_board['MeansOnly'] = 0

control_board['CI'] = 0
parameters['steps'] = 500
lottery(parameters, control_board) 



##############################################################################


control_board['filename'] = 'lotteryp4_me_quantiles'

control_board['title'] = 'Imitation Dynamics, Mean 95% Confidence Interval, p=0.4'

parameters['alpha'] = 0.0

parameters['lottery_p'] = 0.4

control_board['MeansOnly'] = 0

control_board['CI'] = 1

lottery(parameters, control_board)  