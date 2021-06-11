# specify an example model
from neuron import h, gui

a = h.Section()
b = h.Section()

for sec in h.allsec():
    sec.insert('hh')

def fi0():
    print('fi0 called after v set but before INITIAL blocks')
    print('  a.v=%g a.m_hh=%g' % (a.v, a.m_hh))
    a.v = 10

def fi1():
    print('fi1() called after INITIAL blocks but before BREAKPOINT blocks')
    print('     or variable step initialization.')
    print('     Good place to change any states.')
    print('  a.v=%g a.m_hh=%g' % (a.v, a.m_hh))
    print('  b.v=%g b.m_hh=%g' % (b.v, b.m_hh))
    b.v = 10

def fi2():
    print('fi2() called after everything initialized. Just before return')
    print('     from finitialize.')
    print('     Good place to record or plot initial values')
    print('  a.v=%g a.m_hh=%g' % (a.v, a.m_hh))
    print('  b.v=%g b.m_hh=%g' % (b.v, b.m_hh))

fih = [h.FInitializeHandler(0, fi0),
       h.FInitializeHandler(1, fi1),
       h.FInitializeHandler(2, fi2)]

class Test:
    def __init__(self):
        self.fih = h.FInitializeHandler(self.p)
    def p(self):
        print('inside %r.p()' % self)

test = Test()

h.stdinit()
fih[0].allprint()