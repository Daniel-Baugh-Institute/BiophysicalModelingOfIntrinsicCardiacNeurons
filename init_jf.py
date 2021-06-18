from imp import IMP_HOOK
from future.standard_library import install_aliases
from netpyne import sim
from neuron import h
import matplotlib.pyplot as plt


simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
# sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
sim.create(netParams=netParams, simConfig=simConfig)


def fi():
    '''set steady state RMP for 1 cell'''
    seg = sim.net.cells[0].secs.soma.hObj(0.5) # since only 1 cell with nseg=1 can jump straight to that seg
    isum = 0.0
    try:
        if seg.na_ion.is_ion() == True: 
            isum = isum + seg.ina 
    except:
        isum = isum
    try:
        if seg.k_ion.is_ion() == True:   # always has to be a K given our dataset
            isum = isum + seg.ik
    except:
        isum = isum
    try:
        if seg.ca_ion.is_ion() == True:
            isum = isum + seg.ica
    except:
        isum = isum
    try:
        if seg.other_ion.is_ion() == True:
            isum = isum + seg.iother
    except:
        isum = isum

    seg.e_pas = cfg.hParams['v_init']+isum/seg.g_pas
    print('AAAA: isum = ',isum, 'ipas = ',seg.i_pas, 'isum+ipas =',isum+seg.i_pas, 'epas = ',seg.e_pas,'v = ', seg.v)

fih = [h.FInitializeHandler(2, fi)]
sim.simulate()
sim.analyze()




