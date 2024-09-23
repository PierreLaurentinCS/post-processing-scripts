"""
Postprocessing code for mms on Cahn-Hilliard equations
"""

#-------------------------------------------
# Modules
#-------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyvista as pv

import os
import sys

import scienceplots
plt.style.use(['science','ieee'])

from natsort import os_sorted

from functions import get_errors

#For controlling font sized globally
SMALL_SIZE = 7
MEDIUM_SIZE = 10
BIGGER_SIZE = 15

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', labelsize=11)             # fontsize of the x and y labels
plt.rc('xtick', labelsize=6)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

rootdir = sys.argv[1]

folder_name_list = []
root, dirs, files = next(os.walk(rootdir, topdown=True))

for dir in dirs:
    folder_name_list.append(str(root + "/" + dir))

folder_name_list = os_sorted(folder_name_list)
dirs = os_sorted(dirs)

pparams=dict(xlabel=r'$\Delta x$', ylabel=r'$\text{Erreur }L^2$')
marker_colors = ['black','brown','darkblue']
line_colors = ['gray','indianred','#3a6f9c']

with plt.style.context(['science', 'ieee']):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for i in range(len(folder_name_list)):
        # Plot the L2-error
        delta_x, errors_phase = get_errors(folder_name_list[i])
        label_loop = dirs[i]
        for j in range(len(errors_phase)):
            # Plot the theoretical line
            ax.loglog(delta_x, delta_x ** (j + 2) / (
                    delta_x[0] ** (j + 2) / errors_phase[j][0]),
                      c=line_colors[j], ls='--')
            # Plot the actual error points
            ax.loglog(delta_x, errors_phase[j], label='Degré ' + str(j + 1) + " d'interpolation",
                      lw=1, linestyle='', c=line_colors[j], mec=marker_colors[j], markersize=11,
                      marker=(j + 2, 2, 0))
            # Add text box with slope information
            if j==0:
                #text_x = 0.045  # X position for text; text_x = 0.045 for 3d
                text_x = 10e-3 # X position for text; text_x = 8e-3 for 2d
            #text_y = errors_phase[j][len(errors_phase[j]) // 2] * 0.65  # Y position for text, slightly above the point 3D
            text_y = errors_phase[j][len(errors_phase[j]) // 2] * 0.65
            ax.text(text_x, text_y, r'$\frac{\log(e)}{\log(\Delta x)} = $' + '{}'.format(j + 2),
                    color=marker_colors[j], fontsize=12, ha='center', va='bottom')

        plt.grid(which='both')

    # ax.set_ylim([1e-9,1e-1])
    # ax.set_xlim([2e-2, 3e-1])
    ax.legend(loc='lower right', frameon=True, edgecolor='k',
              prop={'size': SMALL_SIZE}, ncol=1, fancybox=False,labelspacing = 0.69)
    #plt.legend(labelspacing = 1) 
    ax.set(**pparams)
    fig.savefig('mms-2d.pdf', format="pdf", dpi=500)
    fig.savefig('mms-2d.png', format="png", dpi=500)
