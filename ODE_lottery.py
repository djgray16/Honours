# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 14:48:12 2022

@author: djgra
"""

from scipy.integrate import odeint

dt = 0.1

SS_start = 0.33

RS_start = 0.33

RWS_start = 0.33

t_start = 0 
t_end = 500

def model(proportions, t):
    SS,RS,RWS = proportions
    dSS = SS*(0.2*RS -0.04*RWS)
    dRS = RS*(0.06*RWS - 0.2*SS)
    dRWS = RWS*(0.04*SS - 0.06*RS)
    return [dSS, dRS, dRWS]

p0 = [0.33, 0.33, 0.33]

t = np.linspace(0,500)

z = odeint(model, p0, t)

plt.plot(t,z[:,0], color = 'r', label = 'SS')
plt.plot(t,z[:,1], color = 'blue', label = 'RS + SR')
plt.plot(t,z[:,2], color = 'g', label = 'R-WS')
plt.legend()