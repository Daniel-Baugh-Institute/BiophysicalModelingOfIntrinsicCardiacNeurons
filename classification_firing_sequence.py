# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 17:17:01 2023

@author: mmgee 
"""


import pandas as pd
import numpy as np
import plotly_express as px
from os import makedirs
import re
from collections import OrderedDict
from itertools import product
import plotly.graph_objects as go
import plotly_express as px
import plotly.io as pio
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib_scalebar.scalebar import ScaleBar

# Function to plot time vs voltage curves
def plotVm(df,batchLabel):
    makedirs('vmPlots')
    font = 15
    f, ax = plt.subplots()
    plt.axis("off")
    offset = 0
    for indx in [0,49,50]: #df.index:
        y = df['Vlist'][indx]
        y = np.array(y)
        y = 3*(offset)+y # add offset for ease of viewing
        x = df['t'][indx]
        x = np.array(x)
        x = 25*(offset) + x #add offset
        plt.plot(x,y,linewidth=1.5)
        offset = offset + 1
    plt.hlines(-20.0,900,1000,label='100 ms',colors=['black'])
    plt.vlines(900.0,-20,-10,label="10 mV",colors=['black'])
    plt.text(865,-25,'100 ms',fontsize=font)
    plt.text(725,-18,'10 mV',fontsize=font)
    plt.title(f"Tonic, Neuronal-Type ID: T{df['cellnum'][indx]+1}", fontsize=font)
    plt.tick_params(axis='both',labelsize=font)
    plt.legend(['0.1','0.3','0.5'])
    plt.savefig(f"vmPlots/{batchLabel}.png",dpi=300,bbox_inches='tight')
    plt.close()
    return

# Produces bar chart of firing sequences vs counts
def classify_sequence(dc):
    dc['pbt'] = dc.apply(lambda x: 
                            0 if x['Phasic'] == 1 
                            else (1 if x['Burst'] == 1 
                                else (2 if x['Tonic'] == 1 
                                        else (3 if x['Subthreshold'] == 1 
                                            else 4))), 
                        axis=1)

    dc["pbt_list"] = "" # create a new column "pbt_seq" and initialize it with empty strings
    temp_list = []

    dc = dc.reset_index(drop=True)
    for index, row in dc.iterrows():
        if index == 0:
            temp_list.append(dc.loc[index,"pbt"])
            dc.loc[index, 'pbt_list'] = temp_list
        elif (row["cellnum"] == dc.iloc[index-1]["cellnum"]) and (row["na"] == dc.iloc[index-1]["na"]):
            temp_list.append(dc.loc[index, "pbt"])
            dc.at[index, 'pbt_list'] = temp_list
        else:
            temp_list = []
            temp_list.append(dc.loc[index, "pbt"])
            dc.at[index, 'pbt_list'] = temp_list
            
    dc.at[len(dc)-1, "pbt_list"] = temp_list # last value in the temp_list
    a = dc['pbt_list']



    num_rows = dc.shape[0]/5
    num_rows = int(num_rows)
    shape = [num_rows, 1]  # shape of the array
    seq_cat = np.empty(shape)
    df_temp = pd.DataFrame(columns=['rseq'])
    # print out indice for example firing sequence
    index_t = 0
    index_p = 0
    index_pt = 0
    index_tp = 0
    index_tb = 0
    # keep track of indices for each firing sequence
    tb_idx = []
    ptb_idx = []
    pbtb_idx = []
    pbp_idx = []
    pb_idx = []
    tbp_idx = []
    ptp_idx = []
    bp_idx = []
    ptbt_idx = []

    for index in range(num_rows):
        # loop through sections of 5 (for each of the 5 input stimulus) and make new array with sequence of firing patterns
        seq = np.array(dc.iloc[5*index:5*index+5]['pbt'])

        # Remove consecutive duplicates and assign to new array, rseq
        rseq = []
        for i in seq:
            if len(rseq) == 0 or i != rseq[-1]:
                rseq.append(i)
        
        rseq = np.array([rseq])
        df_temp.at[index,'rseq'] = rseq

        # Classify rseq into categories: 'Phasic', 'PB', 'PBP', 'PBT','PBTP', 'PBTB','Phasic-Tonic','PTB','PTP','PTBT','BP','Tonic','Tonic-Phasic','TB','TBP','SP','Other'
        if rseq.size == 0:
            print('Uh oh, rseq is empty!')
        elif 4 in rseq:
            seq_cat[index] = 16
            print('Post-stimulus firing, Block, or incomplete repolarisation occured')
        elif rseq.size == 1:
            if rseq[0][0] == 0: #p
                seq_cat[index] = 0
                if index_p == 0:
                    print('P')
                    print(index*5)
                    index_p = index_p + 1
            elif rseq[0][0] == 2: #t
                seq_cat[index] = 11
                if index_t == 0:
                    print('T')
                    print(index*5)
                    index_t = index_t + 1
            else:
                print('No category at')
                print(index)
        elif rseq[0][0] == 1: #bp
            seq_cat[index] = 10
            bp_idx.append(index*5)
        elif rseq[0][0] == 3: #sp
            seq_cat[index] = 15
        elif rseq[0][0] == 2: # starts with tonic, but not tonic only
            if rseq[0][1] == 0 and rseq.size == 2: # tp
                seq_cat[index] = 12
                if index_tp == 0:
                    print('TP')
                    print(index*5)
                    index_tp = index_tp + 1
            elif rseq.size == 2: # tb
                seq_cat[index] = 13
                print('TB')
                tb_idx.append(index*5)
                index_tb = index_tb + 1
            elif rseq.size == 3: # tbp
                seq_cat[index] = 14
                tbp_idx.append(index*5)
            else:
                print('No category at')
                print(index)
        else: # starts with phasic, but not phasic only
            if rseq.size == 2:
                if rseq[0][1] == 1: # pb
                    seq_cat[index] = 1
                    pb_idx.append(index*5)
                elif rseq[0][1] == 2: # pt
                    seq_cat[index] = 6
                    if index_pt == 0:
                        print('PT')
                        print(index*5)
                        index_pt = index_pt + 1
                else:
                    print('No category at')
                    print(index)
            elif rseq.size == 3:
                if rseq[0][1] == 1:
                    if rseq[0][2] == 0: # pbp
                        seq_cat[index] = 2
                        pbp_idx.append(index*5)
                    elif rseq[0][2] == 2: # pbt
                        seq_cat[index] = 7
                    else:
                        print('No category at')
                        print(index)
                else:
                    if rseq[0][2] == 0: #ptp
                        seq_cat[index] = 8
                    elif rseq[0][2] == 1: # ptb
                        seq_cat[index] = 7
                        #ptb_idx.append(index*5)
                    else:
                        print('No category at')
                        print(index)
            else:
                if rseq[0][2] == 1: #ptbt
                    seq_cat[index] = 9
                    ptbt_idx.append(index*5)
                elif rseq[0][3] == 1: # pbtb
                    seq_cat[index] = 5
                    pbtb_idx.append(index*5)
                elif rseq[0][3] == 2: #pbtp
                    seq_cat[index] = 4   
                else: 
                    print('No category at')
                    print(index) 
   

    # make new dataframe with the count of each firing pattern
    df_seq = pd.DataFrame(columns = ['Firing pattern','Count'])
    df_seq['Firing pattern'] = ['Phasic', 'PB', 'PBP', 'PBT','PBTP', 'PBTB','Phasic-Tonic','PTB','PTP','PTBT','BP','Tonic','Tonic-Phasic','TB','TBP','SP','Other']

    # count number of each firing sequence
    firing_behavior = range(0,17)
    count_col = []
    for index in range(len(firing_behavior)):
        count = np.count_nonzero(seq_cat == index)
        count_col.append(count)

    print(count_col)
    df_seq['Count'] = count_col
    df_seq = df_seq[df_seq['Count'] > 40] # Change this threshold to plot only commonly occuring firing sequences
    df_seq = df_seq.sort_values(by = 'Count',ascending=False)
    df_seq = df_seq.drop([16]) # drop block firing types (there are 63 of them)
    print("Dataframe size:", df_seq.shape)
    df_seq.to_json('df_seq.json')

    # Plot bar chart
    fig = px.bar(df_seq,x='Firing pattern',y='Count')
    fig.update_layout(
        font=dict(
            size=18
        )
    )
    fig.write_image("firing_bar.png")
    fig.show()
    return

# load data
dc = pd.read_json("classification_test.json")

# Run sequence classification
classify_sequence(dc)

makedirs('vmPlots')
# Phasic only plots
# print(dc.head(5)) # Row numbers for example voltage traces are printed out in the script. To determine the indices of those row numbers, uncomment this line to print them out
idx = [1, 833,1665]
df = dc.loc[idx,['Vlist','t','cellnum']]
batchLabel = "Phasic" #
plotVm(df,batchLabel,idx)

# Tonic only plots
#print(dc.iloc[2000:2006])
idx = [201,1033,1865]
df = dc.loc[idx,['Vlist','t','cellnum']]
batchLabel = "Tonic" #
plotVm(df,batchLabel,idx)

# Phasic-tonic plots
#print(dc.head(15))
idx = [6241,7073,7905]
df = dc.loc[idx,['Vlist','t','cellnum']]
batchLabel = "Phasic-Tonic" #
plotVm(df,batchLabel,idx)

# Tonic-phasic
#print(dc.iloc[1990:1996])
idx = [10597,11429,12261]
df = dc.loc[idx,['Vlist','t','cellnum']]
batchLabel = "Tonic-Phasic" #
plotVm(df,batchLabel,idx)


