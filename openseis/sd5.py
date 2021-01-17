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

    def __init__(self):

        self.il_min = None
        self.il_max = None
        self.il_step = None

        self.xl_min = None
        self.xl_max = None
        self.xl_step = None

        self.z_min = None
        self.z_max = None
        self.z_step = None

        self.p1x = None
        self.p1y = None
        self.p1il = None
        self.p1xl = None

        self.p2x = None
        self.p2y = None
        self.p2il = None
        self.p2xl = None

        self.p3x = None
        self.p3y = None
        self.p3il = None
        self.p3xl = None

        self.x_origin = None
        self.y_origin = None
        self.azimuth = None

        self.num_samp = None

    def set_geom_3pts(il1, xl1, x1, y1, il2, xl2, x2, y2, il3, xl3, x3, y3):
        """
        Define the geometry of the 3D survey using inline, xline, x, y values
        for 3 points within the survey.

        Parameters
        ----------
        il1 : TYPE
            DESCRIPTION.
        xl1 : TYPE
            DESCRIPTION.
        x1 : TYPE
            DESCRIPTION.
        y1 : TYPE
            DESCRIPTION.
        il2 : TYPE
            DESCRIPTION.
        xl2 : TYPE
            DESCRIPTION.
        x2 : TYPE
            DESCRIPTION.
        y2 : TYPE
            DESCRIPTION.
        il3 : TYPE
            DESCRIPTION.
        xl3 : TYPE
            DESCRIPTION.
        x3 : TYPE
            DESCRIPTION.
        y3 : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
