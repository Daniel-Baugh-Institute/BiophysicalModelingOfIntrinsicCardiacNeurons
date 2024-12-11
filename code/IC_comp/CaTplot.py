import os
os.system('nrnivmodl CaTmod')

# from netpyne import sim
from neuron import h
import numpy as np
import matplotlib.pyplot as plt


sec = h.Section(name = 'sec')
mc = []	#CP
tmc = []
hc = []
thc = []
mm = []	#modelDB
tmm = []
hm = []
thm = []
mt = []  #IT.mod
tmt = []
ht = []
tht = []

sec.insert('ch_Cacna1i_cp42')
sec.insert('ch_Cacna1i_md279')
sec.insert('ittc')

volt = [v for v in np.arange(-100,100,1)]

h.setdata_ch_Cacna1i_cp42(sec(0.5))
for v in volt:
	h.rates_ch_Cacna1i_cp42(v)
	mc.append(sec.mInf_ch_Cacna1i_cp42)
	hc.append(sec.hInf_ch_Cacna1i_cp42)
	tmc.append(sec.mTau_ch_Cacna1i_cp42)
	thc.append(sec.hTau_ch_Cacna1i_cp42)

h.setdata_ch_Cacna1i_md279(sec(0.5))
for v in volt:
	h.evaluate_fct_ch_Cacna1i_md279(v)
	mm.append(sec.m_inf_ch_Cacna1i_md279)
	hm.append(sec.h_inf_ch_Cacna1i_md279)
	tmm.append(sec.tau_m_ch_Cacna1i_md279)
	thm.append(sec.tau_h_ch_Cacna1i_md279)

h.setdata_ittc(sec(0.5))
for v in volt:
	h.mh_ittc(v)
	mt.append(sec.m_inf_ittc)
	ht.append(sec.h_inf_ittc)
	tmt.append(sec.tau_m_ittc)
	tht.append(sec.tau_h_ittc)


fig, axs = plt.subplots(2,2)
fig.suptitle('Voltage-gated T-type Calcium Channel (Cav 3.3)')
axs[0,0].set_title('Activation State Variable at steady-state')
axs[0,0].plot(volt,mc, label = 'Cacna1i (Channelpedia 42)',linestyle='dashed',color='blue')
# axs[0,0].plot(volt,mt, label = 'T-type (Neurosim)', color='black')
axs[0,0].plot(volt,mm, label = 'Cacna1i (ModelDB 279)*', color='red')
axs[0,0].legend()

axs[0,1].set_title('Inactivation State Variable at steady-state')
axs[0,1].plot(volt,hc, label = 'Cacna1i (Channelpedia 42)',linestyle='dashed',color='blue')
# axs[0,1].plot(volt,ht, label = 'T-type (Neurosim)', color='black')
axs[0,1].plot(volt,hm, label = 'Cacna1i (ModelDB 279)*', color='red')
axs[0,1].legend()

axs[1,0].set_title('Activation Time Constant (ms)')
axs[1,0].plot(volt,tmc, label = 'Cacna1i (Channelpedia 42)',linestyle='dashed',color='blue')
# axs[1,0].plot(volt,tmt, label = 'T-type (Neurosim)', color='black')
axs[1,0].plot(volt,tmm, label = 'Cacna1i (ModelDB 279)*', color='red')
axs[1,0].set_xlabel('Membrane Voltage (mV)')
axs[1,0].legend()

axs[1,1].set_title('Inactivation Time Constant (ms)')
axs[1,1].plot(volt,thc, label = 'Cacna1i (Channelpedia 42)',linestyle='dashed',color='blue')
# axs[1,1].plot(volt,tht, label = 'T-type (Neurosim)', color='black')
axs[1,1].plot(volt,thm, label = 'Cacna1i (ModelDB 279)*', color='red')
axs[1,1].set_xlabel('Membrane Voltage (mV)')
axs[1,1].legend()
plt.show()

# plt.figure()
# plt.plot(volt,mc)
# plt.show()

# plt.figure()
# plt.plot(volt,tmc)
# plt.show()