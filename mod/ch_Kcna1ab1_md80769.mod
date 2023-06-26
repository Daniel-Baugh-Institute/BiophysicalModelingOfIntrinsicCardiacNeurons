COMMENT 

Source: ModelDB
		Model Kv1.mod (Accession:80769)

Edits by sgupta (SG): 
	*Temperature-dependence variable has been replaced by a constant
	*Inactivation variable (x) has been introduced to account for the effect of ß1 subunit (refer to manuscript for details)
March 2021
ENDCOMMENT


TITLE Voltage-gated low threshold potassium current from Kv1 subunits

COMMENT

NEURON implementation of a potassium channel from Kv1.1 subunits
Kinetical scheme: Hodgkin-Huxley m^4, no inactivation

Kinetic data taken from: Zerr et al., J.Neurosci. 18 (1998) 2842
Vhalf = -28.8 +/- 2.3 mV; k = 8.1 +/- 0.9 mV

The voltage dependency of the rate constants was approximated by:

alpha = ca * exp(-(v+cva)/cka)
beta = cb * exp(-(v+cvb)/ckb)

Parameters ca, cva, cka, cb, cvb, ckb
are defined in the CONSTANT block.

Laboratory for Neuronal Circuit Dynamics
RIKEN Brain Science Institute, Wako City, Japan
http://www.neurodynamics.brain.riken.jp

Reference: Akemann and Knoepfel, J.Neurosci. 26 (2006) 4602
Date of Implementation: April 2005
Contact: akemann@brain.riken.jp

ENDCOMMENT


NEURON {
	SUFFIX ch_Kcna1ab1_md80769
	USEION k READ ek WRITE ik
	RANGE gk, gbar, ik, ikcna, ninf, taun
	RANGE xinf, taux
}

UNITS {
	(mV) = (millivolt)
	(mA) = (milliamp)
	(nA) = (nanoamp)
	(pA) = (picoamp)
	(S)  = (siemens)
	(nS) = (nanosiemens)
	(pS) = (picosiemens)
	(um) = (micron)
	(molar) = (1/liter)
	(mM) = (millimolar)		
}

CONSTANT {
	q10 = 3

	ca = 0.12889 (1/ms)
	cva = 45 (mV)
	cka = -33.90877 (mV)

	cb = 0.12889 (1/ms)
    cvb = 45 (mV)
	ckb = 12.42101 (mV)         
}

PARAMETER {
	v (mV)
	celsius (degC)
	
	gbar = 0.011 (mho/cm2)   <0,1e9>
}


ASSIGNED {
 	ik (mA/cm2) 
	ek (mV)
	gk  (mho/cm2)
	ninf
	taun (ms)
	alphan (1/ms)
	betan (1/ms)
	qt
	ikcna (mA/cm2)
	xinf
	taux (ms)
}

STATE { n x}

INITIAL {
	qt = q10^((celsius-22 (degC))/10 (degC))	
	rates(v)
	n = ninf
	x = xinf
}

BREAKPOINT {
	SOLVE states METHOD cnexp
    gk = gbar * n^4 * x
	ikcna = gk * (v - ek)
	ik = ikcna
}

DERIVATIVE states {
	rates(v)
	n' = (ninf-n)/taun 
	x' = (xinf-x)/taux 
}

PROCEDURE rates(v (mV)) {
	alphan = 0.12889 * exp(-(v+45)/-33.90877) 
	betan = 0.12889 * exp(-(v+45)/12.42101)
	ninf = alphan/(alphan+betan) 
	taun = 1/(4.171167511*(alphan + betan)) 
	xinf = (0.95 / (1 + exp((v + 59) / 3))^0.5)+0.05
	taux = (500 / (14*exp((v+28) / 20) + 29*exp(-(v+28) / 10))) + 6      
}

FUNCTION alphanfkt(v (mV)) (1/ms) {
	alphanfkt = ca * exp(-(v+cva)/cka) 
}

FUNCTION betanfkt(v (mV)) (1/ms) {
	betanfkt = cb * exp(-(v+cvb)/ckb)
}










