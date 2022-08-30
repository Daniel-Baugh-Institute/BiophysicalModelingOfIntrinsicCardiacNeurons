from netpyne import specs, sim
import numpy as np
import csv
netParams = specs.NetParams()
try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg  # if no simConfig in parent module, import directly from cfg.py:cfg

netParams.defaultThreshold = -10
# order in genemod MUST be preserved to match cell_identities channel order
genemod = {'ch_Hcn3_cp11':{'gHCN3bar': 0.01},  'ch_Hcn1_cp9':{'gHCN1bar': 0.003},
           'ch_Cacna1g_cp41':{'gCav3_1bar': 0.0003},        'ch_Cacna1a_cp5':{'gCav2_1bar': 0.00005},
           'ch_Cacna1d_md150284':{'pcaLbar': 0.00045},  'ch_Hcn4_cp12':{'gHCN4bar': 0.0035},
            'ch_Cacna1c_cp3':{'gLbar': 0.006},         'ch_Cacna1i_md279':{'gcabar': cfg.c1i},           
            'ch_Kcna1ab1_md80769':{'gbar': 0.018},        'ch_Kcnj3_md2488':{'gbar': 0.0035},           
            'ch_Cacna1b_cp6':{'gCav2_2bar': 0.0001},  'ch_Hcn2_cp10':{'gHCN2bar': 0.009},  #0.0011          
            'ch_Kcnc1_rothman':{'gbar': 0.018, 'phi':cfg.phi}, 'ch_Scn1a_cp35':{'gNabar': 0.075}  }     #0.0015

cell_identities = np.bool_(np.transpose(np.genfromtxt('red_tdata_all_15_m2l.csv', delimiter=',')))
cell = cell_identities[cfg.cellnum]

## Cell parameters/rules
CEL = {'secs': {}}

CEL['secs']['soma'] = {'geom': {'diam': cfg.sze, 'L': cfg.sze, 'Ra': 35.4, 'cm':1}, 'mechs':  {'pas' : {'g': 0.00078, 'e': -65}, 'nm_In_md149739':{'gbar':0}} } #1e-5
                                                                            

for mod,onoff in zip(genemod,cell):
    if onoff:
        CEL['secs']['soma']['mechs'][mod]=genemod[mod]
netParams.cellParams['CEL'] = CEL
netParams.popParams['U'] = {'cellType': 'CEL', 'numCells': 1}

if cfg.stim == 'IClamp':
    netParams.stimSourceParams['iclamp'] = {'type': 'IClamp', 'amp': cfg.amp, 'dur': 400, 'delay': 100} 
    netParams.stimTargetParams['iclamp->CEL'] = {'source': 'iclamp', 'conds': {'cellType': 'CEL'}, 'sec': 'soma', 'loc': 0.5}
elif cfg.stim == 'VClamp':
    netParams.stimSourceParams['vclamp'] = {'type': 'VClamp', 'dur': [100,400,500], 'amp': [cfg.hParams['v_init'],cfg.vc,cfg.hParams['v_init'] ]} 
    netParams.stimTargetParams['vclamp->CEL'] = {'source': 'vclamp', 'conds': {'cellType': 'CEL'}, 'sec': 'soma', 'loc': 0.5}


# 'ch_Kcna1ab1_md80769g':{'gbar': cfg.ka}
# 'ch_Scn1a_cp35':{'gNabar': cfg.na}
# 'ch_Scn1a_md264834':{'gNav11bar': cfg.na}
