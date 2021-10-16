from netpyne import sim
from neuron import h
import csv

simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams_A.py')
# sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
sim.create(netParams=netParams, simConfig=simConfig)

seg = sim.net.cells[0].secs.soma.hObj(0.5) # since only 1 cell with nseg=1 can jump straight to that seg
# elist = []

def fi():
    '''set steady state RMP for 1 cell'''
    isum = 0
    isum = (seg.ina if h.ismembrane('na_ion') else 0) + (seg.ik if h.ismembrane('k_ion') else 0) + (seg.ica if h.ismembrane('ca_ion') else 0) + (seg.iother if h.ismembrane('other_ion') else 0)
    seg.e_pas = cfg.hParams['v_init']+isum/seg.g_pas

fih = [h.FInitializeHandler(2, fi)]
print('SSSSSSSSSSSSSSSSIM before simulate')
sim.simulate()
print('AAAAAAAAAAAAAAAASIM after simulate')
sim.analyze()
h.quit()


