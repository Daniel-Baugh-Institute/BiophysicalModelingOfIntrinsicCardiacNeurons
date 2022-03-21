from netpyne import specs, sim
import numpy as np
import csv
netParams = specs.NetParams()
try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg  # if no simConfig in parent module, import directly from cfg.py:cfg

# order in genemod MUST be preserved to match cell_identities channel order
genemod = {'ch_Cacna1a_cp5':{'gCav2_1bar': 0.00001},  'ch_Cacna1b_cp6':{'gCav2_2bar': 0.0001},
           'ch_Cacna1c_cp3':{'gLbar': 0.0001},        'ch_Cacna1d_md150284':{'pcaLbar': 1.7e-4},
           'ch_Cacna1g_cp41':{'gCav3_1bar': 0.00001},  'ch_Cacna1i_md279':{'gcabar': 0.00027},
            'ch_Hcn1_cp9':{'gHCN1bar': 0.00001},         'ch_Hcn2_cp10':{'gHCN2bar': 0.009},           
            'ch_Hcn3_cp11':{'gHCN3bar': 0.0001},        'ch_Hcn4_cp12':{'gHCN4bar': 0.0002},           
            'ch_Kcna1_rothman':{'gbar': 0.011,'zeta':0.5},  'ch_Kcnc1_rothman':{'gbar': 0.011, 'phi':0.85},            
            'ch_Kcnj3_md2488':{'gbar': 0},                 'ch_Scn1a_md264834':{'gNav11bar': 1}}     
# cell_identities = np.bool_(np.transpose(np.genfromtxt('red_nsp_15_pig.csv', delimiter=',')))
cell_identities = np.bool_(np.transpose(np.genfromtxt('red_nsp_NA_pig.csv', delimiter=',')))
# cell_identities = np.bool_(np.transpose(np.genfromtxt('red_sp_15_pig.csv', delimiter=',')))
# cell_identities = np.bool_(np.transpose(np.genfromtxt('red_sp_NA_pig.csv', delimiter=',')))
cell = cell_identities[cfg.cellnum]

## Cell parameters/rules
CEL = {'secs': {}}

CEL['secs']['soma'] = {'geom': {'diam': cfg.sze, 'L': cfg.sze, 'Ra': 35.4, 'cm':1}, 'mechs':  {'pas' : {'g': 1.8e-6, 'e': -65}, 'nm_In_md149739':{'gbar':0}} } #1e-3
                                                                            
#KAAR_rybak; gAbar

for mod,onoff in zip(genemod,cell):
    if onoff:
        CEL['secs']['soma']['mechs'][mod]=genemod[mod]
netParams.cellParams['CEL'] = CEL
netParams.popParams['U'] = {'cellType': 'CEL', 'numCells': 1}

if cfg.stim == 'IClamp':
    netParams.stimSourceParams['iclamp'] = {'type': 'IClamp', 'amp': 0, 'dur': 0, 'delay': 0} 
    netParams.stimTargetParams['iclamp->CEL'] = {'source': 'iclamp', 'conds': {'cellType': 'CEL'}, 'sec': 'soma', 'loc': 0.5}

