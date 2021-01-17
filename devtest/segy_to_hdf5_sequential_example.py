# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 12:43:36 2021

@author: wesha
"""

#%%

import numpy as np
import matplotlib.pyplot as plt
import auralib as aura
import h5py

sgyfile = r'C:\Users\wesha\Dropbox\data\Blackfoot\VERTIMIG.sgy'
sg5file = r'C:\Users\wesha\Dropbox\source\repos\openseis\devtest\VERTIMIG_seq.sg5'

def_thead = {'il':{'bpos':193,  'fmt':'l', 'nbyte':4},
             'xl':{'bpos':197, 'fmt':'l', 'nbyte':4},
             'cmpx':{'bpos':185, 'fmt':'l', 'nbyte':4},
             'cmpy':{'bpos':189, 'fmt':'l', 'nbyte':4},
             'idcode':{'bpos':29, 'fmt':'h', 'nbyte':2}}

buf = aura.segy.Segy(sgyfile, def_thead)

if True:
    tdata = buf.read_tdata_multi(0, buf.num_traces, verbose=1000)
    thead = buf.read_thead_multi(0, buf.num_traces, verbose=1000)

il_min = np.min(thead['il'])
il_max = np.max(thead['il'])
xl_min = np.min(thead['xl'])
xl_max = np.max(thead['xl'])
nil = il_max - il_min + 1
nxl = xl_max - xl_min + 1

dz = buf.bhead['samp_rate']*1e-6
nz = buf.bhead['num_samp']
z_min = 0
z_max = z_min + nz*dz

# create HDF5 file and create basic file structure to hold SEGY trace
# and header data
#with h5py.File(hdf5file,'w') as fd:
fd = h5py.File(sg5file, 'w')

g0 = fd.create_group('seis')
d0 = g0.create_dataset('tdata', (buf.num_traces, nz))

g1 = g0.create_group('thead')
for key in thead.keys():
    d = g1.create_dataset(key, (buf.num_traces,))

d0[:] = tdata[:]

for key in thead.keys():
    g1[key][:] = thead[key][:]

fd.close()
