# begin boiler plate for compatibility
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import sys
if sys.version_info.major > 2:
    xrange = range
elif sys.version_info.major == 2:
    pass
# end boiler plate for compatibility

import lab_manager as lm # have to combine two lab_manager later

import scipy as sp
import numpy as np
from jitcode import jitcode, y, t
try:
    import symengine as sym_backend
except:
    import sympy as sym_backend
import networkx as nx
import random
import networks as net
import neuron_models as nm
import experiments as ex
from itertools import chain

#First number is #LNs, second is #PNs
neuron_nums = [2, 6]
#Create_AL creates AL with random connections with prob 0.5
AL = net.create_AL(nm.LN, nm.PN_2, nm.Synapse_gaba_LN, nm.Synapse_nAch_PN_2, neuron_nums)

#Set up the experiment
num_layers = 2

# Roughly the max current each neuron is injected with. This block of code makes it
# so that random neurons are injected with current, and the levels are slighlty different
Iscale = 300
I_ext = []
for i in range(num_layers):
    I_ext.append(np.random.rand(neuron_nums[i]))
    I_ext[i][(np.nonzero(I_ext[i] >= 0.67))] = 1.0
    I_ext[i] = np.floor(I_ext[i])
    I_ext[i][np.nonzero(I_ext[i])] = Iscale*np.asarray(I_ext[i][np.nonzero(I_ext[i])] + 0.02*np.random.randn(np.count_nonzero(I_ext[i]),))
neuron_inds = [np.nonzero(I_ext[j])[0].tolist() for j in range(num_layers)]
current_vals = [I_ext[j][np.nonzero(I_ext[j])] for j in range(num_layers)]


ex.const_current(AL, num_layers, neuron_inds, current_vals)
#ex.feed_gaussian_rate_poisson_spikes(AL,0.1,i_max=1000,num_sniffs=50)
#set up the lab
f, initial_conditions, neuron_inds  = lm.set_up_lab(AL)

#run for specified time with dt
time_len = 1000.0
dt = 0.02
time_sampled_range = np.arange(0., time_len, dt)

data = lm.run_lab(f, initial_conditions, time_sampled_range, integrator = 'dopri5')

#lm.show_all_neuron_in_layer(time_sampled_range, data, AL, 0)
lm.plot_LFP(time_sampled_range, data, AL, layer_pn = 1)
