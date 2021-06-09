from netpyne import sim

simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
print('AAAAAAAAAAAAAAAAAAAAAA')


def set_memb():
    isum = 0.0
    if ismembrane("na_ion"):
        isum = isum + ina  
    if ismembrane("k_ion"):
        isum = isum + ik    
    if ismembrane("ca_ion"):
        isum = isum + ica  
    if ismembrane("iother"):
        isum = isum + iother 


