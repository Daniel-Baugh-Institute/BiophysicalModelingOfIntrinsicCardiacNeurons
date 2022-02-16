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
chcond = np.genfromtxt('all_ionch_condcells.csv', delimiter=',')

## Cell parameters/rules
CEL = {'secs': 
       {'soma': 
        {'geom': {'diam': 30, 'L': 30, 'Ra': 35.4, 'cm':1}, 
         'mechs': {'pas' : {'g': 1.8e-6, 'e': -65}}}}}
CEL['secs']['soma']['mechs'].update({mod : {list(val)[0]: gmax} for (mod, val),gmax in zip(genemod.items(), chcond[cfg.cellnum]) if gmax>0})
netParams.cellParams['CEL'] = CEL
netParams.popParams['U'] = {'cellType': 'CEL', 'numCells': 1}

if cfg.stim == 'IClamp':
    netParams.stimSourceParams['iclamp'] = {'type': 'IClamp', 'amp': cfg.amp, 'dur': 500, 'delay': 100} 
    netParams.stimTargetParams['iclamp->CEL'] = {'source': 'iclamp', 'conds': {'cellType': 'CEL'}, 'sec': 'soma', 'loc': 0.5}
elif cfg.stim == 'exp2syn':
    netParams.synMechParams['exc'] = {'mod': 'Exp2Syn', 'tau1': cfg.tau1, 'tau2': cfg.tau2, 'e': cfg.e}
    netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': cfg.rate, 'noise': cfg.noise}
    netParams.stimTargetParams['bkg->exc'] = {'source': 'bkg', 'conds': {'cellType': 'CEL'}, 'weight': cfg.weight, 'delay': cfg.delay, 'synMech': 'exc'}
elif cfg.stim == 'expsyn':
    netParams.synMechParams['exc'] = {'mod': 'ExpSyn', 'tau': cfg.tau1, 'e': cfg.e}
    netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': cfg.rate, 'noise': cfg.noise}
    netParams.stimTargetParams['bkg->exc'] = {'source': 'bkg', 'conds': {'cellType': 'CEL'}, 'weight': cfg.weight, 'delay': cfg.delay, 'synMech': 'exc'}
elif cfg.stim ==  'fdexp2syn':
    netParams.synMechParams['exc'] = {'mod': 'FDSExp2Syn', 'tau1': cfg.tau1,
                                      'tau2' : cfg.tau2, 'e': cfg.e,
                                      'f' : cfg.f, 'd1': cfg.d1,
                                      'd2': cfg.d2, 'tau_F': cfg.tau_F,
                                      'tau_D1' : cfg.tau_D1,
                                      'tau_D2': cfg.tau_D2}
    netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': cfg.rate, 'noise': cfg.noise}
    netParams.stimTargetParams['bkg->exc'] = {'source': 'bkg', 'conds': {'cellType': 'CEL'}, 'weight': cfg.weight, 'delay': cfg.delay, 'synMech': 'exc'}
elif cfg.stim == 'dexp2syn':
    netParams.synMechParams['exc'] = {'mod': 'DExp2Syn', 'tau1': cfg.tau1,
                                      'tau2' : cfg.tau2, 'e': cfg.e,
                                      'd': cfg.d, 'rrate': cfg.rrate}
    netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': cfg.rate, 'noise': cfg.noise}
    netParams.stimTargetParams['bkg->exc'] = {'source': 'bkg', 'conds': {'cellType': 'CEL'}, 'weight': cfg.weight, 'delay': cfg.delay, 'synMech': 'exc'}
if cfg.hyp != 0:
    netParams.stimSourceParams['iclamp'] = {'type': 'IClamp', 'amp': cfg.hyp, 'dur': 1e9, 'delay': 0.025}
    netParams.stimTargetParams['iclamp->CEL'] = {'source': 'iclamp', 'conds': {'cellType': 'CEL'}, 'sec': 'soma', 'loc': 0.5}

