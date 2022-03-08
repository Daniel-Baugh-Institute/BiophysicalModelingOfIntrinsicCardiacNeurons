:[$URL: https://bbpteam.epfl.ch/svn/analysis/trunk/IonChannel/xmlTomod/CreateMOD.c $]
:[$Revision: 1499 $]
:[$Date: 2012-01-28 10:45:44 +0100 (Sat, 28 Jan 2012) $]
:[$Author: rajnish $]
:Comment :
:Reference :Cellular expression and functional characterization of four hyperpolarization-activated pacemaker channels in cardiac and neuronal tissues. Eur. J. Biochem., 2001, 268, 1646-52

: Edited by Suranjana Gupta (10 June 2021): Removed 'NONSPECIFIC_CURRENT ihcn' and added ion 'other', to incorporate the rmp() code 

COMMENT
22 June 2021
mInf, mTau are made GLOBAL
rates(v(mV)) instead of rates()
ENDCOMMENT

NEURON	{
	SUFFIX ch_Hcn3_cp11
	USEION other WRITE iother VALENCE 1.0 					:Added by SG
	RANGE gHCN3bar, gHCN3, ihcn3, ehcn, BBiD, mInf, mTau
    RANGE npymod	 
}

UNITS	{
	(S) = (siemens)
	(mV) = (millivolt)
	(mA) = (milliamp)
}

PARAMETER	{
	gHCN3bar = 0.00001 (S/cm2) 
	BBiD = 11 
	ehcn = -45.0 (mV)
    npymod = 0 <0,1>
    npymax = 0.7
}

ASSIGNED	{
	v		(mV)
	ihcn3	(mA/cm2)
	gHCN3	(S/cm2)
	mInf
	mTau
	iother (mA/cm2)
}

STATE	{ 
	m
}

BREAKPOINT	{
	SOLVE states METHOD cnexp
	gHCN3 = gHCN3bar*m
	ihcn3 = gHCN3*(v-ehcn)*(1.0 - npymod*(1.0 - npymax))
	iother = ihcn3				:Added by SG
}

DERIVATIVE states	{
	rates(v)
	m' = (mInf-m)/mTau
}

INITIAL{
	rates(v)
	m = mInf
}

PROCEDURE rates(v (mV)){
	UNITSOFF 
		mInf = 1.0000/(1+exp((v- -96)/8.6)) 
		mTau = 265.0000
	UNITSON
}
