from netpyne import sim

simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
# sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
sim.create(netParams=netParams, simConfig=simConfig)


def set_memb():
    isum = ina + ik + ica + iother
    e_pas= v + isum/g_pas
    if e_pas<-100:
        g_pas = isum/(e_pas-v)
    else:
        print("Error!")

set_memb()
print('AAAAAAAAAAAAAAAAAAAAAA')