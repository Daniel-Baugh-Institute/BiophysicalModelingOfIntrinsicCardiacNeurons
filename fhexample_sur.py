# specify an example model
from neuron import h
from neuron.units import ms, mV
import matplotlib.pyplot as plt
h.load_file('stdrun.hoc')

a = h.Section()
h.v_init = -61

for sec in h.allsec():
    sec.insert('hh')
    sec.gnabar_hh = 10 #(default is 0.12)
    # sec.gkbar_hh = 10   #(default is 0.036)
    #tried - 10, 0.4 and 0.04

def fi():
    print('eleak at begg. of fi() = ', a.el_hh)
    isum = a.ina + a.ik
    if isum==0:
        a.el_hh = h.v_init
    else:
        if a.gl_hh>0:
            a.el_hh = h.v_init+isum/a.gl_hh
        else:
            if a.el_hh != h.v_init:
                a.gl_hh = isum/(a.el_hh-h.v_init)
    print('isum = ',isum)
    print('ileak = ',a.il_hh)
    print('isum+ileak =',isum+a.il_hh)
    print('eleak = ',a.el_hh)


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
