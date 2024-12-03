# -*- coding: utf-8 -*-
"""
Created in January 19, 2024

@author: mmgee
"""
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
from scAnalysis import classification, toPandas, readBatchData, readAllData
from classification_firing_sequence import classify_sequence, plotVm, classification_subplots

df = dfss = filenamepkl = None


try:
    with open('params.csv', 'r') as file:
        # If you reach this point, the file is successfully opened
        print("File 'params.csv' can be opened.")
        # You can add additional code to read or process the file if needed
except FileNotFoundError:
    print("File 'params.csv' not found.")
except IOError:
    print("Error opening the file 'params.csv'.")


# read batch data to generate _allData.json file
dataFolder = "25jan24_scn1a_-20"
batchLabel = '25jan24_scn1a_-20'
readBatchData(dataFolder, batchLabel, paramFile = 'params_15.csv', target=None, saveAll=True, vars=None, maxCombs=None, listCombs=None)

# load json file and convert to pandas dataframe
filename = '//lustre//ogunnaike//users//2420//matlab_example//ragp//batch//25jan24_scn1a_-20_allData.json'
params, data, df_20jan24 = readAllData(filename,dfonly = False)

# classify behavior and generate classification.json file that will be analyzed to determine the classification sequence 
classification(df_20jan24)

# determine classification sequence using classification_firing_sequence.py
dc = pd.read_json('//lustre//ogunnaike//users//2420//matlab_example//ragp//batch//classification.json')
#dc = dc.iloc[0:3]
# Run sequence classification
classify_sequence(dc)

# Tonic only plots
#print(dc.iloc[4:6])

idx = [0, 104, 208]#[0+59,78+59,156+59]
df = dc.loc[idx,['Vlist','t','cellnum']]
batchLabel = "T1_scn1a-20" #
plotVm(df,batchLabel,idx)
"""
df_seq_13 = pd.DataFrame(columns = ['Firing pattern','Count'])
df_seq_13['Firing pattern'] = ['Phasic', 'Tonic', 'Phasic-Tonic','Tonic-Phasic']
df_seq_13['Count'] = [40,18,16,3]

df_seq_14 = df_seq_13
df_seq_16 = df_seq_13
df_seq_17 = df_seq_13

df_seq_14['Count'] = [51, 20, 3, 1]
df_seq_16['Count'] = [40, 6, 22, 5]
df_seq_17['Count'] = [40, 6, 22, 5]



classification_subplots(df_seq_13,df_seq_14,df_seq_16,df_seq_17)

# Load JSON data from a file
with open('//lustre//ogunnaike//users//2420//matlab_example//ragp//batch//23jan24_13//23jan24_13_0_0_data.json', 'r') as file:
    json_data = json.load(file)

# If the JSON data is a dictionary, you can directly convert it to a DataFrame
df = pd.DataFrame.from_dict(json_data)

# If the JSON data is a list of dictionaries, you can still convert it to a DataFrame
# by specifying the 'orient' parameter as 'records'
# df = pd.DataFrame.from_dict(json_data, orient='records')

# Display the DataFrame
print(df.head())
print('spkt')
print(df['spkt'])
"""
