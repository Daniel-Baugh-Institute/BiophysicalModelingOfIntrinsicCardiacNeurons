import json
import pickle
import pandas as pd
import numpy as np
import os,sys
from os import makedirs
import re
from collections import OrderedDict
from itertools import product
import plotly.graph_objects as go
import plotly_express as px
import plotly.io as pio
import matplotlib.pyplot as plt
import scipy.optimize as opt
from plotly.subplots import make_subplots
from scAnalysis import readBatchData, readAllData, plotRheobase, plotRin, plotEpas, plotRmp, plotFiringRate
import efel
import seaborn as sns

# Create _allData.json file
dataFolder = '12jun24'
batchLabel = '12jun24'
readBatchData(dataFolder, batchLabel, paramFile = 'params.csv', target=None, saveAll=True, vars=None, maxCombs=None, listCombs=None)

# load _allData.json file
filename = '12jun24_allData.json'
[params, data, df] = readAllData(filename, dfonly=False) # if dfonly = True it returns an orderedDict for some reason


# Analyze data in _allData.json
"""
Analyze outputs based on rheobase, rmp, rin, firing rate, reversal potential
5. Filter parameter sets with acceptable outputs

	Criteria
	a. rheobase: [119-751], 435 ± 161 pA, n = 29 (Tompkins 2024, mean+/-SD). Suri: 0.02 - 0.08 nA (Lizot et al., 2022
	b. rmp:near [-73- - 43] (combined).  −58 +/- 7  mV, n =29 (Hanna et al., 2021, mean+/-SD), -58 ± 8 mV (Tompkins 2024)
	c. rin: [42 154], mean = 98 (combined). 95 +/- 54 Mohm (Hanna). 101 ± 58 MΩ (Tompkins). Suri had: 40 - 300 MΩ(Hanna et al., 2021; Edwards et al., 1995; Harper and Adams, 2021; Selyanko, 1992)
	d. firing rate: Tompkins saw only phasic (<4 spikes) unless SK channels blocked. Suri: 0.5 - 60 Hz outside of bursts when stimulated (Harper and Adams, 2021; Vaseghi et al., 2017)
	e. leak reversal potential: Not reported... Suri: −80 - −50 mV, corresponding to a range between EK and Eh
	f. AHP amplitude: -[5.3-17.3], 11.3 ± 3 mV (Tompkins)
	g. AHP duration: 62 ± 11 ms
	h. AP1/2 width:
	i. AP amplitude:
6. Analyze variation in parameter values: clustering analysis, plot ranges of acceptable parameter values, see Marder and Taylor 2013 papers for examples
"""

# Rheobase
d_rheo = plotRheobase(df)

# Rin
d_rin = plotRin(df=df)

# Rmp
d_rmp = plotRmp(df,data)

# Add metrics to dataframe
df['rheo'] = d_rheo['rheo']
df['rin'] = d_rin['ripk']
df['rmp'] = d_rmp['Vrmp']

# filter based on criteria
rheo_min, rheo_max = 0.119, 0.751 #nA
rin_min, rin_max = -152, -42
rmp_min, rmp_max = -73, -43

# Create the mask columns
df['rheo_mask'] = df['rheo'].apply(lambda x: 1 if rheo_min <= x <= rheo_max else 0)
df['ripk_mask'] = df['rin'].apply(lambda x: 1 if rin_min <= x <= rin_max else 0)
df['rmp_mask'] = df['rmp'].apply(lambda x: 1 if rmp_min <= x <= rmp_max else 0)

# Add the 'accepted' column for parameter sets that meet all criteria
df['accepted'] = ((df['rheo_mask'] == 1) & (df['ripk_mask'] == 1) & (df['rmp_mask'] == 1)).astype(int)


print('test mask')
print(df.head(10))
print(df['rheo'].head(10))
print(df['rin'].head(10))
print(df['accepted'].head(10))

# Save the DataFrame to a JSON file
json_file_path = 'filtered_data.json'
df.to_json(json_file_path, orient='records', lines=True)

# formatting for plotting
df['plot'] = df['rmp_mask'].apply(lambda x:1 if x> 100000 else 1)

# Firing rate
df_ff = plotFiringRate(data,df)


# Epas (reversal potential)
# plotEpas(df = df)

# Plot violin plots with points of accepted models overlaid to compare to plots by Tompkins
# Set up the plot

def plotViolin(filename,varname,ylabel):

    plt.figure(figsize=(10, 6))

    # Plot rheo values where accepted is 0 (background)
    #sns.scatterplot(data=df[df['accepted'] == 0], x='plot', y=varname, color='gray', label='Not Accepted', s=100, alpha=0.6)

    # Plot violin plot for rheo values where accepted is 1
    sns.violinplot(data=df[df['accepted'] == 1], x='plot', y=varname, inner=None, color='skyblue')


    # Plot rheo values where accepted is 0 (background)
    sns.swarmplot(data=df[df['accepted'] == 0], x='plot', y=varname, color='gray', label='Not Accepted', s=5, alpha=0.6)


    # Overlay scatter plot for rheo values where accepted is 1
    sns.swarmplot(data=df[df['accepted'] == 1], x='plot', y=varname, color='red', label='Accepted', s=10)


    # Calculate mean and quartiles for the accepted values
    accepted_values = df[df['accepted'] == 1][varname]
    mean_val = accepted_values.mean()
    q1_val = accepted_values.quantile(0.25)
    q3_val = accepted_values.quantile(0.75)

    # Draw dotted lines for mean, 1st quartile, and 3rd quartile
    plt.axhline(mean_val, color='black', linestyle='--', linewidth=0.75)
    plt.axhline(q1_val, color='black', linestyle='--', linewidth=0.75)
    plt.axhline(q3_val, color='black', linestyle='--', linewidth=0.75)

    # Customize the plot
    fs = 18
    plt.xlabel('', fontsize=fs)
    plt.ylabel(ylabel, fontsize=fs)
    #plt.title('Rheobase (rheo) Distribution by Acceptance', fontsize=fs)
    plt.xticks(ticks=[], labels=[], fontsize=fs)
    plt.yticks(fontsize=fs)
    plt.legend(fontsize=fs)
    plt.grid(False)

    # Show the plot
    plt.tight_layout()
    plt.savefig(filename, format='png', dpi=300)
    return

filename = 'plot_rheobase_violin.png'
varname = 'rheo'
ylabel = 'Rheobase (nA)'
plotViolin(filename,varname,ylabel)

filename = 'plot_rin_violin.png'
varname = 'rin'
ylabel = 'Input impedance (MΩ)'
plotViolin(filename,varname,ylabel)

filename = 'plot_rmp_violin.png'
varname = 'rmp'
ylabel = 'Resting membrane potential (mV)'
plotViolin(filename,varname,ylabel)

# Classify as phasic, tonic, etc as Tompkins has
# plot traces of representative voltage curves
