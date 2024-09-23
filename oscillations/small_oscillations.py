#############################################################################

# Importing libraries
import numpy as np
import sys
import matplotlib.pyplot as plt
import pyvista as pv
import os
from natsort import os_sorted
import scienceplots
plt.style.use(['science','ieee'])
#############################################################################

#For controlling font sized globally
SMALL_SIZE = 14
MEDIUM_SIZE = 8
BIGGER_SIZE = 15

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', labelsize=SMALL_SIZE)             # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

#############################################################################

# Take case path as argument and store it
output_dir = sys.argv[1]
n = int(output_dir[-1])
t_list = []
y_list = []

# Make the plot of the contour of the bubble
list_latest_files = []
list_list_vtu = []


def get_bubble_top_point(output_path):
    list_vtu = os.listdir(output_path)
    pvd_file = [x for x in list_vtu if (x.endswith('.pvd'))]
    if len(pvd_file) == 0:
        print(f"Folder {output_path} is empty! Returning empty lists")
        return [],[]

    list_vtu = [x for x in list_vtu if ("pvtu" in x)]
    list_vtu = os_sorted(list_vtu)
    reader = pv.get_reader(output_path + "/" + pvd_file[0])
    time = np.array(reader.time_values)
    coordinate_of_interest=np.zeros(len(time))

    for i, vtu_file in enumerate(list_vtu):
        sim = pv.read(f"{output_path}/{vtu_file}")
        if "phase_order" not in sim.point_data.keys():
            print(f"Skipping {vtu_file} : corrupted")
            continue
        sim.set_active_scalars("phase_order")
        contour_val = np.array([0.0])
        contour = sim.contour(contour_val, scalars='phase_order')
        if n==2 or n==4:
            y = contour.points[:, 1]
            coordinate_of_interest[i]=np.max(y)
        elif n==3:
            x = contour.points[:, 0]
            coordinate_of_interest[i]=np.max(x)
        else:
            raise Exception("Choix de coordonées incorrect (x ou y)")
    return coordinate_of_interest,time

analytical_times=[4.192e-4,2.096e-4,1.326e-4]

if n==2 or n==4:
    pparams=dict(xlabel=r'Time [ms]', ylabel=r'$y_P \text{[}\mu\text{m]}$')
elif n==3:
    pparams=dict(xlabel=r'Time [ms]', ylabel=r'$x_P \text{[}\mu\text{m]}$')
else:
    raise Exception("Choix de coordonées incorrect (x ou y)")


with plt.style.context(['science', 'ieee']):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    print(f'Reading directory : {output_dir}')
    coordinate,time = get_bubble_top_point(output_dir)
    time=1000*time
    coordinate = 1000*coordinate
    label_loop = output_dir

    ax.plot(time, coordinate-np.mean(coordinate), lw=1,
             label="Lethe" ,linestyle='solid')
    ax.axvline(1000*analytical_times[n-2],label=f'$T_{n}$', color="k",ls="dashed")
    ax.set(**pparams)
    #ax.set_xlim(left=0,right=0.6) #n=2
    ax.set_xlim(left=0,right=0.3) #n=3 et n=4
    #ax.legend(loc='upper left', prop={'size': SMALL_SIZE}, ncol=1, fancybox=False)
    #ax.legend( prop={'size': SMALL_SIZE}, ncol=1, fancybox=False) # n=2
    #ax.legend(loc='upper right', prop={'size': SMALL_SIZE}, ncol=1, fancybox=False) # n=4
    #plt.legend(bbox_to_anchor=(0.10, 0.35), loc='upper left') #n=2
    plt.legend(bbox_to_anchor=(0.10, 1), loc='upper left') #n=3
    #plt.legend(bbox_to_anchor=(0.10, 0.35), loc='upper left') #n=4
    fig.savefig(f'n={n}.png',format="png", dpi=500)
    fig.savefig(f'n={n}.pdf',format="pdf", dpi=500)

