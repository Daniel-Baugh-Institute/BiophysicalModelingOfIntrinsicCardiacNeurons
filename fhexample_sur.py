# specify an example model
from neuron import h
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


h.stdinit()
fih[0].allprint()
h.finitialize(h.v_init)