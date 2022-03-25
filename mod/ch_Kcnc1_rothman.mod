NEURON {
	SUFFIX ch_Kcnc1_rothman
	USEION k READ ek WRITE ik
	RANGE gbar, ik, ikcnc, ninf, taun, pinf, taup
	RANGE phi
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


PARAMETER {
	v (mV)
	celsius (degC)
	phi = 0.85
	gbar = 0.011 (mho/cm2)   <0,1e9>
}


ASSIGNED {
 	ik (mA/cm2) 
	ek (mV)
	ninf
	taun (ms)
	pinf
	taup (ms)
	ikcnc (mA/cm2)
}

STATE { n p }

INITIAL {
	rates(v)
	n = ninf
	p = pinf
}

BREAKPOINT {
	SOLVE states METHOD cnexp
	ikcnc = gbar * (v - ek) * ((phi*n*n)+((1-phi)*p))
	ik = ikcnc
}

DERIVATIVE states {
	rates(v)
	n' = (ninf-n)/taun 
	p' = (pinf-p)/taup 
}

PROCEDURE rates(v (mV)) {
	ninf = (1+exp(-(v+15)/5))^(-1/2)    
	pinf = (1+exp(-(v+23)/6))^(-1)  
	taun = (100 * (11*exp((v+60)/24) + 21*exp(-(v+60)/23))^(-1)) + 0.7 
	taup = (100 * (4*exp((v+60)/32) + 5*exp(-(v+60)/22))^(-1)) + 5
}
