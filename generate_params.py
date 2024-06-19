# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 15:10:17 2024

@author: mmgee
"""

# this code generates all combinations of parameters
"""
import csv
params = [['amp', 'cellnum']]
for amp in [0.1, 0.3, 0.5]:
    for cellnum in range(104): #78,86,114, 122 321
        params.append([amp,cellnum])
with open('params.csv', 'w') as f:
    wr = csv.writer(f)
    wr.writerows(params)
"""


# this code generates Sobol sampled parameter sets
import csv
from sobol_seq import sobol_seq

# Define the number of parameters
num_parameters = 14

# Define the number of parameter sets
numSamples = 100
numCells = 104

# Define the minimum and maximum bounds for each parameter
# parameters: ['Scn1a','Kcna1+ab','Kcnc1','Kcnj3','Cacna1a','Cacna1b','Cacna1c','Cacna1d','Cacna1g','Cacna1i','Hcn1','Hcn2','Hcn3','Hcn4']

min_bounds = [0.075,1.8e-2, 1.8e-2, 3.5e-3, 3e-3, 9e-3, 1e-2, 3.5e-3, 6e-4, 3e-4,4.5e-4,6e-3,1e-4,5e-5]
#[1.67e-6, 1.8e-3, 1.8e-3, 1.67e-4, 1.67e-6, 1.67e-6, 1.67e-6, 2.8e-7, 1.67e-6, 3.3e-5,1.67e-6,1.67e-6,1.67e-6,1.67e-6]  # Minimum bounds for each parameter
max_bounds =  [6e-1,0.066,0.066,0.006, 6e-3, 6e-2, 6e-2, 4e-3, 6e-4, 1.2e-3, 6e-4,7e-3,6e-4,6e-5] 
#[6e-5,0.066,0.066,0.006, 6e-5, 6e-5, 6e-5, 1e-6, 6e-5, 1.2e-3, 6e-5,6e-5,6e-5,6e-5,]  # Maximum bounds for each parameter

# Generate Sobol sequence within given bounds
sobol_samples = sobol_seq.i4_sobol_generate(num_parameters, numSamples)

# Scale the Sobol sequence to match the specified bounds
scaled_samples = []
for i in range(num_parameters):
    scaled_samples.append(min_bounds[i] + sobol_samples[:, i] * (max_bounds[i] - min_bounds[i]))

# Transpose the list to get parameter sets in rows
params = list(zip(*scaled_samples))

params_with_cellnum = params.append(params,numCells) #[[i // numCells] + list(params[i]) for i in range(numSamples * numCells)]


# Write parameter sets to CSV file
with open('params.csv', 'w', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(['cellnum','Scn1a','Kcna1+ab','Kcnc1','Kcnj3','Cacna1a','Cacna1b','Cacna1c','Cacna1d','Cacna1g','Cacna1i','Hcn1','Hcn2','Hcn3','Hcn4'])
    wr.writerows(params_with_cellnum)
