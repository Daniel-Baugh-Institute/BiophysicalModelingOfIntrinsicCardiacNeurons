from netpyne import sim

simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
# sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
sim.create(netParams=netParams, simConfig=simConfig)


def set_memb():
    '''set steady state RMP for 1 cell'''
    vinit = sim.net.cells[0].secs.soma.hObj(0.5).v
    seg = sim.net.cells[0].secs.soma.hObj(0.5) # since only 1 cell with nseg=1 can jump straight to that seg
    isum = seg.ina + seg.ik + seg.ica + seg.iother
    seg.e_pas= vinit + isum/seg.g_pas
    if seg.e_pas < -100:
        seg.g_pas = isum/(seg.e_pas - vinit)
    else:
        print("Error!")

set_memb()
print('AAAAAAAAAAAAAAAAAAAAAA')
