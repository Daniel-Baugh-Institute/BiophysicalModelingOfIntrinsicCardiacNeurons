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
    if h.ismembrane("me_cadad_Adestexhe"):
        kd_me_cadad_Adestexhe = seg.cai*(-(seg.cai * depth_me_cadad_Adestexhe *FARADAY) + cainf_me_cadad_Adestexhe * depth_me_cadad_Adestexhe * FARADAY - \
            5000*seg.ica*taur_me_cadad_Adestexhe - depth_me_cadad_Adestexhe * FARADAY*kt_me_cadad_Adestexhe * taur_me_cadad_Adestexhe)
        kd_me_cadad_Adestexhe = kd_me_cadad_Adestexhe/(seg.cai*depth_me_cadad_Adestexhe*FARADAY - cainf_me_cadad_Adestexhe * depth_me_cadad_Adestexhe * FARADAY + \
               5000*seg.ica*taur_me_cadad_Adestexhe)
    else:
        0
    print(cfg.cellnum)
    print(seg.e_pas)
    # elist.append(seg.e_pas)



fih = [h.FInitializeHandler(2, fi)]
sim.simulate()
sim.analyze()

# file = open('edump_21jul26b.csv','a') 
# csvwriter = csv.writer(file, delimiter = '\t')
# csvwriter.writerow(elist)
# file.close()
