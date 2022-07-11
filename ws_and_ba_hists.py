# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 17:43:26 2022

@author: djgra
"""

''' make graph here'''
import numpy as np
import pandas as pd

from TAG import *

n = 1000

degree = 6


p = 0.05



G = nx.barabasi_albert_graph(n, m = int(degree/2))

GG = nx.watts_strogatz_graph(n,k = int(degree), p=p)





def plot_hist(G):
    
    degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
    dmax = max(degree_sequence)
    
    
    
    
    
    
    
    ax = plt.bar(*np.unique(degree_sequence, return_counts=True))
    plt.title(f"Degree Histogram; Watts-Strogatz, N ={n}, Mean Degree = {degree}, p = {p}")
    plt.xlabel("Degree")
    plt.ylabel("# of Nodes")
    return

#plot_hist(GG)




tdict = {}
T = 10

for i in range(T):
    end = 0.2
    p = 0+end*i/(T)
    GG = nx.watts_strogatz_graph(n,k = int(degree), p=p)
    aspl = nx.average_shortest_path_length(GG)
    clus  =np.mean( [nx.clustering(GG)[i] for i in range(len(GG.degree))])
    tdict[i] = (p,aspl,clus)

#nx.average_shortest_path_length(G)


#a = [GG.degree[i] for i in range(len(G.degree))]

#print(np.mean(a))

#aa = [nx.clustering(GG)[i] for i in range(len(GG.degree))]


#print(np.mean(aa))

df = pd.DataFrame.from_dict(tdict)

df = df.T

'''todo

plot df as the two lines, and also put on the constant BA network

import into new slides second random model
finish summary slide
add references slide


reference slide done
'''


