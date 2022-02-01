NEURON {
	POINT_PROCESS DExp2Syn
	RANGE tau1, tau2, e, i
	NONSPECIFIC_CURRENT i
	RANGE D, g, d, rrate
	GLOBAL total
}

UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(umho) = (micromho)
}



PARAMETER {
	tau1 = 5 (ms) < 1e-9, 1e9 >
	tau2 = 18 (ms) < 1e-9, 1e9 >
	e = 0	(mV)
    d = 0.416 (1) < 0, 1 >     : depression
    rrate = 0.3118 (1) < 1e-9, 1e9 >
}

ASSIGNED {
	v (mV)
	i (nA)
	g (umho)
	factor
	total (umho)
}


STATE {
	A (umho)
	B (umho)
}

INITIAL {
	LOCAL tp
	total = 0
	if (tau1/tau2 > 0.9999) {
		tau1 = 0.9999*tau2
	}
	A = 0
	B = 0
	tp = (tau1*tau2)/(tau2 - tau1) * log(tau2/tau1)
	factor = -exp(-tp/tau1) + exp(-tp/tau2)
	factor = 1/factor
}


BREAKPOINT {
	SOLVE state  METHOD cnexp
	g = B - A
	i = g*(v - e)
}



DERIVATIVE state {
	A' = -A/tau1
	B' = -B/tau2
}


NET_RECEIVE(weight (umho), D, tsyn(ms)) {
    INITIAL {
        : these are in NET_RECEIVE to be per-stream
        D = 1
        tsyn = 0
    }
    D = d + (1-d)*pow(((t-tsyn)*1e-3),rrate)
    if (D > 1) {
        D = 1
    }
    printf("%g\t%g\t%g\t%g\n", t, ((t-tsyn)*1e-3), D,  weight*D)
    tsyn = t
	state_discontinuity(A, A + weight*factor*D)
	state_discontinuity(B, B + weight*factor*D)
	total = total + weight * D
    :D = D * d
}

