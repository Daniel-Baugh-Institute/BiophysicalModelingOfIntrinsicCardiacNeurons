COMMENT 

Source: Channelpedia
		Model Cav3.1 (ID=41)       

Edits by sgupta (SG): eca computed by adding ghk()
April 2021

ENDCOMMENT

:[$URL: https://bbpteam.epfl.ch/svn/analysis/trunk/IonChannel/xmlTomod/CreateMOD.c $]
:[$Revision: 1499 $]
:[$Date: 2012-01-28 10:45:44 +0100 (Sat, 28 Jan 2012) $]
:[$Author: rajnish $]
:Comment :
:Reference :Subunit-specific modulation of T-type calcium channels by zinc. J. Physiol. (Lond.), 2007, 578, 159-71


NEURON	{
	SUFFIX ch_Cacna1g_cp41
	USEION ca READ cai, cao WRITE ica 			:Added by SG
	RANGE gCav3_1bar, gCav3_1, ica, BBiD, ica1g
	RANGE ggk, mInf, mTau, hInf, hTau			:Added by SG
	GLOBAL USEGHK								:Added by SG
}

UNITS	{
	(S) = (siemens)
	(mV) = (millivolt)
	(mA) = (milliamp)

	:Added by SG
	(molar) = (1/liter)
	(mM) = (millimolar)
	FARADAY = (faraday) (coulomb)	
	R = (k-mole) (joule/degC)	: SG -> it is actually J/K-mole but won't compile if units are changed
}

PARAMETER	{
	gCav3_1bar = 0.00001 (S/cm2) 
	BBiD = 41 
  	USEGHK=1 	:Added by SG
}

ASSIGNED	{
	v	(mV)
	eca	(mV)
	ica	(mA/cm2)
	gCav3_1	(S/cm2)
	mInf
	mTau
	hInf
	hTau

	:Added by SG
	ggk		
	celsius 	(degC)
	cai (mM)
	cao (mM)
	ica1g (mA/cm2)
}

STATE	{ 
	m
	h
}

BREAKPOINT	{
	SOLVE states METHOD cnexp
	gCav3_1 = gCav3_1bar*m*h

	:Added by SG

	if(USEGHK ==1)	{
		ggk = ghk(v,cai,cao,celsius)
	} else {
		ggk = (v-eca)
	}
	ica1g = gCav3_1*ggk
	ica = ica1g
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
		mInf = 1 /(1+exp((v-(-42.921064))/-5.163208))
		if(v < -10){
			mTau = -0.855809 + (1.493527 * exp(-v/27.414182))
		}
		if(v >= -10){
			mTau = 1.0
		} 
		hInf = 1 /(1+exp((v-(-72.907420))/4.575763)) 
		hTau = 9.987873 + (0.002883 * exp(-v/5.598574))	
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