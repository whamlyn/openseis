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
sg5file = r'C:\Users\wesha\Dropbox\source\repos\openseis\devtest\VERTIMIG_v2.sg5'

def_thead = {'il':{'bpos':193,  'fmt':'l', 'nbyte':4},
             'xl':{'bpos':197, 'fmt':'l', 'nbyte':4},
             'cmpx':{'bpos':185, 'fmt':'l', 'nbyte':4},
             'cmpy':{'bpos':189, 'fmt':'l', 'nbyte':4},
             'idcode':{'bpos':29, 'fmt':'h', 'nbyte':2}}

#def load_from_sgy(sgyfile, sg5file, def_thead):
    # """
    # Function to create an sg5 (i.e. HDF5) format seismic file by loading trace
    # and header data from a SEG-Y datafile.
    # """

# create an auralib Segy object instance
buf = aura.segy.Segy(sgyfile, def_thead)

# read all trace data and header data and store in list/dictionary
tdata = buf.read_tdata_multi(0, buf.num_traces, verbose=1000)
thead = buf.read_thead_multi(0, buf.num_traces, verbose=1000)

# convert trace headers to a dictionary of numpy arrays for fast calcuation
tdata = np.array(tdata)
for key in thead.keys():
    thead[key] = np.array(thead[key])

# calculate some statistics from the trace headers and use these to build
# the 3D geometry for the sg5 file
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
#with h5py.File(sg5file,'w') as fd:
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

# create an HDF5 "group" called "seis" to contain seismic trace datasets
g0 = fd.create_group('seis')

# create an HDF5 "dataset" called "tdata" to actually store the traces
d0 = g0.create_dataset('tdata', (nil, nxl, nz))

# create an HDF5 "group" called "seis" to contain trace header datasets
g1 = g0.create_group('thead')

# create multiple HDF% "datasets", one for each trace heder to be loaded
for key in thead.keys():
    d1 = g1.create_dataset(key, (nil, nxl))

# Create the inline and crossline indicies
ili = thead['il'] - il_min
xli = thead['xl'] - xl_min

# Now, write the traces read from the SEG-Y into the HDF5 'tdata' dataset
for i in range(buf.num_traces):

    # print a status message to command line
    if i%nxl == 0:
        print('Writing trace inline %i' % (thead['il'][i]))

    # writing each trace individually, there must be a faster way to do
    # this but the HDF5 indexing isn't as flexible as numpy's; requires
    # further investigation, but at least this works
    d0[ili[i], xli[i]] = tdata[i, :]

# Now, write the trace headers in the HDF5 'thead' group
for key in thead.keys():

    # print a status message to the command line
    print('Writing header key=%s' % (key))

    # the trace headers were easier to set up as an indexed writing
    # operation than the trace data (2d arrays vs 3D arrays). Trace
    # headers more easily fit into memory and could be transformed from a
    # 1D array to a 2D array which was then easily written to a 2D HDF5
    # dataset. This was  much faster than writing each individual header
    # for each individual trace.

    # make 2D numpy array of current trace header field
    tmp = np.zeros([nil, nxl])
    tmp[:,:] = np.nan
    tmp[ili, xli] = thead[key]

    # write 2D numpy array to HDF5 file in a single operation without
    # requiring loops
    g1[key][:, :] = tmp[:, :]

fd.close()