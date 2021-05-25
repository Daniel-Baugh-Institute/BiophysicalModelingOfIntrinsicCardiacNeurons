from netpyne import specs, sim
import scipy.io as sio 
import array
import numpy

try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg  # if no simConfig in parent module, import directly from cfg module

# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

## LOAD ALL CELL TYPES
# from mat file
cell_identities = = sio.loadmat('all_cellTypes.mat')['allcells_new12_unique_binary']
# allcells_new12_unique_binary= sio.loadmat('all_cellTypes.mat')
# output = allcells_new12_unique_binary['allcells_new12_unique_binary'] # array

# len(output[1]) >>> 115
# output[1:12] >>> array of 115 celltypes
# accesing cellType as (1:12, idx)>>> 
# temp = output[1:12]
# cell = temp[:, idx] # where idx  1:115  




#sortedallcells_new12_unique_binary.keys())
#allcells_new12_unique_binar['testdouble']

## Cell parameters/rules
PYRcell = {'secs': {}}
PYRcell['secs']['soma'] = {'geom': {}, 'mechs': {}}  # soma params dict
PYRcell['secs']['soma']['geom'] = {'diam': 18.8, 'L': 18.8, 'Ra': 123.0}  # soma geometry
PYRcell['secs']['soma']['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}  # soma hh mechanism
netParams.cellParams['PYR'] = PYRcell

## Population parameters
netParams.popParams['S'] = {'cellType': 'PYR', 'numCells': 20}
netParams.popParams['M'] = {'cellType': 'PYR', 'numCells': 20}

## Synaptic mechanism parameters
netParams.synMechParams['exc'] = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': cfg.synMechTau2, 'e': 0}  # excitatory synaptic mechanism

# Stimulation parameters
netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 10, 'noise': 0.5}
netParams.stimTargetParams['bkg->PYR'] = {'source': 'bkg', 'conds': {'cellType': 'PYR'}, 'weight': 0.01, 'delay': 5, 'synMech': 'exc'}

## Cell connectivity rules
netParams.connParams['S->M'] = {    #  S -> M label
    'preConds': {'pop': 'S'},       # conditions of presyn cells
    'postConds': {'pop': 'M'},      # conditions of postsyn cells
    'probability': 0.5,             # probability of connection
    'weight': cfg.connWeight,       # synaptic weight
    'delay': 5,                     # transmission delay (ms)
    'synMech': 'exc'}               # synaptic mechanism
