from netpyne import specs, sim
import numpy as np
import csv
import pandas as pd
netParams = specs.NetParams()

try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg  # if no simConfig in parent module, import directly from cfg.py:cfg

# order in genemod MUST be preserved to match cell_identities channel order
genemod = {'ch_Cacna1a_cp5':{'gCav2_1bar': 0.00001},  'ch_Cacna1b_cp6':{'gCav2_2bar': 0.0001},
           'ch_Cacna1c_cp3':{'gLbar': 0.0001},        'ch_Cacna1g_cp41':{'gCav3_1bar': 0.00001},
           'ch_Cacna1i_md279':{'gcabar': 0.00015},  'ch_Hcn1_cp9':{'gHCN1bar': 0.00001},         #pcabar =.2e-3; 'gCav3_3bar': 0.0001
           'ch_Hcn2_cp10':{'gHCN2bar': 0.003},           'ch_Hcn3_cp11':{'gHCN3bar': 0.0001},    
           'ch_Hcn4_cp12':{'gHCN4bar': 0.0001},           'ch_Kcna1ab1_md80769':{'gbar': 0.015},   
           'ch_Kcnc1_md74298':{'gk': 0.015},            'ch_Scn1a_md264834':{'gNav11bar': 1.0}}
cell_identities = np.bool_(np.transpose(np.genfromtxt('allcells_new12_unique_binary.csv', delimiter=',')))
cell = cell_identities[cfg.cellnum]

ctr = 0 
df_chcond = pd.read_csv('ionch_cond_allcells_Naf_05.csv',sep = ',',header=None) # ionch_cond_allcells_Naf01.csv
                                                                        # ionch_cond_allcells.csv

## Cell parameters/rules
CEL = {'secs': {}}
CEL['secs']['soma'] = {'geom': {'diam': 30, 'L': 30, 'Ra': 35.4, 'cm':1}, 'mechs': {'pas' : {'g': 1.8e-6, 'e': -65}}}

for mod,onoff in zip(genemod,cell):
    if onoff:
        for i in genemod[mod]: genemod[mod][i] = df_chcond.iloc[cfg.cellnum][ctr]
        ctr+=1
        print('ctr='+ str(ctr))
        CEL['secs']['soma']['mechs'][mod]=genemod[mod]
netParams.cellParams['CEL'] = CEL
netParams.popParams['U'] = {'cellType': 'CEL', 'numCells': 1}

if cfg.stim == 'IClamp':
    netParams.stimSourceParams['iclamp'] = {'type': 'IClamp', 'amp': cfg.amp, 'dur': 300, 'delay': 50} 
    netParams.stimTargetParams['iclamp->CEL'] = {'source': 'iclamp', 'conds': {'cellType': 'CEL'}, 'sec': 'soma', 'loc': 0.5}
