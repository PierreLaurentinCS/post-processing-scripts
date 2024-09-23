"""
Postprocessing code for plotting the detachment time and volume detachment for the bubble detachment in shear flow case.
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


#For controlling font sizes globally
SMALL_SIZE = 10
MEDIUM_SIZE = 8
BIGGER_SIZE = 15

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', labelsize=SMALL_SIZE)             # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

pparams=dict(xlabel=r'$\text{Taux de cisaillement \;[s}^{-1}\text{]}$', ylabel=r'$V_{det} \text{[mm$^3$]}$')
pparams1=dict(xlabel=r'$\text{Taux de cisaillement \;[s}^{-1}\text{]}$', ylabel=r'$t_{det} \text{[s]}$')
pparams3=dict(xlabel=r'$\Delta x_\text{uniforme} \;\text{[m]}$', ylabel=r'$t_{det} \text{[s]}$')
pparams2=dict(xlabel=r'$\Delta x_\text{uniforme} \; \text{[m]}$', ylabel=r'$V_{det} \text{[mm$^3$]}$')
#-------------------------------------------
# Below are the results obtained by Mirsandi et al.
#-------------------------------------------

volume_air_flow_ref = [26.937799043062203, 22.966507177033492, 19.76076555023924, 16.842105263157897, 12.822966507177034, 10.526315789473687, 8.94736842105263, 7.799043062200962, 6.794258373205739, 6.076555023923449, 5.502392344497613, 5.071770334928232] # in mm³
time_air_flow_ref = [0.05345104333868377, 0.045264847512038506, 0.039004815409309786, 0.03322632423756015, 0.025040128410914936, 0.020706260032102762, 0.017817014446227943, 0.01540930979133226, 0.01252006420545744, 0.011556982343499167, 0.010593900481540896, 0.009630818619582676]
shear_ref = [0.576923076923067, 44.42307692307691, 66.92307692307688, 89.42307692307689, 133.84615384615384, 178.26923076923066, 222.11538461538456, 265.96153846153834, 311.5384615384615, 355.96153846153834, 400.38461538461524, 444.8076923076922]

time_surface_tension_low = []
time_surface_tension_high = []
volume_surface_tension_low = []
volume_surface_tension_high = []

time_density_low = []
time_density_high = []
volume_density_low = []
volume_density_high = []

#-------------------------------------------
# Below are the results obtained from the simulations
# Be aware that the inlet velocity (500mm³/s) is not
# the one used by Mirsandi et al. for their parametric
# sweep (167mm³/s). This for a more various results pool
# This does not make much difference.
# How to sya it in the master's thesis? Since we have very similar results for the case with regular properties, it is interesting to see if the solver is able to get coherent results using closely (but not exactly) similar physical properties.
#-------------------------------------------
TBD = 0

# Expected results for simulations that are still running. Should be replaced by simulated values it is done
expected_volume_no_shear_high_sigma = 57.2
expected_time_no_shear_high_sigma = 0.141
expected_volume_no_shear_low_density = 106.5
expected_time_no_shear_low_density = 0.2

expected_volume_S_100_low_density = 40.5
expected_time_S_100_low_density = 0.1
expected_volume_S_200_low_density = 18.85
expected_time_S_200_low_density = 0.054


shear = [0,100,200,300,450]

time_air_flow_simulation = [0.0602499,0.0331663,0.0185421,0.0138963,0.009816]
volume_air_flow_simulation = [28.349,15.386,9.336,6.3796,5.0455]

time_surface_tension_low = [0.0255157,0.0199485,0.0153284,0.013041,0.0123957]
time_surface_tension_high = [0.143158,0.0647685,0.0383104,0.0259236,0.0173563]
volume_surface_tension_low = [12.651,9.9247,7.6693,6.5498,6.18]
volume_surface_tension_high = [60.473,25.138,13.622,8.7991,5.6187]


time_density_low = [expected_time_no_shear_low_density,0.074467,0.0417058,0.0282051,0.0186395]
time_density_high = [0.0343434,0.0224821,0.0152106,0.0121619,0.00996644]
volume_density_low = [expected_volume_no_shear_low_density,33.535,18.52,12.45,8.1678]
volume_density_high = [16.343,10.531,7.0437,5.5755,4.4931]




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
    fig7 = plt.figure()
    ax7 = fig7.add_subplot(111)
    
    #-------------------------------------------
    # Comparison between Mirsandi and our results for regular properties
    #-------------------------------------------

    ax.plot(shear_ref, time_air_flow_ref,"ro",markerfacecolor='none', lw=1,
                 label= r'Mirsandi et al.')
    ax.plot(shear,time_air_flow_simulation,"k^",markerfacecolor='none',lw=1,
                 label= r'Lethe - CHNS')

    ax.set(**pparams1)
    ax.legend(loc='upper right', frameon=True, edgecolor='k',
               prop={'size': SMALL_SIZE}, ncol=1, fancybox=False)

    ax.set_xlim([-10, 460])
    ax.set_ylim([0, 0.062])
    
    
    ax1.plot(shear_ref, volume_air_flow_ref,"ro",markerfacecolor='none', lw=1,
                 label= r'Mirsandi et al.')
    ax1.plot(shear,volume_air_flow_simulation,"k^",markerfacecolor='none',lw=1,
                 label= r'Lethe - CHNS')

    ax1.set(**pparams)
    ax1.legend(loc='upper right', frameon=True, edgecolor='k',
               prop={'size': SMALL_SIZE}, ncol=1, fancybox=False)

    ax1.set_xlim([-10, 460])
    #ax1.set_ylim([0, 0.062])
    
    fig.savefig('time_comparison_regular.pdf', format="pdf", dpi=500)
    fig.savefig('time_comparison_regular.png', format="png", dpi=500)
    fig1.savefig('volume_comparison_regular.pdf', format="pdf", dpi=500)
    fig1.savefig('volume_comparison_regular.png', format="png", dpi=500)
    
    #-------------------------------------------
    # Density sweep (detachment time and volume)
    #-------------------------------------------
    
    ax2.plot(shear[1:],time_density_low[1:],"b^",markerfacecolor='none',lw=1,
                 label= r'$\rho_l / \rho_w = 0.2$')
    #ax2.plot(shear[:2],time_density_low[:2],"bx",markerfacecolor='none',lw=1,
                 #label= r'$\rho_l / \rho_w = 0.2$ (valeurs attendues)')            
    ax2.plot(shear,time_air_flow_simulation,"k^",markerfacecolor='none',lw=1,
                 label= r'$\rho_l / \rho_w = 1$')
    ax2.plot(shear,time_density_high,"r^",markerfacecolor='none',lw=1,
                 label= r'$\rho_l / \rho_w = 2.5$')
    ax2.set(**pparams1)
    ax2.legend(loc='upper right', frameon=True, edgecolor='k',
               prop={'size': SMALL_SIZE}, ncol=1, fancybox=False)
               
    ax3.plot(shear[1:],volume_density_low[1:],"b^",markerfacecolor='none',lw=1,
                 label= r'$\rho_l / \rho_w = 0.2$')   
    #ax3.plot(shear[:2],volume_density_low[:2],"bx",markerfacecolor='none',lw=1,
                 #label= r'$\rho_l / \rho_w = 0.2$ (valeurs attendues)')
    ax3.plot(shear,volume_air_flow_simulation,"k^",markerfacecolor='none',lw=1,
                 label= r'$\rho_l / \rho_w = 1$')
    ax3.plot(shear,volume_density_high,"r^",markerfacecolor='none',lw=1,
                 label= r'$\rho_l / \rho_w = 2.5$')
    ax3.set(**pparams)
    ax3.legend(loc='upper right', frameon=True, edgecolor='k',
               prop={'size': SMALL_SIZE}, ncol=1, fancybox=False)
               
    fig2.savefig('time_density_sweep.pdf', format="pdf", dpi=500)
    fig2.savefig('time_density_sweep.png', format="png", dpi=500)
    fig3.savefig('volume_density_sweep.pdf', format="pdf", dpi=500)
    fig3.savefig('volume_density_sweep.png', format="png", dpi=500)
               
    #-------------------------------------------
    # Surface tension sweep (detachment time and volume)
    #-------------------------------------------
                 
    ax4.plot(shear,time_surface_tension_low,"b^",markerfacecolor='none',lw=1,
                 label= r'$\sigma / \sigma_w = 0.2$')
    ax4.plot(shear,time_air_flow_simulation,"k^",markerfacecolor='none',lw=1,
                 label= r'$\sigma / \sigma_w = 1$')
    ax4.plot(shear,time_surface_tension_high,"r^",markerfacecolor='none',lw=1,
                 label= r'$\sigma / \sigma_w = 2.5$')
    #ax4.plot(shear[0],time_surface_tension_high[0],"rx",markerfacecolor='none',lw=1,
                 #label= r'$\sigma / \sigma_w = 2.5$ (valeurs attendues)')
    ax4.set(**pparams1)
    ax4.legend(loc='upper right', frameon=True, edgecolor='k',
               prop={'size': SMALL_SIZE}, ncol=1, fancybox=False)
               
    ax5.plot(shear,volume_surface_tension_low,"b^",markerfacecolor='none',lw=1,
                 label= r'$\sigma / \sigma_w = 0.2$')
    ax5.plot(shear,volume_air_flow_simulation,"k^",markerfacecolor='none',lw=1,
                 label= r'$\sigma / \sigma_w = 1$')
    ax5.plot(shear,volume_surface_tension_high,"r^",markerfacecolor='none',lw=1,
                 label= r'$\sigma / \sigma_w = 2.5$')
    #ax5.plot(shear[0],volume_surface_tension_high[0],"rx",markerfacecolor='none',lw=1,
                 #label= r'$\sigma / \sigma_w = 2.5$ (valeurs attendues)')
    ax5.set(**pparams)
    ax5.legend(loc='upper right', frameon=True, edgecolor='k',
               prop={'size': SMALL_SIZE}, ncol=1, fancybox=False)

    fig4.savefig('time_surface_tension_sweep.pdf', format="pdf", dpi=500)
    fig4.savefig('time_surface_tension_sweep.png', format="png", dpi=500)
    fig5.savefig('volume_surface_tension_sweep.pdf', format="pdf", dpi=500)
    fig5.savefig('volume_surface_tension_sweep.png', format="png", dpi=500)
    
    #-------------------------------------------
    # Grid convergence analysis (detachment time and volume)
    #-------------------------------------------
    
    delta_x_list = [8*6.25e-5,8*3.125e-5,8*2.08e-5,8*1.56e-5]
    t_det_list = [0.0110940890499,0.0102861292193,0.00981588,0.00973563]
    v_det_list = [5.1685,5.3935,5.0455,5.0509]
    delta_x_ref = [8.00e-5]
    v_det_ref = [5.011]
    t_det_ref = [9.960e-3]
    
    ax6.plot(delta_x_list,v_det_list,"-k^",lw=1,
                 label= r'Lethe - CHNS')
    ax6.axhline(v_det_ref,ls="--",color='r',lw=1,
                 label= r'Mirsandi et al.')
    ax6.set(**pparams2)
    ax6.legend( frameon=True, edgecolor='k',
               prop={'size': SMALL_SIZE}, ncol=1, fancybox=False)
    #ax6.invert_xaxis()
    ax7.plot(delta_x_list,t_det_list,"-k^",lw=1,
                 label= r'Lethe - CHNS')
    ax7.axhline(t_det_ref,ls="--",color='r',lw=1,
                 label= r'Mirsandi et al.')
    ax7.set(**pparams3)    
    ax7.legend( frameon=True, edgecolor='k',
               prop={'size': SMALL_SIZE}, ncol=1, fancybox=False)
    #ax7.invert_xaxis()
    
    fig7.savefig('time_grid_convergence.pdf', format="pdf", dpi=500)
    fig7.savefig('time_grid_convergence.png', format="png", dpi=500)
    fig6.savefig('volume_grid_convergence.pdf', format="pdf", dpi=500)
    fig6.savefig('volume_grid_convergence.png', format="png", dpi=500)         
    
    
    
