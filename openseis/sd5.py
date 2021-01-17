"""
OpenSeis module
"""

import numpy as np

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
