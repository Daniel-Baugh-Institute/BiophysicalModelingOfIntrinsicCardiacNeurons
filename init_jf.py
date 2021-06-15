from netpyne import sim
from neuron import h
h.load_file('stdrun.hoc')
import matplotlib.pyplot as plt



simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
# sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
sim.create(netParams=netParams, simConfig=simConfig)

'''set steady state RMP for 1 cell'''

h.v_init = -61


def fi():
    seg = sim.net.cells[0].secs.soma.hObj(0.5) # since only 1 cell with nseg=1 can jump straight to that segt('epas at begg. of fi() = ', seg.e_pas)
    isum = seg.ina + seg.ik + seg.il_hh + seg.iother + seg.ica
    if isum==0:
        seg.e_pas = h.v_init
    else:
        if seg.g_pas>0:
           seg.e_pas = h.v_init+isum/seg.g_pas
        else:
            if seg.e_pas != h.v_init:
                seg.g_pas = isum/(seg.e_pas-h.v_init)
    print('isum = ',isum)
    print('ipas = ', seg.i_pas)
    print('isum+ipas =',isum + seg.i_pas)
    print('epas = ',seg.e_pas)
    volt = h.Vector().record(seg.v) 
    time = h.Vector().record(h._ref_t) 

            
fih = [h.FInitializeHandler(2,fi)]
fih[0].allprint()
h.finitialize(h.v_init)



# h.stdinit()
fih[0].allprint()
h.finitialize(h.v_init)
h.fcurrent()
h.tstop = 5*ms
h.run(h.tstop)
print('Volt at 0 ms = ',volt[0])
print('Volt at 10 ms = ',volt[-1])

plt.figure()
plt.plot(time, volt)
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')
plt.show()


