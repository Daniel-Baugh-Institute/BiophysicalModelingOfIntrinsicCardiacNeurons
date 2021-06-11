from netpyne import sim

simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
# sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
sim.create(netParams=netParams, simConfig=simConfig)


def set_memb(vinit):
    '''set steady state RMP for 1 cell'''
    seg = sim.net.cells[0].secs.soma.hObj(0.5) # since only 1 cell with nseg=1 can jump straight to that seg
    isum = ina + ik + ica + iother
    e_pas= vinit + isum/g_pas
    if e_pas<-100:
        g_pas = isum/(e_pas - vinit)
    else:
        print("Error!")


print('AAAAAAAAAAAAAAAAAAAAAA')
