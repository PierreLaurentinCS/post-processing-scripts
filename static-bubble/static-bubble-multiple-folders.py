"""
Postprocessing code for Static bubble example
This code extracts the difference in pressure betwwen the interior and the
exterior of the bubble for multiple folders

This should be called as follows : python3 static-bubble-multiple-folders.py
outputs
"""
# -------------------------------------------
# Modules
# -------------------------------------------

from postprocessing_static_bubble import get_pressure_difference, \
    analytical_solution, get_velocity_error_time,get_pressure_slice
import numpy as np
import os
import sys
import scienceplots
from natsort import os_sorted
import matplotlib.pyplot as plt

# For plotting nice Latex-style plots and controlling the sizes of the texts on
# the plot
plt.style.use(['science', 'ieee'])

SMALL_SIZE = 10
MEDIUM_SIZE = 10
BIGGER_SIZE = 15
plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=8)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=8)  # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


class parametres():
    sigma = 1
    radius = 0.15

    def set_radius(self, r):
        self.radius = r


prm = parametres()

rootdir = sys.argv[1]

folder_name_list = []
root, dirs, files = next(os.walk(rootdir, topdown=True))

for dir in dirs:
    folder_name_list.append(str(root + "/" + dir))

folder_name_list = os_sorted(folder_name_list)
dirs = os_sorted(dirs)

print(folder_name_list)
print(dirs)

with plt.style.context(['science', 'ieee']):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    pparams = dict(xlabel=r'$\text{Rayon} (R) \text{[m]}$',
                   ylabel=r'$\Delta p \text{[Pa]}$')

plots = []

for i in range(len(folder_name_list)):
    radius = float(dirs[i][2:])
    prm.set_radius(radius)
    pressure_diff = get_pressure_difference(folder_name_list[i], prm)
    # Store the plot handle with label "Lethe"
    plot_handle, = ax.plot(radius, pressure_diff, 'k*', label="Lethe")
    if i == 0:  # Store the handle only once
        plots.append(plot_handle)

# Store the analytical solution plot handle
radius_array, pressure_diff_analytical = analytical_solution(prm)
analytical_handle, = ax.plot(radius_array, pressure_diff_analytical, label=r'$\Delta p$ analytique (Young-Laplace)')
plots.append(analytical_handle)

# Set the legend with the stored handles
ax.legend(handles=plots, loc='upper right', frameon=True, edgecolor='k', prop={'size': 8}, ncol=1)

ax.set(**pparams)
ax.set_xlim([0, 0.5])
ax.set_ylim([2, 10])
fig.savefig('pressure-difference.pdf', format="pdf", dpi=500)
fig.savefig('pressure-difference.png', format="png", dpi=500)

with plt.style.context(['science', 'ieee']):
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    pparams1 = dict(xlabel=r'$\text{Time [s]}$',
                    ylabel=r'$\mathrm{Velocity} \; L_2{\text-} \text{error}$')
    for i in range(len(folder_name_list)):
        time, error_velocity = get_velocity_error_time(folder_name_list[i])
        label_loop = r'$R = \;$' + dirs[i][2:] + r'$\text{[m]}$'
        ax1.plot(time, error_velocity,label=label_loop )
    ax1.ticklabel_format(axis='y', scilimits=[-1, 1])    
    ax1.legend(loc='upper right', frameon=True, edgecolor='k',
               prop={'size': MEDIUM_SIZE}, ncol=1)
    ax1.set(**pparams1)
    ax1.grid(which='major', color='lightgrey', linestyle='--',alpha=0.8)
    ax1.set_xlim([0, 3])
    #ax1.set_ylim([, 10])
    fig1.savefig('l2-error-velocity.pdf', format="pdf", dpi=500)
    
with plt.style.context(['science', 'ieee']):
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    pparams1 = dict(xlabel=r'$x \text{[m]}$',
                    ylabel=r'$\mathrm{Pression} \text{[Pa]}$')
    for i in range(len(folder_name_list)):
        p, x = get_pressure_slice(folder_name_list[i])
        label_loop = r'$R = $ ' + dirs[i][2:] + r'$ \text{[m]}$'
        ax2.plot(x, p,label=label_loop )
    ax2.legend(loc='upper left', frameon=True, edgecolor='k',
               prop={'size': 8.5}, ncol=1)
    ax2.set(**pparams1)
    ax2.grid(which='major', color='lightgrey', linestyle='--',alpha=0.8)
    fig2.savefig('pressure-profile.pdf', format="pdf", dpi=500)
    fig2.savefig('pressure-profile.png', format="png", dpi=500)
