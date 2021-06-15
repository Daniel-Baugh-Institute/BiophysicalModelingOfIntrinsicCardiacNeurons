from netpyne import sim
from neuron import h
import matplotlib.pyplot as plt


simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
# sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
sim.create(netParams=netParams, simConfig=simConfig)


def fi():
    '''set steady state RMP for 1 cell'''
    print('AAAAAAAAAAAAAAAAAAAAAA')
    seg = sim.net.cells[0].secs.soma.hObj(0.5) # since only 1 cell with nseg=1 can jump straight to that seg
    print('epas at begg. of fi() = ', seg.e_pas)
    isum = seg.ina + seg.ik + seg.ica + seg.iother
    if isum==0:
        seg.e_pas = cfg.hParams['v_init']
    else:
        if seg.g_pas>0:
            seg.e_pas = cfg.hParams['v_init']+isum/seg.g_pas
        else:
            if seg.e_pas != cfg.hParams['v_init']:
                seg.g_pas = isum/(seg.e_pas-cfg.hParams['v_init'])
    print('isum = ',isum)
    print('ipas = ',seg.i_pas)
    print('isum+ipas =',isum+seg.i_pas)
    print('epas = ',seg.e_pas)
    print(seg.v)
    print(h.t)
    plt.figure()
    plt.plot(h.t, seg.v)
    plt.show()

fih = [h.FInitializeHandler(2, fi)]
sim.simulate()
sim.analyze()





