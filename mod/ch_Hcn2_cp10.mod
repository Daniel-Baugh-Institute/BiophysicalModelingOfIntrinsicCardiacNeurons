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
	SUFFIX ch_Hcn2_cp10
	USEION other WRITE iother VALENCE 1.0 				:Added by SG
	RANGE gHCN2bar, gHCN2, ihcn2, ehcn, BBiD, mInf, mTau 
    RANGE npy, npymod
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
    npy = 0 (mM)
    npymaxG = 0.11     : maximum 11% reduction in conductance
    npymaxV = 12       : maximum 15% reduction in Erev (to -51.75)
    npyic50 = 404e-6 (mM)
}

ASSIGNED	{
	v	(mV)
	ihcn2	(mA/cm2)
	gHCN2	(S/cm2)
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
	gHCN2 = gHCN2bar*m
    npymod = (npy/(npy+npyic50))
	ihcn2 = gHCN2*(v-ehcn + npymaxV*npymod)*(1.0 - npymaxG*npymod)
	iother = ihcn2				:Added by SG
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
		mInf = 1.0000/(1+exp((v- -99)/6.2)) 
		mTau = 184.0000
	UNITSON
}
