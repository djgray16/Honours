# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 17:43:26 2022

@author: djgra
"""

''' make graph here'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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


'''

tdict = {}
T = 40

for i in range(T):
    end = 0.15
    p = 0+end*i/(T)
    GG = nx.watts_strogatz_graph(n,k = int(degree), p=p)
    aspl = nx.average_shortest_path_length(GG)
    clus  =np.mean( [nx.clustering(GG)[i] for i in range(len(GG.degree))])
    tdict[i] = (p,aspl,clus)
    print('donealap')


ba_aspl = nx.average_shortest_path_length(G)


a = [GG.degree[i] for i in range(len(G.degree))]
#print(np.mean(a))

ba_clus = np.mean([nx.clustering(GG)[i] for i in range(len(GG.degree))])


#print(np.mean(aa))

df = pd.DataFrame.from_dict(tdict)

df = df.T

df.columns = ['p', 'aspl', 'clus']
df = df.set_index('p')
'''



'''todo

plot df as the two lines, and also put on the constant BA network

import into new slides second random model
finish summary slide
add references slide


reference slide done
'''


#define colors to use
col1 = 'steelblue'
col2 = 'red'



#define subplots
fig,ax = plt.subplots()

plt.suptitle('Key Characteristics of Watts-Strogatz, Barabasi-Albert Graphs, N = 1000')


#add first line to plot
ax.plot(df.index, df.aspl, color=col1, label = 'WS_ASPL')

#add x-axis label
ax.set_xlabel('Rewiring Probability p', fontsize=14)

#add y-axis label
ax.set_ylabel('Average Shortest Path Length', color=col1, fontsize=16)
ax.set_ylim(bottom = 0, top = 90)
#define second y-axis that shares x-axis with current plot
ax2 = ax.twinx()
ax2.set_ylim(bottom = 0.30, top = 0.65)

#add second line to plot
ax2.plot(df.index, df.clus, color=col2, label = 'WS_clus')

#add second y-axis label
ax2.set_ylabel('Clustering Coefficient', color=col2, fontsize=16)



ax.hlines(y=ba_aspl, xmin=0, xmax=end, colors='aqua', linestyles='-', lw=2, label='BA_ASPL')
#plt.hlines(y=[39, 40, 41], xmin=[0, 25, 50], xmax=[len(xs)], colors='purple', linestyles='--', lw=2, label='Multiple Lines')
ax2.hlines(y=ba_clus, xmin=0, xmax=end, colors='maroon', linestyles='--', lw=2, label='BA_clus')



handles, labels = [(a + b) for a, b in zip(ax.get_legend_handles_labels(), ax2.get_legend_handles_labels())]
fig.legend(handles, labels, bbox_to_anchor = (0.75,0.75), loc="right", borderaxespad=0)
#fig.legend(handles, labels, loc='upper center')
