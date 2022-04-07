
: A passive non-specific cationic current to simulate nicotinic effect

NEURON {
	SUFFIX nm_In_md149739
	NONSPECIFIC_CURRENT i
	RANGE i, enic, gbar
    RANGE ach, achmod
}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
}

PARAMETER {
	gbar = 1e-3 (siemens/cm2) < 0, 1e9 >
	enic = 3.2  (mV)
    ach = 0 (mM)
    achic50 = 75.5e-3 (mM)
    achmodmax = 1.0
}

ASSIGNED {
	v (mV)
	i (mA/cm2)
}

BREAKPOINT { 
	i = gbar*(v - enic)
}






