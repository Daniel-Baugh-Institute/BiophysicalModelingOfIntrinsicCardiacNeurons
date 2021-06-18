:[$URL: https://bbpteam.epfl.ch/svn/analysis/trunk/IonChannel/xmlTomod/CreateMOD.c $]
:[$Revision: 1499 $]
:[$Date: 2012-01-28 10:45:44 +0100 (Sat, 28 Jan 2012) $]
:[$Author: rajnish $]
:Comment :
:Reference :Cellular expression and functional characterization of four hyperpolarization-activated pacemaker channels in cardiac and neuronal tissues. Eur. J. Biochem., 2001, 268, 1646-52

: Edited by Suranjana Gupta (10 June 2021): Removed 'NONSPECIFIC_CURRENT ihcn' and added ion 'other', to incorporate the rmp() code 

NEURON	{
	SUFFIX ch_Hcn4_cp12
	USEION other WRITE iother VALENCE 1.0 		:Added by SG
	RANGE gHCN4bar, gHCN4, ihcn4, ehcn, BBiD 
}

UNITS	{
	(S) = (siemens)
	(mV) = (millivolt)
	(mA) = (milliamp)
}

PARAMETER	{
	gHCN4bar = 0.00001 (S/cm2) 
	BBiD = 64 
	ehcn = -45.0 (mV)	
}

ASSIGNED	{
	v	(mV)
	ihcn4	(mA/cm2)	
	gHCN4	(S/cm2)
	mInf
	mTau
	iother (mA/cm2)
}

STATE	{ 
	m
}

BREAKPOINT	{
	SOLVE states METHOD cnexp
	gHCN4 = gHCN4bar*m
	ihcn4 = gHCN4*(v-ehcn)
	iother = ihcn4				:Added by SG
}

DERIVATIVE states	{
	rates()
	m' = (mInf-m)/mTau
}

INITIAL{
	rates()
	m = mInf
}

PROCEDURE rates(){
	UNITSOFF 
		mInf = 1.0000/(1+exp((v- -100)/9.6)) 
		mTau = 461.0000
	UNITSON
}
