: SK-type calcium-activated potassium current
: Reference : Kohler et al. 1996

COMMENT
26 July 2021 Edits by Suranjana Gupta (SG)
Changed SUFFIX and added ikcnn3
Changed rates (ca) to rates (conc)
ENDCOMMENT

NEURON {
       SUFFIX ch_Kcnn3_md169457
       USEION k READ ek WRITE ik
       USEION ca READ cai
       RANGE gSK_E2bar, gSK_E2, ikcnn3, ik, offc, zTau, sloc
}

UNITS {
      (mV) = (millivolt)
      (mA) = (milliamp)
      (mM) = (milli/liter)
}

PARAMETER {
    v            (mV)
    gSK_E2bar = .000001 (mho/cm2)
    zTau = 1              (ms)
    ek           (mV)
    cai          (mM)
    offc = 0.00043 (mM)
	sloc = 4.8
}

ASSIGNED {
         zInf
         ik            (mA/cm2)
         ikcnn3        (mA/cm2)         :Added by SG
         gSK_E2	       (S/cm2)
}

STATE {
      z   FROM 0 TO 1
}

BREAKPOINT {
           SOLVE states METHOD cnexp
           gSK_E2  = gSK_E2bar * z
           ikcnn3   =  gSK_E2 * (v - ek)
           ik = ikcnn3                   :Added by SG
}

DERIVATIVE states {
        rates(cai)
        z' = (zInf - z) / zTau
}

PROCEDURE rates(conc(mM)) {                 : SG changed ca to conc
          if(conc < 1e-7){
	              conc = conc + 1e-07
          }
          zInf = 1/(1 + (offc / conc)^sloc)
}

INITIAL {
        rates(cai)
        z = zInf
}






