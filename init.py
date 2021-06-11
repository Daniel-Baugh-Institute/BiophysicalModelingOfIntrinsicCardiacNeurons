from netpyne import sim

simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
# sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
sim.create(netParams=netParams, simConfig=simConfig)


def set_memb(vinit=-61):
    '''set steady state RMP for 1 cell'''
    print('BBBBBBBBBBBBBBBB')
    seg = sim.net.cells[0].secs.soma.hObj(0.5) # since only 1 cell with nseg=1 can jump straight to that seg
    isum = seg.ina + seg.ik + seg.ica + seg.iother
    seg.e_pas= vinit + isum/seg.g_pas

print('AAAAAAAAAAAAAAAAAAAAAA')

foo = h.FInitializeHandler(0,"set_memb()")
print(type(foo))