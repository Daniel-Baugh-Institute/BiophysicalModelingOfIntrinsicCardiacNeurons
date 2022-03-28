from neuron import h
import numpy as np
import math
import matplotlib.pyplot as plt

volt = [v for v in np.arange(-100,100,1)]

sec = h.Section(name = 'sec')
mna = []
hna = []

sec.insert('ch_Scn1a_md264834')

h.setdata_ch_Scn1a_md264834(sec(0.5))
for v in volt:
	h.rates_ch_Scn1a_md264834(v)
	mna.append(sec.mInf_ch_Scn1a_md264834)
	hna.append(sec.hInf_ch_Scn1a_md264834)


sec = h.Section(name = 'sec')
mh1 = []
mh2 = []
mh3 = []
mh4 = []

sec.insert('ch_Hcn1_cp9')
sec.insert('ch_Hcn2_cp10')
sec.insert('ch_Hcn3_cp11')
sec.insert('ch_Hcn4_cp12')

h.setdata_ch_Hcn1_cp9(sec(0.5))
for v in volt:
	h.rates_ch_Hcn1_cp9(v)
	mh1.append(sec.mInf_ch_Hcn1_cp9)
h.setdata_ch_Hcn2_cp10(sec(0.5))
for v in volt:
	h.rates_ch_Hcn2_cp10(v)
	mh2.append(sec.mInf_ch_Hcn2_cp10)
h.setdata_ch_Hcn3_cp11(sec(0.5))
for v in volt:
	h.rates_ch_Hcn3_cp11(v)
	mh3.append(sec.mInf_ch_Hcn3_cp11)
h.setdata_ch_Hcn4_cp12(sec(0.5))
for v in volt:
	h.rates_ch_Hcn4_cp12(v)
	mh4.append(sec.mInf_ch_Hcn4_cp12)

sec = h.Section(name = 'sec')
nka = []
xka = []

pkc = []
nkc = []
nkj = []

sec.insert('ch_Kcna1ab1_md80769')
sec.insert('ch_Kcnc1_rothman')
sec.insert('ch_Kcnj3_md2488')

h.setdata_ch_Kcna1ab1_md80769(sec(0.5))
for v in volt:
	h.rates_ch_Kcna1ab1_md80769(v)
	nka.append(sec.ninf_ch_Kcna1ab1_md80769)
	xka.append(sec.xinf_ch_Kcna1ab1_md80769)

h.setdata_ch_Kcnc1_rothman(sec(0.5))
for v in volt:
	h.rates_ch_Kcnc1_rothman(v)
	nkc.append(sec.ninf_ch_Kcnc1_rothman)
	pkc.append(sec.pinf_ch_Kcnc1_rothman)

h.setdata_ch_Kcnj3_md2488(sec(0.5))
for v in volt:
	h.rates_ch_Kcnj3_md2488(v)
	nkj.append(sec.ninf_ch_Kcnj3_md2488)

sec = h.Section(name = 'sec')
mc1a = []
mc1b = []
hc1b = []
mc1c = []
hc1c = []
mc1d = []
hc1d = []
mc1g = []
hc1g = []
mc1i = []
hc1i = []

sec.insert('ch_Cacna1a_cp5')
sec.insert('ch_Cacna1b_cp6')
sec.insert('ch_Cacna1c_cp3')
sec.insert('ch_Cacna1d_md150284')
sec.insert('ch_Cacna1g_cp41')
sec.insert('ch_Cacna1i_md279')

h.setdata_ch_Cacna1a_cp5(sec(0.5))
for v in volt:
	h.rates_ch_Cacna1a_cp5(v)
	mc1a.append(sec.mInf_ch_Cacna1a_cp5)
h.setdata_ch_Cacna1b_cp6(sec(0.5))
for v in volt:
	h.rates_ch_Cacna1b_cp6(v)
	mc1b.append(sec.mInf_ch_Cacna1b_cp6)
	hc1b.append(sec.hInf_ch_Cacna1b_cp6)
h.setdata_ch_Cacna1c_cp3(sec(0.5))
for v in volt:
	h.rates_ch_Cacna1c_cp3(v)
	mc1c.append(sec.mInf_ch_Cacna1c_cp3)
	hc1c.append(sec.hInf_ch_Cacna1c_cp3)
h.setdata_ch_Cacna1d_md150284(sec(0.5))
for v in volt:
	h.settables_ch_Cacna1d_md150284(v)
	mc1d.append(sec.minf_ch_Cacna1d_md150284)
	hc1d.append(sec.hinf_ch_Cacna1d_md150284)
h.setdata_ch_Cacna1g_cp41(sec(0.5))
for v in volt:
	h.rates_ch_Cacna1g_cp41(v)
	mc1g.append(sec.mInf_ch_Cacna1g_cp41)
	hc1g.append(sec.hInf_ch_Cacna1g_cp41)
h.setdata_ch_Cacna1i_md279(sec(0.5))
for v in volt:
	h.evaluate_fct_ch_Cacna1i_md279(v)
	mc1i.append(sec.m_inf_ch_Cacna1i_md279)
	hc1i.append(sec.h_inf_ch_Cacna1i_md279)

f1 = plt.figure(1)
plt.title('Sodium Channel')
plt.plot(volt,mna, label = 'Activation', color='red')
plt.plot(volt,hna, label = 'Inactivation', linestyle = 'dashed',color='red')
plt.axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
plt.legend()
plt.xlabel('Membrane Potential (mV)')

f2,axs = plt.subplots(2,2)
f2.suptitle('HCN Channels')
axs[0,0].plot(volt,mh1, label = 'HCN1', color='blue')
axs[0,0].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[0,0].legend()
axs[0,0].set_xlabel('Membrane Potential (mV)')

axs[0,1].plot(volt,mh2, label = 'HCN2', color='red')
axs[0,1].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[0,1].legend()
axs[0,1].set_xlabel('Membrane Potential (mV)')

axs[1,0].plot(volt,mh3, label = 'HCN3', color='green')
axs[1,0].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[1,0].legend()
axs[1,0].set_xlabel('Membrane Potential (mV)')

axs[1,1].plot(volt,mh4, label = 'HCN4', color='magenta')
axs[1,1].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[1,1].legend()
axs[1,0].set_xlabel('Membrane Potential (mV)')

f3,axs = plt.subplots(1,3)
f3.suptitle('Potassium Channels')
axs[0].set_title('KCNA1')
axs[0].plot(volt,nka, label = 'Activation', color='red')
axs[0].plot(volt,xka, label = 'Inactivation', linestyle = 'dashed',color='red')
axs[0].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[0].legend()
axs[0].set_xlabel('Membrane Potential (mV)')

axs[1].set_title('KCNC1')
axs[1].plot(volt,nkc, label = 'Fast activation', color='blue')
axs[1].plot(volt,pkc, label = 'Slow activation', marker='+',markersize=4,color='blue')
axs[1].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[1].legend()
axs[1].set_xlabel('Membrane Potential (mV)')

axs[2].set_title('KCNJ3')
axs[2].plot(volt,nkj, label = 'Activation', color='green')
axs[2].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[2].legend()
axs[2].set_xlabel('Membrane Potential (mV)')

f4,axs = plt.subplots(2,3)
f3.suptitle('Calcium Channels')
axs[0,0].set_title('Cacna1a')
axs[0,0].plot(volt,mc1a, label = 'Activation', color='purple')
axs[0,0].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[0,0].legend()
# axs[0,0].set_xlabel('Membrane Potential (mV)')

axs[0,1].set_title('Cacna1b')
axs[0,1].plot(volt,mc1b, label = 'Activation', color='green')
axs[0,1].plot(volt,hc1b, label = 'Inactivation', linestyle = 'dashed',color='green')
axs[0,1].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[0,1].legend()
# axs[0,1].set_xlabel('Membrane Potential (mV)')

axs[0,2].set_title('Cacna1c')
axs[0,2].plot(volt,mc1c, label = 'Activation', color='blue')
axs[0,2].plot(volt,hc1c, label = 'Inactivation', linestyle = 'dashed',color='blue')
axs[0,2].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[0,2].legend()
# axs[0,2].set_xlabel('Membrane Potential (mV)')

axs[1,0].set_title('Cacna1d')
axs[1,0].plot(volt,mc1d, label = 'Activation', color='magenta')
axs[1,0].plot(volt,hc1d, label = 'Inactivation', linestyle = 'dashed',color='magenta')
axs[1,0].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[1,0].legend()
axs[1,0].set_xlabel('Membrane Potential (mV)')

axs[1,1].set_title('Cacna1g')
axs[1,1].plot(volt,mc1g, label = 'Activation', color='steelblue')
axs[1,1].plot(volt,hc1g, label = 'Inactivation', linestyle = 'dashed',color='steelblue')
axs[1,1].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[1,1].legend()
axs[1,1].set_xlabel('Membrane Potential (mV)')

axs[1,2].set_title('Cacna1i')
axs[1,2].plot(volt,mc1i, label = 'Activation', color='red')
axs[1,2].plot(volt,hc1i, label = 'Inactivation', linestyle = 'dashed',color='red')
axs[1,2].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[1,2].legend()
axs[1,2].set_xlabel('Membrane Potential (mV)')

f,axs = plt.subplots(2,2)
axs[0,0].set_title('Sodium Channel')
axs[0,0].plot(volt,mna, label = 'Activation', color='red')
axs[0,0].plot(volt,hna, label = 'Inactivation', linestyle = 'dashed',color='red')
axs[0,0].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[0,0].legend()
# axs[0,0].set_xlabel('Membrane Potential (mV)')
# axs[0,0].set_xlim([-65,-25])

axs[0,1].set_title('HCN Channel')
axs[0,1].plot(volt,mh1, label = 'HCN1', color='blue')
axs[0,1].plot(volt,mh2, label = 'HCN2', color='red')
axs[0,1].plot(volt,mh3, label = 'HCN3', color='green')
axs[0,1].plot(volt,mh4, label = 'HCN4', color='magenta')
axs[0,1].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[0,1].legend() #bbox_to_anchor=(0.4, 0.9), loc=2)
# axs[0,1].set_xlabel('Membrane Potential (mV)')

axs[1,0].set_title('Potassium Channel')
axs[1,0].plot(volt,nka, label = 'KCNA1 (activation)', color='red')
axs[1,0].plot(volt,xka, label = 'KCNA1 (inactivation)', linestyle = 'dashed',color='red')
axs[1,0].plot(volt,nkc, label = 'KCNC1 (fast activation)', color='blue')
axs[1,0].plot(volt,pkc, label = 'KCNC1 (slow activation)', marker='+',markersize=4,color='blue')
axs[1,0].plot(volt,nkj, label = 'KCNJ3 (activation)', color='green')
axs[1,0].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[1,0].legend()
axs[1,0].set_xlabel('Membrane Potential (mV)')

axs[1,1].set_title('Calcium Channel')
axs[1,1].plot(volt,mc1a, label = 'Cacna1a (activation)', color='purple')
axs[1,1].plot(volt,mc1b, label = 'Cacna1b (activation)', color='green')
axs[1,1].plot(volt,hc1b, label = 'Cacna1b (inactivation)', linestyle = 'dashed',color='green')
axs[1,1].plot(volt,mc1c, label = 'Cacna1c (activation)', color='blue')
axs[1,1].plot(volt,hc1c, label = 'Cacna1c (inactivation)', linestyle = 'dashed',color='blue')
axs[1,1].plot(volt,mc1d, label = 'Cacna1d (activation)', color='magenta')
axs[1,1].plot(volt,hc1d, label = 'Cacna1d (inactivation)', linestyle = 'dashed',color='magenta')
axs[1,1].plot(volt,mc1g, label = 'Cacna1g (activation)', color='cyan')
axs[1,1].plot(volt,hc1g, label = 'Cacna1g (inactivation)', linestyle = 'dashed',color='cyan')
axs[1,1].plot(volt,mc1i, label = 'Cacna1i (activation)', color='red')
axs[1,1].plot(volt,hc1i, label = 'Cacna1i (inactivation)', linestyle = 'dashed',color='red')
axs[1,1].axvline(x = -61, color = 'k', label = 'RMP = -61 mV')
axs[1,1].legend(bbox_to_anchor=(0.8, 0.9), loc=2)
axs[1,1].set_xlabel('Membrane Potential (mV)')



plt.show()