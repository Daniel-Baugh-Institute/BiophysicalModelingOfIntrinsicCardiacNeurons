COMMENT 

Source: ModelDB
	Model km.mod (Accession:2488)

Edits by sgupta (SG): Temperature-dependence variable has been replaced by a constant
February 2022
ENDCOMMENT


COMMENT
26 Ago 2002 Modification of original channel to allow variable time step and to correct an initialization error.
    Done by Michael Hines(michael.hines@yale.e) and Ruggero Scorcioni(rscorcio@gmu.edu) at EU Advance Course in Computational Neuroscience. Obidos, Portugal

Potassium channel, Hodgkin-Huxley style kinetics
Based on I-M (muscarinic K channel)
Slow, noninactivating

Author: Zach Mainen, Salk Institute, 1995, zach@salk.edu
	
ENDCOMMENT

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX ch_Kcnj3_md2488
	USEION k READ ek WRITE ik
	RANGE n, gk, gbar
	RANGE ninf, ntau, ikcnj3
	GLOBAL Ra, Rb, tadj, vmin, vmax
}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
	(pS) = (picosiemens)
	(um) = (micron)
} 

PARAMETER {
	gbar = 0.001   	(S/cm2)
	v 		(mV)
								
	tha  = -30	(mV)		: v 1/2 for inf
	qa   = 9	(mV)		: inf slope		
	
	Ra   = 0.001	(/ms)		: max act rate  (slow)
	Rb   = 0.001	(/ms)		: max deact rate  (slow)

	dt		(ms)

	vmin = -120	(mV)
	vmax = 100	(mV)
} 


ASSIGNED {
	a		(/ms)
	b		(/ms)
	ik 		(mA/cm2)
	gk		(pS/um2)
	ek		(mV)
	ninf
	ntau (ms)	
	tadj
	ikcnj3		(mA/cm2)
}
 

STATE { n }

INITIAL { 
	trates(v)
	n = ninf
}

BREAKPOINT {
        SOLVE states METHOD cnexp
	gk = tadj*gbar*n
	ikcnj3 = gk * (v - ek)
	ik = ikcnj3
} 

LOCAL nexp

DERIVATIVE states {   :Computes state variable n 
        trates(v)      :             at the current v and dt.
        n' = (ninf-n)/ntau

}

PROCEDURE trates(v) {  :Computes rate and other constants at current v.
                      :Call once from HOC to initialize inf at resting v.

	rates(v): not consistently executed from here if usetable_hh == 1


:        tinc = -dt * tadj
:        nexp = 1 - exp(tinc/ntau)
}


PROCEDURE rates(v) {  :Computes rate and other constants at current v.
                      :Call once from HOC to initialize inf at resting v.

        a = Ra * (v - tha) / (1 - exp(-(v - tha)/qa))
        b = -Rb * (v - tha) / (1 - exp((v - tha)/qa))

        tadj = 2.716898432 :q10^((celsius - temp)/10)
        ntau = 1/tadj/(a+b)
	ninf = a/(a+b)
}







