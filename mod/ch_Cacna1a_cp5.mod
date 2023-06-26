COMMENT 

Source: Channelpedia
		Model Ca_P/Q (ID=5)

Edits by sgupta (SG): eca computed by adding ghk()
April 2021

ENDCOMMENT


:[$URL: https://bbpteam.epfl.ch/svn/analysis/trunk/IonChannel/xmlTomod/CreateMOD.c $]
:[$Revision: 1499 $]
:[$Date: 2012-01-28 10:45:44 +0100 (Sat, 28 Jan 2012) $]
:[$Author: rajnish $]
:Comment :
:Reference :Low-threshold potassium channels and a low-threshold calcium channel regulate Ca2+ spike firing in the dendrites of cerebellar Purkinje neurons: a modeling study. Brain Res., 2001, 891, 106-15

NEURON	{
	SUFFIX ch_Cacna1a_cp5
	USEION ca READ cai, cao WRITE ica 			:Added by SG
	RANGE gCav2_1bar, gCav2_1, ica, BBiD
	RANGE ggk, ica1a, mInf, mTau				:Added by SG
	GLOBAL USEGHK			 					:Added by SG
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
	gCav2_1bar = 0.00001 (S/cm2) 
	BBiD = 5 
  	USEGHK=1 	:Added by SG
}

ASSIGNED	{
	v	(mV)
	eca	(mV)
	ica	(mA/cm2)
	gCav2_1	(S/cm2)
	mInf
	mTau
	mAlpha
	mBeta

	:Added by SG
	ggk		
	celsius 	(degC)
	cai (mM)
	cao (mM)
	ica1a (mA/cm2)	:Added by SG
}

STATE	{ 
	m
}

BREAKPOINT	{
	SOLVE states METHOD cnexp
	gCav2_1 = gCav2_1bar*m

	:Added by SG

	if(USEGHK ==1)	{
		ggk = ghk(v,cai,cao,celsius)
	} else {
		ggk = (v-eca)
	}
	ica1a = gCav2_1*ggk
	ica = ica1a	
}

DERIVATIVE states	{
	rates(v)
	m' = (mInf-m)/mTau
}

INITIAL{
	rates(v)
	m = mInf
}

UNITSOFF 
PROCEDURE rates(v (mV)){
		mAlpha = 8.5/(1+exp((v-8)/(-12.5))) 
		mBeta = 35/(1+exp((v+74)/(14.5)))
		mInf = mAlpha/(mAlpha + mBeta)
		mTau = 1/(mAlpha + mBeta)
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
