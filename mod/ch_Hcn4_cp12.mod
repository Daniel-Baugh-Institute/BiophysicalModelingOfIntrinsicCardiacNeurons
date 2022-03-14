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
	SUFFIX ch_Hcn4_cp12
	USEION other WRITE iother VALENCE 1.0 					:Added by SG
	RANGE gHCN4bar, gHCN4, ihcn4, ehcn, BBiD, mInf, mTau
    RANGE npy, npymod
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
    npy = 0 (mM)
    npymaxG = 0.11     : maximum 11% reduction in conductance
    npymaxV = 12       : maximum 12mV reduction in Erev
    npyic50 = 404e-6 (mM)

	
}

ASSIGNED	{
	v	(mV)
	ihcn4	(mA/cm2)	
	gHCN4	(S/cm2)
	mInf
	mTau
	iother (mA/cm2)
    npymod
}

STATE	{ 
	m
}

BREAKPOINT	{
	SOLVE states METHOD cnexp
	gHCN4 = gHCN4bar*m
    npymod = (npy/(npy+npyic50))
	ihcn4 = gHCN4*(v-ehcn + npymaxV*npymod)*(1.0 - npymaxG*npymod)
	iother = ihcn4				:Added by SG
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
		mInf = 1.0000/(1+exp((v- -100)/9.6)) 
		mTau = 461.0000
	UNITSON
}
