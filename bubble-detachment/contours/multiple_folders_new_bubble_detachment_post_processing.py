"""
Postprocessing code for controlling the volume of the phases in the 3d bubble detachment case.
"""

#-------------------------------------------
# Modules
#-------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import pyvista as pv
import os
import sys

import scienceplots
plt.style.use(['science','ieee'])

from natsort import os_sorted

from functions_bubble_detachment_post_processing import bubble_volume, get_numerical_detachment_time, savitzky_golay, get_contour_at_fixed_time, get_volume_at_time, parse_string

#For controlling font sized globally
SMALL_SIZE = 5
MEDIUM_SIZE = 8
BIGGER_SIZE = 15

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', labelsize=8)             # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

rootdir = sys.argv[1]
savedir = sys.argv[2]

folder_name_list = []
root, dirs, files = next(os.walk(rootdir, topdown=True))

for dir in dirs:
    folder_name_list.append(str(root + "/" + dir))

folder_name_list = os_sorted(folder_name_list)
dirs = os_sorted(dirs)

pparams=dict(xlabel=r'$\text{Time [s]}$', ylabel=r'$\text{Volume [mm$^3$]}$')
pparams1=dict(xlabel=r'$\text{Time [s]}$', ylabel=r'$\text{Contour area derivative [mm$^2.s^{-1}$]}$')
pparams2=dict(xlabel=r'$x\text{ [mm]}$', ylabel=r'$y\text{ [mm]}$')

with plt.style.context(['science', 'ieee']):
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    color = iter(cm.viridis(np.linspace(0.5, 1, len(folder_name_list))))


    #for i in range(len(folder_name_list)):
    for i in [3,0,1,2]:
    #for i in [0,1,2]:
        # Plot the contour area
         c = next(color)
         print(f'Reading directory : {folder_name_list[i]}')
         time, detachment_time,x,y = get_numerical_detachment_time(folder_name_list[i])
         absolute_volume, time_integrated_flux_volume, analytical_volume_array, time = bubble_volume(
         folder_name_list[i])
         detachment_volume = get_volume_at_time(absolute_volume,time,detachment_time)
         print(f'For the folder : {folder_name_list[i]} \n' +
               f'Detachment time : t_det = {detachment_time} s \n' +
               f'Detachment volume : V_det = {detachment_volume} m³')
         shear, density, surface_tension = parse_string(dirs[i])
         shear = shear/0.005
         label_loop = f'S = {shear} s'+r'$^{-1}$' + r' ($t_{det}=$'+f'{detachment_time:2f} s)'
         x_test, y_test = get_contour_at_fixed_time(detachment_time, folder_name_list[i])
         ax2.scatter(x_test, y_test, s=0.5, marker=".", label=label_loop ,color=c)


    ax2.set_xlim(left=-1)
    #ax2.set_ylim([0, 2.5])
    ax2.set(**pparams2)
    handles, labels = plt.gca().get_legend_handles_labels()
    #specify order of items in legend
    if len(folder_name_list)==4:
       order = [0,1,2,3]
    #else:
    #    order=np.range(0,len(folder_name_list))
    #order = [2,0,1]
    #order = [0,1,2]
    #order = [0,1]

    #add legend to plot
    
    #ax2.legend(loc='upper left', frameon=True, edgecolor='k',
              #prop={'size': 4}, ncol=1, fancybox=False)
    #plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order],loc='upper left', frameon=True, edgecolor='k',
              #prop={'size': 4}, ncol=1, fancybox=False)
    fig2.legend(loc='outside center right',frameon = True,edgecolor='k',prop={'size': MEDIUM_SIZE},ncol=1, fancybox=False, bbox_to_anchor=(0.80, -0.15))
    fig2.savefig(savedir + '/' + savedir + '_bubble_contour.pdf', format="pdf", dpi=500)
    fig2.savefig(savedir + '/' + savedir + '_bubble_contour.png', format="png", dpi=500)


