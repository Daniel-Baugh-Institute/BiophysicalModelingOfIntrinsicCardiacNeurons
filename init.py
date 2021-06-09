from netpyne import sim

simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
# sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
sim.create(netParams=netParams, simConfig=simConfig)

print('AAAAAAAAAAAAAAAAAAAAAA')

def set_memb():
    isum = ina + ik + ica + iother
