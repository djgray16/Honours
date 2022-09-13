# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 14:48:12 2022

@author: djgra
"""
import numpy as np
from scipy.integrate import odeint

import matplotlib.pyplot as plt

dt = 0.1

SS_start = 0.33

RS_start = 0.33

RWS_start = 0.33

t_start = 0 
t_end = 500

strats = ['SS', 'RR', 'RS', 'SR', 'RWS', 'RWR']

def model(proportions, t):
    SS,RR,RS,SR,RWS,RWR = proportions
    dSS = SS*(0.2*RR + 0.2*SR + 0.2*RS -0.04*RWS +0.44*RWR)
    dRR = RR*(-0.2*SS + -0.104*RS -0.104*SR -0.0896*RWS -0.0144*RWR)
    dRS = RS*(-0.2*SS + 0.104*RR+0*SR +  0.072*RWS + 0.032*RWR)
    dSR = SR*(-0.2*SS + 0.104*RR + 0*RS + 0.072*RWS + 0.032*RWR)
    dRWS = RWS*(0.04*SS+ 0.0896*RR  - 0.072*RS - 0.072*SR +0.032*RWR)
    dRWR = RWR*(-0.44*SS + 0.0144*RR - 0.032*SR -0.032*RS -0.032*RWS)
    return [dSS,dRR, dRS, dSR, dRWS, dRWR]

p0 = [1/6]*6

t = np.linspace(0,500)

z = odeint(model, p0, t)
markers =['o', '*', 'x', 'p', 's', 'd', 'p', 'h']
colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',\
               'tab:pink','tab:olive', 'tab:cyan', 'tab:gray' ]

fig, ax = plt.subplots()
for i in range(6):
    ax.plot(t,z[:,i], color = colours[i], marker = markers[i], markevery = 0.1,label = strats[i])



#plt.legend()

fig.suptitle('Deterministic Simulation of Lottery Game')
ax.set_xlabel('Steps')

ax.set_ylabel('Proportion')

filename = 'ODE_lottery'
plt.savefig(f'Overleaf/images/{filename}.pdf')
