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
    sec.gnabar_hh = 10 #(default is 0.12)
    sec.gl_hh = 0
    

def fi():
    print('epas at begg. of fi() = ', a.e_pas)
    isum = a.ina + a.ik #+ a.il_hh
    if isum==0:
        a.e_pas = h.v_init
    else:
        if a.g_pas>0:
            a.e_pas = h.v_init+isum/a.g_pas
        else:
            if a.e_pas != h.v_init:
                a.g_pas = isum/(a.e_pas-h.v_init)
    print('isum = ',isum)
    print('ipas = ',a.i_pas)
    print('isum+ipas =',isum+a.i_pas)
    print('epas = ',a.e_pas)


fih = [h.FInitializeHandler(2, fi)]

volt = h.Vector().record(a(0.5)._ref_v)            
time = h.Vector().record(h._ref_t) 

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
