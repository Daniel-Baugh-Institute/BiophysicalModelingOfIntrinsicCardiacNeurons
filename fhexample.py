from neuron import h

h.load_file("nrngui.hoc")
b = h.Section()
b.insert('hh')


def fi0():
	print ("fi0() called after v set but before INITIAL blocks")
	print ("  b.v=%g b.m_hh=%g\n", b.v, b.m_hh)
	b.v = 10


def fi1():
	print ("fi1() called after INITIAL blocks but before BREAKPOINT blocks")
	print ("     or variable step initialization.")
	print ("     Good place to change any states.")
	print ("  b.v=%g b.m_hh=%g\n", b.v, b.m_hh)
	b.v = 10

def fi2():
	print ("fi2() called after everything initialized. Just before return")
	print ("     from finitialize.")
	print ("     Good place to record or plot initial values")
	print ("  b.v=%g b.m_hh=%g\n", b.v, b.m_hh)


fih0 = h.FInitializeHandler(0, "fi0()")
fih1 = h.FInitializeHandler(1, "fi1()")
fih2 = h.FInitializeHandler(2, "fi2()")

# begintemplate Test
# objref fih, this
# proc init() {
# 	fih = new FInitializeHandler("p()", this)
# }
# proc p() {
# 	printf("inside %s.p()\n", this)
# }
# endtemplate Test

# objref test
# test = new Test()

h.stdinit()
fih1.allprint()