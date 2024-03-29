# -*- coding: utf-8 -*-
"""
Created in April 2021

@author: sgupta
"""

from netpyne import sim
from neuron import h

def fi(seg):
    '''setting steady state RMP for each neuron'''
    isum = 0
    isum = (seg.ina if h.ismembrane('na_ion') else 0) + (seg.ik if h.ismembrane('k_ion') else 0) + (seg.ica if h.ismembrane('ca_ion') else 0) + (seg.iother if h.ismembrane('other_ion') else 0)
    seg.e_pas = cfg.hParams['v_init']+isum/seg.g_pas 
    if h.ismembrane('cadad'):
        seg.cainf_cadad = seg.cai - ((- (10000) * seg.ica / (2 * h.FARADAY * seg.depth_cadad)) * seg.taur_cadad)
    print(cfg.cellnum, seg.e_pas)

def simSim (np0, sc0):
    sim.create(netParams=np0, simConfig=sc0)
    fih = [h.FInitializeHandler(2, lambda: fi(sim.net.cells[0].secs.soma.hObj(0.5)))]
    print('BEFORE simulate')
    sim.simulate()
    sim.saveData()
    sim.analyze()
    print('AFTER save')

simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams_M1.py')
simSim(netParams, simConfig)
