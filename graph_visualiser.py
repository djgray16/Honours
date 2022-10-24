# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 16:23:29 2022

@author: djgra
"""

import agentpy as ap
import numpy as np
import random as random
import networkx as nx
from Agents import *
from TAG import *

gtype = 'RRG'
n = 16
m = 4
graph_p = 0.1
graph_alpha = 0.3

graphs = [1,1,1,1]
graph_labels = ['Watts-Strogatz (WS)', 'Random Regular Graph (RRG)','Barabasi-Albert (BA)',  'Tomassini-Antonioni Graph (TAG)']

#graph = nx.connected_watts_strogatz_graph(n,m,graph_p)

graphs[0] = nx.connected_watts_strogatz_graph(n,m,graph_p)

graphs[2] =  graph=nx.barabasi_albert_graph(n, int(m/2))


graphs[1] = nx.random_regular_graph(m, n)
    


graphs[3]= TAG(n,m,graph_alpha)


fig, axs = plt.subplots(2,2)

for i in range(len(axs.flat)):
    axs.flat[i].set_title(graph_labels[i])
    nx.draw_circular(graphs[i], ax = axs.flat[i], node_size = 60)
fig.suptitle(f'Demonstration of Graph Models, N = {n}, m = {m}')
filename = 'GraphModels16_4'
plt.savefig(f'Overleaf/images/{filename}.pdf')

