from netpyne import sim
from neuron import h
import csv, sys

# elist = []

def fi(seg):
    '''set steady state RMP for 1 cell'''
    isum = 0
    isum = (seg.ina if h.ismembrane('na_ion') else 0) + (seg.ik if h.ismembrane('k_ion') else 0) + (seg.ica if h.ismembrane('ca_ion') else 0) + (seg.iother if h.ismembrane('other_ion') else 0)
    seg.e_pas = cfg.hParams['v_init']+isum/seg.g_pas 
    if h.ismembrane('cadad'):
        seg.cainf_cadad = seg.cai - ((- (10000) * seg.ica / (2 * h.FARADAY * seg.depth_cadad)) * seg.taur_cadad)
    print(cfg.cellnum)
    print(seg.e_pas)
    # elist.append(seg.e_pas)


def simSim (np0, sc0):
    sim.createSimulateAnalyze(netParams=np0, simConfig=sc0)
    fih = [h.FInitializeHandler(2, lambda: fi(sim.net.cells[0].secs.soma.hObj(0.5)))]
    print('BEFORE simulate')
    sim.simulate()
    sim.saveData()
    print('AFTER save')

if __name__ == "__main__":
    simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams_A.py')
    simSim(netParams, simConfig)
