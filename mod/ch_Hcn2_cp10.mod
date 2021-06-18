:[$URL: https://bbpteam.epfl.ch/svn/analysis/trunk/IonChannel/xmlTomod/CreateMOD.c $]
:[$Revision: 1499 $]
:[$Date: 2012-01-28 10:45:44 +0100 (Sat, 28 Jan 2012) $]
:[$Author: rajnish $]
:Comment :
:Reference :Cellular expression and functional characterization of four hyperpolarization-activated pacemaker channels in cardiac and neuronal tissues. Eur. J. Biochem., 2001, 268, 1646-52

: Edited by Suranjana Gupta (10 June 2021): Removed 'NONSPECIFIC_CURRENT ihcn' and added ion 'other', to incorporate the rmp() code 

NEURON	{
	SUFFIX ch_Hcn2_cp10
	USEION other WRITE iother VALENCE 1.0 		:Added by SG
	RANGE gHCN2bar, gHCN2, ihcn2, ehcn, BBiD 
}

UNITS	{
	(S) = (siemens)
	(mV) = (millivolt)
	(mA) = (milliamp)
}

PARAMETER	{
	gHCN2bar = 0.00001 (S/cm2) 
	BBiD = 62 
	ehcn = -45.0 (mV)
}

ASSIGNED	{
	v	(mV)
	ihcn2	(mA/cm2)
	gHCN2	(S/cm2)
	mInf
	mTau
	iother (mA/cm2)
}

STATE	{ 
	m
}

BREAKPOINT	{
	SOLVE states METHOD cnexp
	gHCN2 = gHCN2bar*m
	ihcn2 = gHCN2*(v-ehcn)
	iother = ihcn2				:Added by SG
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
		mInf = 1.0000/(1+exp((v- -99)/6.2)) 
		mTau = 184.0000
	UNITSON
}
