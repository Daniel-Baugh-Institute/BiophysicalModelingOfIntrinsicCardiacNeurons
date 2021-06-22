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

volt = [v for v in np.arange(-100,100,1)]

for v in volt:
	h.rates_ch_Cacna1i_cp42(v)
	minf.append(h.mInf_ch_Cacna1i_cp42)
	hinf.append(h.hInf_ch_Cacna1i_cp42)
	mtau.append(h.mTau_ch_Cacna1i_cp42)
	htau.append(h.hTau_ch_Cacna1i_cp42)

fig, axs = plt.subplots(2,2, sharex = 'all')
fig.suptitle(mech)
axs[0,0].set_xlabel('Membrane Voltage (mV)')
axs[0,0].plot(volt,minf)
axs[0,0].set_title('minf')
axs[0,1].plot(volt,hinf)
axs[0,1].set_title('hinf')
axs[0,1].set_xlabel('Membrane Voltage (mV)')
axs[1,0].plot(volt,mtau)
axs[1,0].set_title('mtau')
axs[1,0].set_xlabel('Membrane Voltage (mV)')
axs[1,1].plot(volt,htau)
axs[1,1].set_title('htau')
axs[1,1].set_xlabel('Membrane Voltage (mV)')
plt.show()
