# -*- coding: utf-8 -*

# Initial parameters

# from math import ceil
from objectives import photometrics_ez

################
# Parameters
################

# objective parameters
objective = '10x'
binning = 1
overlap = 0.1

# file naming parameters
base_name = 'Port_'
port_name = 'C_EcadKO_slit'

# Values for column / row number
columns = 4
rows =1

## x,y,z coordinates 
# top left
x1 =45450
y1 =38817
z1 =-45

################
# Code to generate stg file
################
microscope = photometrics_ez(objective, binning = binning, overlap = overlap)
microscope.generate_stage_pos(x1, y1, z1, columns, rows, base_name = base_name, port_name = port_name)
