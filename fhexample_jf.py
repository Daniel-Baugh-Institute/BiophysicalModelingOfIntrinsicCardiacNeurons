# specify an example model
from neuron import h#, gui
from neuron.units import mV

a = h.Section()
for a in h.allsec():
    #sec.insert('hh')
    #sec.insert('pas')
    #sec.gnabar_hh = 10
    a.insert('hh')
    a.gnabar_hh = 10
    a.insert('pas')
    


def fi2(vinit=-61):
    isum = a.ina + a.ik
    a.e_pas= vinit + isum/a.g_pas
    # print('fi2() called after everything initialized. Just before return')
    # print('     from finitialize.')
    # print('     Good place to record or plot initial values')
    # print('  a.v=%g a.m_hh=%g' % (a.v, a.m_hh))
    # print('  b.v=%g b.m_hh=%g' % (b.v, b.m_hh))

v_init= -61
fih = h.FInitializeHandler(fi2)

class Test:
    def __init__(self):
        self.fih = h.FInitializeHandler(self.p)
    def p(self):
        print('inside %r.p()' % self)

test = Test()

h.stdinit()
fih.allprint(hi)

#fih[0].allprint()