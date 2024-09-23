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

#Take case path as argument and store it
output_path = sys.argv[1]

#Plot the volume of fluid 1 along the simulation

#def analytical_volume(t,flux,v_init):
   #return t*flux + v_init 
   
def computed_volume(t,flux,v_init):
   volume = np.empty(len(t))
   volume[0] = v_init
   for i in range(1,len(t)):
      dt = t[i]-t[i-1]
      volume[i] = (flux[i]+flux[i-1])*dt*0.5 + volume[i-1]
   print(volume)
   return volume


#Functions to turn .dat data in numpy array
#Credits to Lucka Barbeau for the two functions below !
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

list_of_list_of_vars_name,list_of_list_of_vars=read_my_data(output_path + "/phase_statistics.dat")
#list_of_list_of_vars_name_flux,list_of_list_of_vars_flux = read_my_data(output_path + "/flow_rate.dat")

#computed_volume_list = computed_volume(list_of_list_of_vars_flux[0][0],list_of_list_of_vars_flux[0][5],list_of_list_of_vars[0][6][0])
crop = 5
plt.plot(list_of_list_of_vars[0][0][crop:],list_of_list_of_vars[0][6][crop:],label="Fluid 1")
#plt.plot(list_of_list_of_vars_flux[0][0],computed_volume_list,label="Volume computed with numerical flux")
#plt.plot(list_of_list_of_vars[0][0],analytical_volume(list_of_list_of_vars[0][0],5.0e2,(2*np.pi*(0.5)**3)/3),label="Analytical volume")
plt.title("Evolution volumes of the phases")
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Volume of fluid")
#plt.ylim(37.4,37.6)
plt.savefig('./relevant_quantities.png')
plt.show()


