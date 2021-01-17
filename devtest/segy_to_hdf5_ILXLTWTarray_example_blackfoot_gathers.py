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
sg5file = r'C:\Users\wesha\Dropbox\source\repos\openseis\devtest\VERTIMIG_gath.sg5'

def_thead = {'il':{'bpos':193,  'fmt':'l', 'nbyte':4},
             'xl':{'bpos':197, 'fmt':'l', 'nbyte':4},
             'cmpx':{'bpos':185, 'fmt':'l', 'nbyte':4},
             'cmpy':{'bpos':189, 'fmt':'l', 'nbyte':4},
             'offset':{'bpos':37, 'fmt':'l', 'nbyte':4},
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

fd.attrs.create('data_type', 'trace')
fd.attrs.create('data_units', 'amp')
fd.attrs.create('il_min', il_min)
fd.attrs.create('il_max', il_max)
fd.attrs.create('xl_min', xl_min)
fd.attrs.create('xl_max', xl_max)
fd.attrs.create('nil', nil)
fd.attrs.create('nxl', nxl)
fd.attrs.create('dz', dz)
fd.attrs.create('nz', nz)
fd.attrs.create('z_min', z_min)
fd.attrs.create('z_max', z_max)
fd.attrs.create('z_type', 'TWT')

g0 = fd.create_group('seis')
d0 = g0.create_dataset('tdata', (nil, nxl, nz))

g1 = g0.create_group('thead')
for key in thead.keys():
    d = g1.create_dataset(key, (nil, nxl))

for i in range(buf.num_traces):
    if i%nxl == 0:
        print('Writing trace inline %i' % (thead['il'][i]))

    ili = thead['il'][i] - il_min
    xli = thead['xl'][i] - xl_min
    d0[ili, xli] = tdata[i]

for key in thead.keys():
    for i in range(buf.num_traces):
        if i%nxl == 0:
            print('Writing header key=%s for inline %i' % (key, thead['il'][i]))

        ili = thead['il'][i] - il_min
        xli = thead['xl'][i] - xl_min
        g1[key][ili, xli] = thead[key][i]


fd.close()
