COMMENT 

Source: Channelpedia
		Model Ca_LVA (ID=3)     

Edits by sgupta (SG): eca computed by adding ghk()
April 2021

ENDCOMMENT

:[$URL: https://bbpteam.epfl.ch/svn/analysis/trunk/IonChannel/xmlTomod/CreateMOD.c $]
:[$Revision: 1499 $]
:[$Date: 2012-01-28 10:45:44 +0100 (Sat, 28 Jan 2012) $]
:[$Author: rajnish $]
:Comment :
:Reference :Multiple channel types contribute to the low-voltage-activated calcium current in hippocampal CA3 pyramidal neurons. J. Neurosci., 1996, 16, 5567-82


NEURON	{
	SUFFIX ch_Cacna1c_cp3
	USEION ca READ cai, cao WRITE ica 			:Added by SG
	RANGE gLbar, gL, ica, BBiD 
	RANGE ggk, ica1c, mInf, mTau, hInf, hTau	:Added by SG
	GLOBAL USEGHK								:Added by SG
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
	gLbar = 0.00001 (S/cm2) 
	BBiD = 212 
  	USEGHK=1 : Added by SG
}

ASSIGNED	{
	v	(mV)
	eca	(mV)
	ica	(mA/cm2)
	gL	(S/cm2)
	mInf
	mTau
	hInf
	hTau

	:Added by SG
	ggk		
	celsius 	(degC)
	cai (mM)
	cao (mM)
	ica1c (mA/cm2)
}

STATE	{ 
	m
	h
}

BREAKPOINT	{
	SOLVE states METHOD cnexp
	gL = gLbar*m*m*h

	:Added by SG

	if(USEGHK ==1)	{
		ggk = ghk(v,cai,cao,celsius)
	} else {
		ggk = (v-eca)
	}
	ica1c = gL*ggk
	ica = ica1c
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
		mInf = 1.0000/(1+ exp((v - -30.000)/-6)) 
		mTau = 10 
		hInf = 1.0000/(1+ exp((v - -80.000)/6.4)) 
		hTau = 59	
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