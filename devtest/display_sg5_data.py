# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 14:00:08 2021

@author: wesha
"""

#%%

import numpy as np
import matplotlib.pyplot as plt
import auralib as aura
import openseis as os

sg5file = r'C:\Users\wesha\Dropbox\source\repos\openseis\devtest\VERTIMIG.sg5'

buf = os.sd5.Seis3D(sg5file)

tdata = buf.get_zslice(0.97)
thead = buf.get_thead('cmpy')

fig = plt.figure(num=1)
fig.clf()

ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222, sharex=ax1, sharey=ax1)
ax3 = fig.add_subplot(212)

amp = 5

ax1.imshow(tdata, cmap=plt.cm.bwr_r, vmin=-amp, vmax=amp)

ax2.imshow(thead, cmap=plt.cm.jet)

ax3.imshow(buf.get_il(140).T, plt.cm.bwr_r, vmin=-amp, vmax=amp)
ax3.set_aspect('auto')
ax3.set_ylim(1000, 200)
ax3.invert_xaxis()

ax1.set_aspect(1.0)
ax1.invert_xaxis()
ax1.invert_yaxis()

plt.show()