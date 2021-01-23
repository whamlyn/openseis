"""
OpenSeis module
"""

import numpy as np
import os
import openseis as ops

try:
    import h5py
except:
    print('h5py package does not seem to be installed on this system.')


class Seis3D():
    """
    OpenSeis class for 3D seismic datasets
    """

    def __init__(self, sg5file):
        """
        Constructor method for Seis3D class
        """

        self.sg5file = sg5file

        if os.path.exists(self.sg5file):
            self.retreive_attributes()
        else:
            print('No SG5 file found.')

    def retreive_attributes(self):
        """
        Read file attributes from the sd5 file:
        """

        with h5py.File(self.sg5file, 'r') as fd:
            self.il_min = fd.attrs['il_min']
            self.il_max = fd.attrs['il_max']
            self.xl_min = fd.attrs['xl_min']
            self.xl_max = fd.attrs['xl_max']
            self.z_min = fd.attrs['z_min']
            self.z_max = fd.attrs['z_max']
            self.z_type = fd.attrs['z_type']
            self.nil = fd.attrs['nil']
            self.nxl = fd.attrs['nxl']
            self.nz = fd.attrs['nz']


    def get_il(self, il):

        with h5py.File(self.sg5file, 'r') as fd:
            ili = il - fd.attrs['il_min']
            tdata = fd['seis']['tdata'][ili, :]

        return tdata

    def get_xl(self, xl):

        with h5py.File(self.sg5file, 'r') as fd:
            xli = xl - fd.attrs['xl_min']
            tdata = fd['seis']['tdata'][:, xli]

        return tdata

    def get_zslice(self, zval):

        with h5py.File(self.sg5file, 'r') as fd:
            z_min = fd.attrs['z_min']
            dz = fd.attrs['dz']

            zi = round((zval - z_min)/dz)
            tdata = fd['seis']['tdata'][:, :, zi]

        return tdata

    def get_thead(self, key):
        with h5py.File(self.sg5file, 'r') as fd:
            thead = fd['seis']['thead'][key][:]
        return thead

    def open_sd5file(self):
        self.fd = h5py.File(self.sg5file, 'r')
        return self.fd

    def close_sd5file(self, fd=None):
        if fd==None:
            self.fd.close()
        else:
            fd.close()


    def load_from_sgy(self, sgyfile, def_thead):
        """
        Function to create an sg5 (i.e. HDF5) format seismic file by loading trace
        and header data from a SEG-Y datafile.
        """

        # create an auralib Segy object instance
        buf = ops.segy.Segy(sgyfile, def_thead)

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
        with h5py.File(self.sg5file,'w') as fd:

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
                d0[ili[i], xli[i], :] = tdata[i]

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

        self.retreive_attributes()
