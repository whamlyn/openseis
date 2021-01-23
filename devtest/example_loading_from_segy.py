# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 12:43:36 2021

@author: wesha
"""

#%%

import numpy as np
import matplotlib.pyplot as plt
import auralib as aura
import openseis as ops

sgyfile = r'C:\Users\wesha\Dropbox\data\Blackfoot\VERTIMIG.sgy'
sg5file = r'C:\Users\wesha\Dropbox\source\repos\openseis\devtest\VERTIMIG_v3.sg5'

def_thead = {'il':{'bpos':193,  'fmt':'l', 'nbyte':4},
             'xl':{'bpos':197, 'fmt':'l', 'nbyte':4},
             'cmpx':{'bpos':185, 'fmt':'l', 'nbyte':4},
             'cmpy':{'bpos':189, 'fmt':'l', 'nbyte':4},
             'idcode':{'bpos':29, 'fmt':'h', 'nbyte':2}}


buf = ops.sd5.Seis3D(sg5file)
buf.load_from_sgy(sgyfile, def_thead)