from neuron import h
import numpy as np
import math
import matplotlib.pyplot as plt

volt = [v for v in np.arange(-100,100,1)]

sec = h.Section(name = 'sec')
mna26 = []
tmna26 = []
hna26 = []
thna26 = []

mcp = []
tmcp = []
hcp = []
thcp = []

mna20 = []
tmna20 = []
hna20 = []
thna20 = []

mna25 = []
tmna25 = []
hna25 = []
thna25 = []

mry = []
tmry = []
hry = []
thry = []

sec.insert('ch_Scn1a_md264834')
sec.insert('ch_Scn1a_cp35')
sec.insert('ch_Scn1a_md20756')
sec.insert('ch_Scn1a_md256632')
sec.insert('ch_Scn1a_rybak')

h.setdata_ch_Scn1a_md264834(sec(0.5))
for v in volt:
	h.rates_ch_Scn1a_md264834(v)
	mna26.append(sec.mInf_ch_Scn1a_md264834)
	tmna26.append(sec.mTau_ch_Scn1a_md264834)
	hna26.append(sec.hInf_ch_Scn1a_md264834)
	thna26.append(sec.hTau_ch_Scn1a_md264834)

h.setdata_ch_Scn1a_cp35(sec(0.5))
for v in volt:
	h.rates_ch_Scn1a_cp35(v)
	mcp.append(sec.mInf_ch_Scn1a_cp35)
	tmcp.append(sec.mTau_ch_Scn1a_cp35)
	hcp.append(sec.hInf_ch_Scn1a_cp35)
	thcp.append(sec.hTau_ch_Scn1a_cp35)

h.setdata_ch_Scn1a_md20756(sec(0.5))
for v in volt:
	h.settables_ch_Scn1a_md20756(v)
	mna20.append(sec.minf_ch_Scn1a_md20756)
	tmna20.append(sec.mtau_ch_Scn1a_md20756)
	hna20.append(sec.hinf_ch_Scn1a_md20756)
	thna20.append(sec.htau_ch_Scn1a_md20756)

h.setdata_ch_Scn1a_md256632(sec(0.5))
for v in volt:
	h.settables_ch_Scn1a_md256632(v)
	mna25.append(sec.minf_ch_Scn1a_md256632)
	tmna25.append(sec.mtau_ch_Scn1a_md256632)
	hna25.append(sec.hinf_ch_Scn1a_md256632)
	thna25.append(sec.htau_ch_Scn1a_md256632)

h.setdata_ch_Scn1a_rybak(sec(0.5))
for v in volt:
	h.rates_ch_Scn1a_rybak(v)
	mry.append(sec.miNa_ch_Scn1a_rybak)
	tmry.append(sec.tmNa_ch_Scn1a_rybak)
	hry.append(sec.hiNa_ch_Scn1a_rybak)
	thry.append(sec.thNa_ch_Scn1a_rybak)

fna,axs = plt.subplots(2,2)
fna.suptitle('Voltage-gated Sodium Channel (Nav 1.1)')
axs[0,0].set_title('Activation State Variable at steady-state')
axs[0,0].plot(volt,mna26, label = 'Scna1 (ModelDB 264834)', linestyle='dashed',color='blue')
axs[0,0].plot(volt,mna20, label = 'Scna1 (ModelDB 20756)', linestyle='dashdot',color='green')
axs[0,0].plot(volt,mna25, label = 'Scna1 (ModelDB 256632)',color='cyan')
axs[0,0].plot(volt,mry, label = 'Scna1 (Rybak, 1997)', linestyle='dotted',color='black')
axs[0,0].plot(volt,mcp, label = 'Scna1 (Channelpedia 35)*',color='red')
axs[0,0].legend()
axs[0,1].set_title('Inactivation State Variable at steady-state')
axs[0,1].plot(volt,hna26, label = 'Scna1 (ModelDB 264834)', linestyle='dashed',color='blue')
axs[0,1].plot(volt,hna20, label = 'Scna1 (ModelDB 20756)', linestyle='dashdot',color='green')
axs[0,1].plot(volt,hna25, label = 'Scna1 (ModelDB 256632)',color='cyan')
axs[0,1].plot(volt,hry, label = 'Scna1 (Rybak, 1997)', linestyle='dotted',color='black')
axs[0,1].plot(volt,hcp, label = 'Scna1 (Channelpedia 35)*',color='red')
axs[0,1].legend()
axs[1,0].set_title('Activation Time Constant (ms)')
axs[1,0].plot(volt,tmna26,label = 'Scna1 (ModelDB 264834)', linestyle='dashed',color='blue')
axs[1,0].plot(volt,tmna20,label = 'Scna1 (ModelDB 20756)', linestyle='dashdot',color='green')
axs[1,0].plot(volt,tmna25,label = 'Scna1 (ModelDB 256632)',color='cyan')
axs[1,0].plot(volt,tmry,label = 'Scna1 (Rybak, 1997)', linestyle='dotted',color='black')
axs[1,0].plot(volt,tmcp,label = 'Scna1 (Channelpedia 35)*',color='red')
axs[1,0].legend()
axs[1,0].set_xlabel('Membrane Potential (mV)')
axs[1,1].set_title('Inactivation Time Constant (ms)')
axs[1,1].plot(volt,thna26,label = 'Scna1 (ModelDB 264834)', linestyle='dashed',color='blue')
axs[1,1].plot(volt,thna20,label = 'Scna1 (ModelDB 20756)', linestyle='dashdot',color='green')
axs[1,1].plot(volt,thna25,label = 'Scna1 (ModelDB 256632)',color='cyan')
axs[1,1].plot(volt,thry,label = 'Scna1 (Rybak, 1997)', linestyle='dotted',color='black')
axs[1,1].plot(volt,thcp,label = 'Scna1 (Channelpedia 35)*',color='red')
axs[1,1].legend()
axs[1,1].set_xlabel('Membrane Potential (mV)')

plt.show()

# f,ax = plt.subplots(1,2)
# ax[0].plot(volt,mcp, label = 'Activation',color='red')
# ax[0].plot(volt,hcp, label = 'Inactivation',linestyle='dashed',color='blue')
# ax[0].set_title('Scna1 (Channelpedia)')
# ax[0].set_xlabel('Membrane Potential (mV)')
# ax[0].legend()
# ax[1].plot(volt,mna, label = 'Activation',color='red')
# ax[1].plot(volt,hna, label = 'Inactivation',linestyle='dashed',color='blue')
# ax[1].set_title('Scna1 (ModelDB)')
# ax[1].set_xlabel('Membrane Potential (mV)')
# ax[1].legend()
# plt.show()

# f = plt.figure()
# plt.plot(volt,mcp, label = 'cpNa Activation',color='red')
# plt.plot(volt,hcp, label = 'cpNa Inactivation',linestyle='dashed',color='red')
# plt.plot(volt,mna, label = 'mdNa Activation',color='blue')
# plt.plot(volt,hna, label = 'mdNa nactivation',linestyle='dashed',color='blue')
# plt.xlabel('Membrane Potential (mV)')
# plt.legend()
# plt.show()