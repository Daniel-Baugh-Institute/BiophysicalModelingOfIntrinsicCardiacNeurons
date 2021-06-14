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
    if isum==0:
        a.e_pas = h.v_init
    else:
        if a.g_pas>0:
            a.e_pas = h.v_init+isum/a.g_pas
        else:
            if a.e_pas != h.v_init:
                a.g_pas = isum/(a.e_pas-h.v_init)
    print(isum)
    # a.e_pas= h.v_init + isum/a.g_pas
    print(a.e_pas)
    # print(a(0.5).v)


fih = [h.FInitializeHandler(1, fi)]

volt = h.Vector().record(a(0.5)._ref_v)            
time = h.Vector().record(h._ref_t) 
# epas = h.Vector().record(a(0.5)._ref_e_pas) 

# h.stdinit()
fih[0].allprint()
h.finitialize(h.v_init)

h.run(40*ms)

plt.figure()
plt.plot(time, volt)
# plt.plot(time,epas)
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')
plt.show()
