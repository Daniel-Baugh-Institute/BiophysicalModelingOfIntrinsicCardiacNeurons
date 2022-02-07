from netpyne import specs, sim
import numpy as np
import csv
netParams = specs.NetParams()
try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg  # if no simConfig in parent module, import directly from cfg.py:cfg

# order in genemod MUST be preserved to match cell_identities channel order
genemod = {'ch_Cacna1a_cp5':{'gCav2_1bar': cfg.c1a},  'ch_Cacna1b_cp6':{'gCav2_2bar': cfg.c1b},
           'ch_Cacna1c_cp3':{'gLbar': cfg.c1c},        'ch_Cacna1g_cp41':{'gCav3_1bar': cfg.c1g},
           'ch_Hcn1_cp9':{'gHCN1bar': cfg.h1},         'ch_Hcn2_cp10':{'gHCN2bar': cfg.h2},           
           'ch_Hcn3_cp11':{'gHCN3bar': cfg.h3},        'ch_Hcn4_cp12':{'gHCN4bar': cfg.h4},           
           'ch_kcna_232813':{'gkcnabar': cfg.kcna},        'ch_Scn1a_md264834':{'gNav11bar': cfg.na}}     #1.0    #0.015
cell_identities = np.bool_(np.transpose(np.genfromtxt('rat_10ch_unique.csv', delimiter=',')))
cell = cell_identities[cfg.cellnum]

## Cell parameters/rules
CEL = {'secs': {}}

CEL['secs']['soma'] = {'geom': {'diam': cfg.sze, 'L': cfg.sze, 'Ra': 35.4, 'cm':1}, 'mechs':  {'pas' : {'g': 1.8e-6, 'e': -65}} }
                                                                            
#KAAR_rybak; gAbar

for mod,onoff in zip(genemod,cell):
    if onoff:
        CEL['secs']['soma']['mechs'][mod]=genemod[mod]
netParams.cellParams['CEL'] = CEL
netParams.popParams['U'] = {'cellType': 'CEL', 'numCells': 1}

if cfg.stim == 'IClamp':
    netParams.stimSourceParams['iclamp'] = {'type': 'IClamp', 'amp': cfg.amp, 'dur': 500, 'delay': 100} 
    netParams.stimTargetParams['iclamp->CEL'] = {'source': 'iclamp', 'conds': {'cellType': 'CEL'}, 'sec': 'soma', 'loc': 0.5}

