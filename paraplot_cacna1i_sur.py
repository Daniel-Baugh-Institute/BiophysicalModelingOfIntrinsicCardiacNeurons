from netpyne import sim
from neuron import h
import numpy as np
import matplotlib.pyplot as plt

sec = h.Section(name = 'sec')
minf = []
hinf = []
mtau = []
htau = []

mech = 'ch_Cacna1i_cp42' #hh
sec.insert(mech)

volt = [v for v in np.arange(-80,-55,1)] #left window

for v in volt:
	h.rates_ch_Cacna1i_cp42(v)
	minf.append(h.mInf_ch_Cacna1i_cp42)
	hinf.append(h.hInf_ch_Cacna1i_cp42)
	mtau.append(h.mTau_ch_Cacna1i_cp42)
	htau.append(h.hTau_ch_Cacna1i_cp42)

fig, axs = plt. subplots(1,2)
axs[0].set_title('m/hinf vs Vm')
axs[0].plot(volt,minf, volt,hinf)
axs[1].set_title('m/htau vs Vm')
axs[1].plot(volt,mtau, volt,htau)
plt.show()
