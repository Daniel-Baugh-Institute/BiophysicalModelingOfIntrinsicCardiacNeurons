# from imp import IMP_HOOK
from future.standard_library import install_aliases
from netpyne import sim
from neuron import h

simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
# sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
sim.create(netParams=netParams, simConfig=simConfig)
seg = sim.net.cells[0].secs.soma.hObj(0.5)
def fi():
    '''set steady state RMP for 1 cell'''
     # since only 1 cell with nseg=1 can jump straight to that seg
    isum = 0
    isum = (seg.ina if h.ismembrane('na_ion') else 0) + (seg.ik if h.ismembrane('k_ion') else 0) + (seg.ica if h.ismembrane('ca_ion') else 0) + (seg.iother if h.ismembrane('other_ion') else 0)
    seg.e_pas = cfg.hParams['v_init']+isum/seg.g_pas
    print('AAAA: isum = ',isum, 'ipas = ',seg.i_pas, 'isum+ipas =',isum+seg.i_pas, 'epas = ',seg.e_pas,'v = ', seg.v)

fih = [h.FInitializeHandler(2, fi)]
# sim.simulate()
# sim.analyze()




