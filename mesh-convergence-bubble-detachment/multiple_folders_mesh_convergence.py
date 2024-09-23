"""
Postprocessing code for controlling the volume of the phases in the 3d bubble detachment case.
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

from mesh_convergence import bubble_volume, get_numerical_detachment_time, savitzky_golay, get_contour_at_fixed_time

#For controlling font sized globally
SMALL_SIZE = 8
MEDIUM_SIZE = 8
BIGGER_SIZE = 15

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', labelsize=8)             # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

rootdir = sys.argv[1]

folder_name_list = []
root, dirs, files = next(os.walk(rootdir, topdown=True))

delta_x_in=[0.0000625,0.5*0.0000625,2.43e-5,0.5*0.5*0.0000625]
delta_x_u=[0.5e-3,0.5*0.5e-3,1.95e-4,0.5*0.5*0.5e-3]
for dir in dirs:
    folder_name_list.append(str(root + "/" + dir))

folder_name_list = os_sorted(folder_name_list)
dirs = os_sorted(dirs)

pparams=dict(xlabel=r'$\text{Time [s]}$', ylabel=r'$\text{Volume [mm$^3$]}$')
pparams1=dict(xlabel=r'$\text{Time [s]}$', ylabel=r'$\text{Dérivée de l}'+ "'"+ r'\text{aire du contour [mm$^2.s^{-1}$]}$')
pparams2=dict(xlabel=r'$x\text{ [mm]}$', ylabel=r'$y\text{ [mm]}$')

with plt.style.context(['science', 'ieee']):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    fig3 = plt.figure()
    ax3 = fig3.add_subplot(111)
    fig4 = plt.figure()
    ax4 = fig4.add_subplot(111)
    fig5 = plt.figure()
    ax5 = fig5.add_subplot(111)
    fig6 = plt.figure()
    ax6 = fig6.add_subplot(111)

    for i in range(len(folder_name_list)):
        # Plot the contour area
         print(f'Reading directory : {folder_name_list[i]}')
         time, contour_area_list, contour_area_derivative, detachment_time,x,y = get_numerical_detachment_time(folder_name_list[i])
         #print(detachment_time)
         #contour_area_derivative = savitzky_golay(contour_area_derivative,5,0)

         label_loop = dirs[i]
         #ax1.plot(time, contour_area_list, lw=1, label='Contour area ' + label_loop,
                      #linestyle='solid')
         p = ax1.plot(time, contour_area_derivative, lw=1, label=label_loop + r' raffinements' +'\n' + r'$ t_{\text{det}} =$' + f'{detachment_time:1f} s',
                      linestyle='solid')
         x_test, y_test = get_contour_at_fixed_time(detachment_time, folder_name_list[i])
         delta_x_u_loop = delta_x_u[i]
         delta_x_in_loop = delta_x_in[i]
         ax2.scatter(x_test, y_test, s=0.5, marker=".", label=label_loop + r' raffinements' +'\n' + r'$ t_{\text{det}} =$' + f'{detachment_time:1f} s' + '\n' + r'$\Delta_{x,u} =$' + f'{delta_x_u_loop:.2E} m' + '\n' + r'$\Delta_{x,in} =$' + f'{delta_x_in_loop:.2E} m')
         color = p[0].get_color() # 'b'
         ax1.axvline(detachment_time, color=color,
                ls='--')

         ax5.plot(time, contour_area_derivative, lw=1,
             label=label_loop + r' raffinement' +'\n' + r'$ t_{\text{det}} =$' + f'{detachment_time:1f} s',
             linestyle='solid')
         ax5.axvline(detachment_time, color=color,
                ls='--')


    ax2.set_xlim([-1, 5])
    ax2.set_ylim([0, 3])
    ax2.set(**pparams2)
    # ax2.legend(loc='upper left', frameon=True, edgecolor='k',
    #           prop={'size': SMALL_SIZE}, ncol=1, fancybox=False)
    fig2.legend(loc='outside center right', frameon=True, edgecolor='k',
               prop={'size': SMALL_SIZE}, ncol=1, fancybox=False,
               bbox_to_anchor=(1.35, 0.5))
    fig2.savefig('bubble_contour.pdf', format="pdf", dpi=500)
    fig2.savefig('bubble_contour.png', format="png", dpi=500)
    ax2.axvline(9.787E-03, label="Temps de détachement (Mirsandi et al.)", color='b',
                ls='--')
    ax1.set(**pparams1)
    #ax1.legend(loc='lower left', frameon=True, edgecolor='k',
              #prop={'size': SMALL_SIZE}, ncol=1, fancybox=False)
    fig1.legend(loc='outside center right', frameon=True, edgecolor='k',
               prop={'size': SMALL_SIZE}, ncol=1, fancybox=False,
               bbox_to_anchor=(1.30, 0.5))
    ax5.set_xlim([0.0095, 0.0115])
    ax5.set(**pparams1)
    # ax5.legend(loc='lower left', frameon=True, edgecolor='k',
    #           prop={'size': SMALL_SIZE}, ncol=1, fancybox=False)
    fig5.legend(loc='outside center right', frameon=True, edgecolor='k',
               prop={'size': SMALL_SIZE}, ncol=1, fancybox=False,
               bbox_to_anchor=(1.30, 0.5))
    fig5.savefig('bubble_contour_area_zoom.pdf', format="pdf", dpi=500)
    fig5.savefig('bubble_contour_area_zoom.png', format="png", dpi=500)
    fig1.savefig('bubble_contour_area.pdf', format="pdf", dpi=500)
    fig1.savefig('bubble_contour_area.png', format="png", dpi=500)


    for i in range(len(folder_name_list)):
        # Plot the bubble volume
         absolute_volume, time_integrated_flux_volume,analytical_volume_array,time = bubble_volume(folder_name_list[i])
         label_loop = dirs[i]
         ax.plot(time, absolute_volume, lw=1, label= label_loop + ' raffinement',
                linestyle='solid')
         ax6.plot(time, absolute_volume, lw=1, label=label_loop + ' raffinement',
            linestyle='solid')
         # ax.plot(time, time_integrated_flux_volume, lw=1, label='Time integrated flux volume ' + label_loop,
         #        linestyle='solid')
         # if i==len(folder_name_list)-1:
         #     ax.plot(time, analytical_volume_array, lw=1, label='Analytical volume ', linestyle='--')


    ax.axvline(9.787E-03,label="Temps de détachement (Mirsandi et al.)" + "\n" + r'$t_{det} = 0.009787$ s',color='k', ls='--')
    ax.axhline(5.0424,label="Volume au détachement (Mirsandi et al.)" + "\n" + r'$V_{det} = 5.0424$ mm$^3$',color='k', ls='--')
    ax6.axvline(9.787E-03,label="Temps de détachement (Mirsandi et al.)" + "\n" + r'$t_{det} = 0.009787$ s',color='k', ls='--')
    ax6.axhline(5.0424,label="Volume au détachement (Mirsandi et al.)" + "\n" + r'$V_{det} = 5.0424$ mm$^3$',color='k', ls='--')
    ax.set_xlim([0, 0.0125])
    ax.set_ylim([0, 6])
    ax6.set_xlim([0.0095, 0.01])
    ax6.set_ylim([4.4, 5.4])
    #ax.legend(loc='lower right', frameon=True, edgecolor='k',
               #prop={'size': SMALL_SIZE}, ncol=1, fancybox=False)
    fig.legend(loc='outside center right', frameon=True, edgecolor='k',
               prop={'size': SMALL_SIZE}, ncol=1, fancybox=False,
               bbox_to_anchor=(1.60, 0.5))
    ax.set(**pparams)
    fig6.legend(loc='outside center right', frameon=True, edgecolor='k',
               prop={'size': SMALL_SIZE}, ncol=1, fancybox=False,
               bbox_to_anchor=(1.60, 0.5))
    ax6.set(**pparams)
    fig.savefig('bubble_volume.pdf', format="pdf", dpi=500)
    fig.savefig('bubble_volume.png', format="png", dpi=500)
    fig6.savefig('bubble_volume_zoom.pdf', format="pdf", dpi=500)
    fig6.savefig('bubble_volume_zoom.png', format="png", dpi=500)

    fixed_time = 9.0e-3
    for i in range(len(folder_name_list)):
        x,y = get_contour_at_fixed_time(fixed_time,folder_name_list[i])
        label_loop = dirs[i]
        ax3.scatter(x, y, s=0.5, marker=".",
                    label="Contour at fixed time " + label_loop + f'(t ={fixed_time:2f} [s])')
        ax3.set_xlim([-1, 5])
        ax3.set_ylim([0, 2.5])
        ax3.set(**pparams2)
        ax3.legend(loc='upper left', frameon=True, edgecolor='k',
                   prop={'size': 4}, ncol=1, fancybox=False)
        fig3.savefig('bubble_contour_fixed_t='+f'{fixed_time}'+'.pdf', format="pdf", dpi=500)
        fig3.savefig('bubble_contour_fixed_t='+f'{fixed_time}'+'.png', format="png", dpi=500)


