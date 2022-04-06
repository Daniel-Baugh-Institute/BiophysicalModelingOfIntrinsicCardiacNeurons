from netpyne import sim
from neuron import h
import numpy as np
import matplotlib.pyplot as plt

sec = h.Section(name="sec")
# m1 = []
# tm1 = []
# m2 = []
# tm2 = []
# m3 = []
# tm3 = []
# m4 = []
# tm4 = []

# sec.insert('ch_Hcn1_cp9')
# sec.insert('ch_Hcn2_cp10')
# sec.insert('ch_Hcn3_cp11')
# sec.insert('ch_Hcn4_cp12')

# volt = [v for v in np.arange(-100,100,1)]
# h.setdata_ch_Hcn1_cp9(sec(0.5))
# for v in volt:
# 	h.rates_ch_Hcn1_cp9(v)
# 	m1.append(sec.mInf_ch_Hcn1_cp9)
# 	tm1.append(sec.mTau_ch_Hcn1_cp9)

# h.setdata_ch_Hcn2_cp10(sec(0.5))
# for v in volt:
# 	h.rates_ch_Hcn2_cp10(v)
# 	m2.append(sec.mInf_ch_Hcn2_cp10)
# 	tm2.append(sec.mTau_ch_Hcn2_cp10)

# h.setdata_ch_Hcn3_cp11(sec(0.5))
# for v in volt:
# 	h.rates_ch_Hcn3_cp11(v)
# 	m3.append(sec.mInf_ch_Hcn3_cp11)
# 	tm3.append(sec.mTau_ch_Hcn3_cp11)

# h.setdata_ch_Hcn4_cp12(sec(0.5))
# for v in volt:
# 	h.rates_ch_Hcn4_cp12(v)
# 	m4.append(sec.mInf_ch_Hcn4_cp12)
# 	tm4.append(sec.mTau_ch_Hcn4_cp12)

# fig, axs = plt.subplots(1,2)
# axs[0].set_title('inf')
# axs[0].plot(volt,m1, label = 'HCN1')
# axs[0].plot(volt,m2, label = 'HCN2')
# axs[0].plot(volt,m3, label = 'HCN3')
# axs[0].plot(volt,m4, label = 'HCN4')
# axs[0].legend()
# axs[1].set_title('tau')
# axs[1].plot(volt,tm1, label = 'HCN1')
# axs[1].plot(volt,tm2, label = 'HCN2')
# axs[1].plot(volt,tm3, label = 'HCN3')
# axs[1].plot(volt,tm4, label = 'HCN4')
# axs[1].legend()
# plt.show()
minf = []
hinf = []
mtau = []
htau = []

# mech = 'ch_Cacna1i_cp42' #hh
# sec.insert(mech)
# h.setdata_ch_Cacna1i_cp42(sec(0.5))
# volt = [v for v in np.arange(-100,100,1)] #left window

# for v in volt:
# 	h.rates_ch_Cacna1i_cp42(v)
# 	minf.append(sec.mInf_ch_Cacna1i_cp42)
# 	hinf.append(sec.hInf_ch_Cacna1i_cp42)
# 	mtau.append(sec.mTau_ch_Cacna1i_cp42)
# 	htau.append(sec.hTau_ch_Cacna1i_cp42)

mech = "ch_Cacna1i_md279"  # hh
sec.insert(mech)
# h.setdata_itGHK(sec(0.5))
volt = [v for v in np.arange(-100, 100, 1)]

h.setdata_ch_Cacna1i_md279(sec(0.5))
# import IPython; IPython.embed()

for v in volt:
    h.evaluate_fct_ch_Cacna1i_md279(v)
    minf.append(sec.m_inf_ch_Cacna1i_md279)
    hinf.append(sec.h_inf_ch_Cacna1i_md279)


plt.figure()
plt.plot(volt, minf, volt, hinf)
plt.show()

# fig, axs = plt. subplots(1,2)
# axs[0].set_title('m/hinf vs Vm')
# axs[0].plot(volt,minf, volt,hinf)
# axs[1].set_title('m/htau vs Vm')
# axs[1].plot(volt,mtau, volt,htau)
# plt.show()
