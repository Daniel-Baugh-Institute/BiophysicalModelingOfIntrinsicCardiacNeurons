NEURON {
	SUFFIX ch_Kcna1_gupta
	USEION k READ ek WRITE ik
	RANGE gbar, ik, ikcna, winf, tauw, zinf, tauz
	RANGE xinf, taux
	RANGE zeta
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
	zeta = 0.5
	gbar = 0.011 (mho/cm2)   <0,1e9>
}


ASSIGNED {
 	ik (mA/cm2) 
	ek (mV)
	winf
	tauw (ms)
	zinf
	tauz (ms)
	xinf
	taux (ms)
	ikcna (mA/cm2)
}

STATE { w z x}

INITIAL {
	rates(v)
	w = winf
	z = zinf
	x = xinf
}

BREAKPOINT {
	SOLVE states METHOD cnexp
	ikcna = gbar * (w^4)*z*x*(v - ek) 
	ik = ikcna
}

DERIVATIVE states {
	rates(v)
	w' = (winf-w)/tauw
	z' = (zinf-z)/tauz 
	x' = (xinf-x)/taux 
}

PROCEDURE rates(v (mV)) {
	winf = (1+exp(-(v+48)/6))^(-1/4)    
	zinf = (1-zeta)*((1+exp((v+71)/10))^(-1))+zeta  
	xinf = (0.95 / (1 + exp((v + 59) / 3))^0.5)+0.05
	tauw = (100 * (6*exp((v+60)/6) + 16*exp(-(v+60)/45))^(-1)) + 1.5 
	tauz = (1000 * (exp((v+60)/20) + exp(-(v+60)/8))^(-1)) + 50
	taux = (500 / (14*exp((v+28) / 20) + 29*exp(-(v+28) / 10))) + 6
}
