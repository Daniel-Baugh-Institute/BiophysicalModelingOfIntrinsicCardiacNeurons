from netpyne import specs, sim

try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg_IClamp import cfg  # if no simConfig in parent module, import directly from tut8_cfg module

# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

## Cell parameters/rules
cell_12_1 = {'secs': {}}
cell_12_1['secs']['soma'] = {'geom': {}, 'mechs': {}}  # soma params dict
cell_12_1['secs']['soma']['geom'] = {'diam': 30, 'L': 30, 'cm': 1, 'nseg':1}  # soma geometry
cell_12_1['secs']['soma']['mechs']['pas'] = {'gl': 1.8e-6, 'el': -65}

## HERE >>> hardcode 12 -- SET ALL GMAX TO SAME VALUE
#PYRcell['secs']['soma']['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}  # soma hh mechanism
##NA##
cell_12_1['secs']['soma']['mechs']['ch_Scn1a_md264834'] = {'gNav11bar':1.0}
##K##
cell_12_1['secs']['soma']['mgit aechs']['ch_Kcna1ab1_md80769'] = {'gbar': 0.015}
cell_12_1['secs']['soma']['mechs']['ch_Kcnc1_md74298'] = {'gk': 0.1}  #0.015
##CA ghk()##
cell_12_1['secs']['soma']['mechs']['ch_Cacna1a_cp5'] = {'gCav2_1bar': 1e-5}
cell_12_1['secs']['soma']['mechs']['ch_Cacna1b_cp6'] = {'gCav2_2bar': 1e-4}
cell_12_1['secs']['soma']['mechs']['ch_Cacna1c_cp3'] = {'gLbar': 1e-5}
cell_12_1['secs']['soma']['mechs']['ch_Cacna1g_cp41'] = {'gCav3_1bar':1e-5}
cell_12_1['secs']['soma']['mechs']['ch_Cacna1i_cp42'] = {'gCav3_3bar':1e-5}
##HCN##
cell_12_1['secs']['soma']['mechs']['ch_Hcn1_cp9'] = {'gHCN1bar':  0.0001}
cell_12_1['secs']['soma']['mechs']['ch_Hcn2_cp10'] = {'gHCN2bar': 0.0001}
cell_12_1['secs']['soma']['mechs']['ch_Hcn3_cp11'] = {'gHCN3bar': 0.0001 }
cell_12_1['secs']['soma']['mechs']['ch_Hcn4_cp12'] = {'gHCN4bar': 0.001}

netParams.cellParams['cellType'] = cell_12_1

## Population parameters
netParams.popParams['cell'] = {'cellType': 'cell_12_1', 'numCells': 1}
#netParams.popParams['M'] = {'cellType': 'PYR', 'numCells': 20}

## Synaptic mechanism parameters
#netParams.synMechParams['exc'] = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': cfg.synMechTau2, 'e': 0}  # excitatory synaptic mechanism
#netParams.synMechParams['inh'] = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': cfg.synMechTau2, 'e': -80}  # excitatory synaptic mechanism

# Stimulation parameters
# netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 10, 'noise': 0.5}
# netParams.stimTargetParams['bkg->PYR'] = {'source': 'bkg', 'conds': {'cellType': 'PYR'}, 'weight': 0.01, 'delay': 5, 'synMech': 'exc'}

## Cell connectivity rules
#netParams.connParams['S->M'] = {    #  S -> M label
#    'preConds': {'pop': 'S'},       # conditions of presyn cells
#    'postConds': {'pop': 'M'},      # conditions of postsyn cells
#    'probability': 0.5,             # probability of connection
#    'weight': cfg.connWeight,       # synaptic weight
#    'delay': 5,                     # transmission delay (ms)
#    'synMech': 'exc'}               # synaptic mechanism

#------------------------------------------------------------------------------
# Synaptic mechanism parameters
#------------------------------------------------------------------------------
# # excitatory synapses
# netParams.synMechParams['NMDA']             = {'mod': 'MyExp2SynNMDABB',    'tau1NMDA': 15, 'tau2NMDA': 150,                'e': 0}
# netParams.synMechParams['AMPA']             = {'mod': 'MyExp2SynBB',        'tau1': 0.05,   'tau2': 5.3,                    'e': 0}
# # inhibitory synapses
# netParams.synMechParams['GABAB']            = {'mod': 'MyExp2SynBB',        'tau1': 3.5,    'tau2': 260.9,                  'e': -93} 
# netParams.synMechParams['GABAA']            = {'mod': 'MyExp2SynBB',        'tau1': 0.07,   'tau2': 18.2,                   'e': -80}
# netParams.synMechParams['GABAASlow']        = {'mod': 'MyExp2SynBB',        'tau1': 2,      'tau2': 100,                    'e': -80}
# netParams.synMechParams['GABAASlowSlow']    = {'mod': 'MyExp2SynBB',        'tau1': 200,    'tau2': 400,                    'e': -80}

#ESynMech    = ['exc']
#SOMESynMech = ['inh']
#SOMISynMech = ['inh']
#PVSynMech   = ['inh']
#NGFSynMech  = ['inh']

#------------------------------------------------------------------------------
# Current inputs (IClamp)
#------------------------------------------------------------------------------
if cfg.addIClamp:
    for key in [k for k in dir(cfg) if k.startswith('IClamp')]:
        params = getattr(cfg, key, None)
        [pop,sec,loc,start,dur,amp] = [params[s] for s in ['pop','sec','loc','start','dur','amp']]

        # cfg.analysis['plotTraces']['include'].append((pop,0))  # record that pop

        # add stim source
        # netParams.stimSourceParams[key] = {'type': 'IClamp', 'delay': start, 'dur': dur, 'amp': amp}
        netParams.stimSourceParams[key] = { 'type': 'IClamp', 
                                            'delay': cfg.startStimTime if cfg.startStimTime is not None else start, 
                                            'dur': cfg.stimDur if cfg.stimDur is not None else dur, 
                                            'amp': cfg.clampAmplitude if cfg.clampAmplitude is not None else amp}
        
        # connect stim source to target
        netParams.stimTargetParams[key+'_'+pop] =  {
            'source': key, 
            'conds': {'pop': pop},
            'sec': sec, 
            'loc': loc}

if cfg.addPreIClamp:
    for key in [k for k in dir(cfg) if k.startswith('PreIClamp')]:
        params = getattr(cfg, key, None)
        [pop,sec,loc,start,dur,amp] = [params[s] for s in ['pop','sec','loc','start','dur','amp']]

        # cfg.analysis['plotTraces']['include'].append((pop,0))  # record that pop

        # add stim source
        # netParams.stimSourceParams[key] = {'type': 'IClamp', 'delay': start, 'dur': dur, 'amp': amp}
        netParams.stimSourceParams[key] = { 'type': 'IClamp', 
                                            'delay': start, 
                                            'dur': cfg.stimDur_pre if cfg.stimDur_pre is not None else dur, 
                                            'amp': cfg.clampAmplitude_pre if cfg.clampAmplitude_pre is not None else amp}
        
        # connect stim source to target
        netParams.stimTargetParams[key+'_'+pop] =  {
            'source': key, 
            'conds': {'pop': pop},
            'sec': sec, 
            'loc': loc}