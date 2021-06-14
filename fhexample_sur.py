# specify an example model
from neuron import h
from neuron.units import ms, mV
import matplotlib.pyplot as plt
h.load_file('stdrun.hoc')

a = h.Section()
h.v_init = -61

for sec in h.allsec():
    sec.insert('hh')
    sec.insert('pas')
    sec.gnabar_hh = 10

def fi():
    print(a.e_pas)
    isum = a.ina + a.ik
    print(isum)
    a.e_pas= h.v_init + isum/a.g_pas
    print(a.e_pas)


fih = [h.FInitializeHandler(1, fi)]

v = h.Vector().record(a(0.5)._ref_v)            
t = h.Vector().record(h._ref_t) 

h.stdinit()
fih[0].allprint()
h.finitialize(h.v_init)

h.continuerun(40*ms)

plt.figure()
plt.plot(t, v)
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')
plt.show()
