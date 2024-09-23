"""
Postprocessing code for rayleigh-taylor-instability example
This code extracts the y position of the bubble and the spike and compares it
to the results of He et al (1999)
"""

#-------------------------------------------
# Modules
#-------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyvista as pv
from natsort import os_sorted
import os
import sys
import scienceplots
plt.style.use(['science', 'ieee'])

#--------------------------------------------
# Main
#--------------------------------------------

#For controlling font sized globally
SMALL_SIZE = 9
MEDIUM_SIZE = 10
BIGGER_SIZE = 10
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', labelsize=SMALL_SIZE)             # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

#To make it work, type "python3 rayleigh-taylor_postprocess.py ./output/adaptive/" or
#"python3 rayleigh-taylor_postprocess.py ./output/constant/" into the terminal.


#Load reference data from He et al (1999)
ref_data_file = "ref_He_et_al_data.txt"
ref_data = np.loadtxt(ref_data_file,skiprows=1)
ref_time = ref_data[:,0]
ref_y_bubble = ref_data[:,1]
ref_y_spike = ref_data[:,2]



#Constants
H = 0.25
g = 9.81

#Set phase_limit to search for y values
phase_limit = 0

#Take case path as argument and store it
output_path = sys.argv[1]

#Define list of VTU files
list_vtu = os.listdir(output_path)
list_vtu = [x for x in list_vtu if ("pvtu" in x)]

print(len(list_vtu))

# Sort VTU files to ensure they are in the same order as the time step
list_vtu = os_sorted(list_vtu)
print(list_vtu)
# Read the pvd file to extract the times
reader = pv.get_reader("./output-chns-oscillations/rayleigh-taylor-chns.pvd")

# Get active times
time_list = reader.time_values
time_list = [x * ((g/H)**0.5) for x in time_list]

#Create a list to fill with maximum y in which phase < phase_limit
y_bubble_list = []

#Create a list to fill with minimum y in which phase > phase_limit
y_spike_list = []

#Create beginning and end points for spike line
a_spike = [0.125, 0, 0]
b_spike = [0.125, 1, 0]

#Create beginning and end points for bubble line
a_bubble = [0, 0, 0]
b_bubble = [0, 1, 0]

#Read VTU files
for vtu_file in list_vtu:
    sim = pv.read(f"{output_path}/{vtu_file}")

    sampled_data_spike = sim.sample_over_line(a_spike, b_spike, resolution=1000)
    phase_spike = pd.DataFrame(sampled_data_spike["phase_order"])
    points_spike = pd.DataFrame(sampled_data_spike.points)

    sampled_data_bubble = sim.sample_over_line(a_bubble, b_bubble, resolution=1000)
    phase_bubble = pd.DataFrame(sampled_data_bubble["phase_order"])
    points_bubble = pd.DataFrame(sampled_data_bubble.points)

    #Find min 'y' in phase > phase_limit (SPIKE)
    fluid1_points = points_spike[phase_spike[0] < phase_limit].values
    y_min = fluid1_points[0][1]
    for points in fluid1_points:
        if points[1] < y_min:
            y_min = points[1]
    y_spike_list.append(y_min)

    #Find max 'y' in phase < phase_limit (BUBBLE)
    fluid0_points = points_bubble[phase_bubble[0] > phase_limit].values
    y_max = fluid0_points[0][1]
    for points in fluid0_points:
        if points[1] > y_max:
            y_max = points[1]
    y_bubble_list.append(y_max)

bulle_vof=[0.524, 0.524, 0.528, 0.54, 0.552, 0.563, 0.572, 0.58, 0.588, 0.594, 0.6, 0.604, 0.609, 0.614, 0.617, 0.62, 0.624, 0.626, 0.629, 0.631, 0.635, 0.637, 0.639, 0.641, 0.643, 0.646, 0.649, 0.651, 0.653, 0.655, 0.657, 0.659, 0.662, 0.664, 0.666, 0.668, 0.671, 0.674, 0.676, 0.678, 0.682, 0.684, 0.687, 0.69, 0.692, 0.696, 0.698, 0.701, 0.704, 0.706, 0.709, 0.711, 0.714, 0.717]

pointe_vof=[0.476, 0.476, 0.472, 0.458, 0.442, 0.427, 0.412, 0.398, 0.385, 0.373, 0.362, 0.352, 0.343, 0.334, 0.327, 0.32, 0.314, 0.308, 0.302, 0.297, 0.292, 0.287, 0.283, 0.279, 0.274, 0.27, 0.265, 0.261, 0.257, 0.253, 0.249, 0.244, 0.24, 0.236, 0.232, 0.227, 0.222, 0.218, 0.212, 0.207, 0.201, 0.196, 0.191, 0.185, 0.179, 0.173, 0.167, 0.162, 0.156, 0.15, 0.144, 0.138, 0.132, 0.126]

time_vof = [0.0, 0.09983495867825486, 0.35878113000464906, 0.8092678802534944, 1.096912930053299, 1.31638745323102, 1.5061305150828235, 1.6768881368954642, 1.8319932473046008, 1.9669947091992745, 2.0861121086175385, 2.195807599425395, 2.2954917049539407, 2.3851471696441506, 2.46739751798765, 2.541542780734958, 2.6126210716301395, 2.678346336554838, 2.7400153019188043, 2.8005259232415614, 2.8563370469503426, 2.9132581165255127, 2.9669389600953138, 3.017736115519761, 3.0689641852011764, 3.118408687181058, 3.170426363044376, 3.2200137977085164, 3.268985485608238, 3.318345773183854, 3.366402730139647, 3.4181115935694746, 3.46768327172512, 3.518268989212308, 3.570030268651985, 3.6208628688460363, 3.675196924969777, 3.7290168830847263, 3.785516287934015, 3.845155491962343, 3.905136891763598, 3.9662263309331336, 4.0268430335042, 4.087052830768934, 4.147138845529652, 4.2065991439269235, 4.2660613239785485, 4.3249706844885, 4.383692055899824, 4.442252127018617, 4.498228475944582, 4.555279185461687, 4.611350778159313, 4.665401325726032]


#Figure
with plt.style.context(['science', 'ieee']):
    fig0 = plt.figure()
    ax0 = fig0.add_subplot(111)
    print(len(time_list))
    print(len(y_spike_list))
    print(time_list)
    print(y_spike_list)
    ax0.plot(time_list, y_spike_list, '-b*',markersize=1.5, linewidth=1, label="Pointe - Lethe CHNS")
    ax0.plot(time_vof, pointe_vof, '-k', linewidth=1, label="Pointe - Lethe VOF")
    ax0.plot(ref_time, ref_y_spike, '-r',  linewidth=1,  label="Pointe - He et al (1999)")
    
    ax0.plot(time_list, y_bubble_list, '--b*',markersize=1.5, linewidth=1, label="Bulle - Lethe CHNS")
    ax0.plot(time_vof, bulle_vof,'--k', linewidth=1, label="Bulle - Lethe VOF")
    ax0.plot(ref_time, ref_y_bubble, '--r',  linewidth=1, label="Bulle - He et al (1999)")
    ax0.set_ylabel(r'$y$ [m]')
    ax0.set_xlabel(r'Temps t$^*$ [s]')
    ax0.set_xlim([0, 4.5])
    ax0.set_ylim([0.1, 0.8])
    ax0.legend(loc="lower left",frameon=True, edgecolor='k',
               prop={'size': 5.5}, ncol=1)
    #plt.title("Spike and bubble evolution Cahn-Hilliard".format(output_path[9:-1]))
    fig0.savefig('./spike_and_bubble_evolution_oscillations_{}.png'.format(output_path[9:-1]),dpi=1000)
    fig0.savefig('./spike_and_bubble_evolution_oscillations_{}.pdf'.format(output_path[9:-1]), format="pdf",dpi=1000)

#Plot the mass of fluid along the simulation

#Functions to turn .dat data in numpy array
#Credits to Lucka Barbeau for the two functions below!
def is_number(s):
    try:
        float(s)
    except ValueError:
        return False
    return True
def read_my_data(results_path):
    force_file = open(results_path, 'r')
    list_of_list_of_vars_name = [[]];
    list_of_list_of_vars = [[]];
    fix_vars_name = False

    nb_set_of_vars = 0;
    for line in force_file.readlines():
        i = 0;
        for word in line.split():
            if is_number(word):
                fix_vars_name = True
                list_of_list_of_vars[nb_set_of_vars][i] = np.append(list_of_list_of_vars[nb_set_of_vars][i],
                                                                    float(word))
                i += 1
            else:
                if word != 'particle':
                    if fix_vars_name:
                        nb_set_of_vars += 1
                        list_of_list_of_vars_name.append([])
                        list_of_list_of_vars.append([])
                        fix_vars_name = False
                    list_of_list_of_vars_name[nb_set_of_vars].append(word)
                    list_of_list_of_vars[nb_set_of_vars].append(np.array([]))
    return list_of_list_of_vars_name, list_of_list_of_vars



