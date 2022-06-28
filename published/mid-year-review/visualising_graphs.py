# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:19:57 2022

@author: djgra
"""

from TAG import *

#AA = TAG(20,5,0.2)
n = 50
AA = nx.barabasi_albert_graph(n = n, m = 2)
#AA = nx.gnp_random_graph(n = n, p = 0.1)
p= 0
AA = nx.connected_watts_strogatz_graph(n = n, k = 4, p = p, tries = 100)


#nx.draw(AA)

#A = nx.barabasi_albert_graph(N = 20)






plt.figure()
plt.title(f"Watts-Strogatz, N ={n}, Mean Degree = {b}, Rewiring P = {p} ")
pos = nx.circular_layout(AA)
nx.draw(AA, pos = pos, node_size = 20, width  = 0.5)
#nx.draw_circular(AA)
#nx.draw_spring(AA)

#plot_G(AA)

b = np.mean([a[1] for a in list(nx.degree(AA))])

print(b)