#%% Written by Doorgesh S Jokhun on 17.11.2020

# import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#%% Initial parameters

initial_pos = (3642.9, -4930.1, 5264.5)
AF_Offset = 0

pos_along_X = (-6357.1, -4930.1, 5264.5)  # Any point along the X direction. Used together with the initial position to determine the direction vector of the X-axis.
unit_displacement_X = 400 #300   # Separation between the midpoint of successive plots along the X-axis

pos_along_Y = (3642.8, 5070, 5264.5)  # Any point along the Y direction. Used together with the initial position to determine the direction vector of the Y-axis.
unit_displacement_Y = 400 #300   # Separation between the midpoint of successive plots along the Y-axis

row_offset = 0 #150    # Distance along the X-axis between the expected position of a plot and the actual position when determined relative to a plot on the previous row

series_name = 'MDA100xSR'

#%% Final conditions - Choose one only, else last_pos will be used by default!
if 'last_pos' in locals(): del last_pos
if 'num_of_Cols_n_Rows' in locals(): del num_of_Cols_n_Rows
if 'dims_of_area_X_n_Y' in locals(): del dims_of_area_X_n_Y

# last_pos = (250.32,260.10,50.05)    # Last point to image

num_of_Cols_n_Rows = (25,25)    # Number of plots to image  along X and Y axes

# dims_of_area_X_n_Y = (300.23,260.12)    # lengths along X and Y from the initial position, within which plots are to be imaged


#%%

vec_X = np.subtract(pos_along_X,initial_pos)
UnitVec_X = vec_X / np.sqrt(np.dot(vec_X,vec_X))

vec_Y = np.subtract(pos_along_Y,initial_pos)
UnitVec_Y = vec_Y / np.sqrt(np.dot(vec_Y,vec_Y))


#%%
coordinates=[]
coord_name=[]

current_pos = np.array(initial_pos)
UnitVec_X_correction = 1
if 'num_of_Cols_n_Rows' in locals():
    for row in range(num_of_Cols_n_Rows[1]):
        if row%2 == 0 : num_of_Cols = num_of_Cols_n_Rows[0]
        else: 
            if row_offset!=0: num_of_Cols = num_of_Cols_n_Rows[0]-1
        for col in range(num_of_Cols):
            if col > 0:
                current_pos = current_pos + (UnitVec_X*unit_displacement_X)
            coordinates.append(current_pos.round(2))
            coord_name.append((series_name+'_'+str(row)+','+str(col)))
        current_pos = current_pos + (UnitVec_Y*unit_displacement_Y)-(UnitVec_X_correction*UnitVec_X*row_offset)
        UnitVec_X = -UnitVec_X
        UnitVec_X_correction = -UnitVec_X_correction
coordinates = np.array(coordinates)


# %%

ax = plt.axes(projection='3d')
ax.plot3D(coordinates[:,0],coordinates[:,1],coordinates[:,2], linewidth=1, c='gray')

ax.scatter3D(coordinates[:,0],coordinates[:,1],coordinates[:,2], s=8, c=coordinates[:,2], marker='.')



#%%

header=f'"Stage Memory List", Version 6.0\n 0, 0, 0, 0, 0, 0, 0, "microns", "microns"\n 0\n{coordinates.shape[0]}\n'
with open('coordinates.stg','w') as text: 
    text.writelines(header)
    for line_count in range (coordinates.shape[0]):
        text.writelines(f'"{coord_name[line_count]}", {coordinates[line_count,0]}, {coordinates[line_count,1]}, {coordinates[line_count,2]}, {AF_Offset}, 2.5, FALSE, -9999, TRUE, TRUE, 0, -1, ""\n')

    # text.writelines(stage_pos)
        # self.pos_format = '"{pos_info}", {pos_x}, {pos_y}, {pos_z}, 0, {pos_z}, FALSE, -9999, TRUE, TRUE, 0, -1, ""\n'


# %%

# %%

# %%

# %%
