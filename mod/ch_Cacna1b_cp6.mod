:[$URL: https://bbpteam.epfl.ch/svn/analysis/trunk/IonChannel/xmlTomod/CreateMOD.c $]
:[$Revision: 1499 $]
:[$Date: 2012-01-28 10:45:44 +0100 (Sat, 28 Jan 2012) $]
:[$Author: rajnish $]
:Comment :
:Reference :Activation and inactivation properties of voltage-gated calcium currents in developing cat retinal ganglion cells. Neuroscience, 1998, 85, 239-47

COMMENT
11 Apr 2021
Edits by Suranjana Gupta (SG): eca computed by adding ghk()

ghk() has been added from:
https://senselab.med.yale.edu/modeldb/showmodel.cshtml?model=136095&file=%2fncdemo%2fil.mod#tabs-2

USEGHK (and associated codes) have been added (mm) along the format in:
https://senselab.med.yale.edu/modeldb/ShowModel?model=168874&file=/ca1dDemo/cal_mig.mod#tabs-2

10 June 2021 - Added local ica1b current

22 June 2021
mInf, mTau, hInf, hTau are made GLOBAL
rates(v(mV)) instead of rates()
ENDCOMMENT



NEURON	{
	SUFFIX ch_Cacna1b_cp6
	:USEION ca READ eca WRITE ica 				:SG
	USEION ca READ cai, cao WRITE ica 			:SG mm
	RANGE gCav2_2bar, gCav2_2, ica, BBiD 
	RANGE ggk, ica1b, mInf, mTau, hInf, hTau	:SG mm
	GLOBAL USEGHK								:SG mm
}

UNITS	{
	(S) = (siemens)
	(mV) = (millivolt)
	(mA) = (milliamp)
	:SG
	(molar) = (1/liter)
	(mM) = (millimolar)
	FARADAY = (faraday) (coulomb)	
	R = (k-mole) (joule/degC)	: SG -> it is actually J/K-mole but won't compile if units are changed

}

PARAMETER	{
	gCav2_2bar = 0.00001 (S/cm2) 
	BBiD = 79
	:SG
  	USEGHK=1
}

ASSIGNED	{
	v	(mV)
	eca	(mV)
	ica	(mA/cm2)
	gCav2_2	(S/cm2)
	mInf
	mTau
	mAlpha
	mBeta
	hInf
	hTau
	hAlpha
	hBeta
	:SG
	ggk		
	celsius 	(degC)
	cai (mM)
	cao (mM)
	ica1b (mA/cm2)
}

STATE	{ 
	m
	h
}

BREAKPOINT	{
	SOLVE states METHOD cnexp
	gCav2_2 = gCav2_2bar*m*m*h
	:Added by SG
	if(USEGHK ==1)	{
		ggk = ghk(v,cai,cao,celsius)
	} else {
		ggk = (v-eca)
	}
	ica1b = gCav2_2*ggk
	ica = ica1b
	:ica = gCav2_2*(v-eca)
}

DERIVATIVE states	{
	rates(v)
	m' = (mInf-m)/mTau
	h' = (hInf-h)/hTau
}

INITIAL{
	rates(v)
	m = mInf
	h = hInf
}

UNITSOFF
PROCEDURE rates(v (mV)){
		if(v == 20){
			v = v + 0.000001
		}
		mAlpha = (0.1*(v-20)/(1-exp(-(v-20)/10))) 
		mBeta = 0.4*exp(-(v+25)/18)
		mInf = mAlpha/(mAlpha + mBeta)
		mTau = 1/(mAlpha + mBeta) 
		hAlpha = 0.01*exp(-(v+50)/10) 
		hBeta = 0.1/(1+exp(-(v+17)/17))
		hInf = hAlpha/(hAlpha + hBeta)
		hTau = 1/(hAlpha + hBeta)	
}
:Two Functions added by SG
FUNCTION ghk(v(mV), ci(mM), co(mM),celsius(degC)) (.001 coul/cm3) {
	LOCAL z, eci, eco
	z = (1e-3)*2*FARADAY*v/(R*(celsius+273.15))
	eco = co*efun(z)
	eci = ci*efun(-z)
	:high cao charge moves inward
	:negative potential charge moves inward
	ghk = (.001)*2*FARADAY*(eci - eco)
}

FUNCTION efun(z) {
	if (fabs(z) < 1e-4) {
		efun = 1 - z/2
	}else{
		efun = z/(exp(z) - 1)
	}
}


UNITSON