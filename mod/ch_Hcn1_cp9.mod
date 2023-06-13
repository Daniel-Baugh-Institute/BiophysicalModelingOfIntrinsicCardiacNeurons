COMMENT 

Source: Channelpedia
		Model HCN1 (ID 9)

Edited by sgupta (SG): Removed 'NONSPECIFIC_CURRENT ihcn' and added ion 'other', to achieve RMP stabilisation (init.py)
June 2021

ENDCOMMENT


:[$URL: https://bbpteam.epfl.ch/svn/analysis/trunk/IonChannel/xmlTomod/CreateMOD.c $]
:[$Revision: 1499 $]
:[$Date: 2012-01-28 10:45:44 +0100 (Sat, 28 Jan 2012) $]
:[$Author: rajnish $]
:Comment :
:Reference :Cellular expression and functional characterization of four hyperpolarization-activated pacemaker channels in cardiac and neuronal tissues. Eur. J. Biochem., 2001, 268, 1646-52


NEURON	{
	SUFFIX ch_Hcn1_cp9
	USEION other WRITE iother VALENCE 1.0 					:Added by SG
	RANGE gHCN1bar, gHCN1, ihcn1, ehcn, BBiD, mInf, mTau 
}

UNITS	{
	(S) = (siemens)
	(mV) = (millivolt)
	(mA) = (milliamp)
}

PARAMETER	{
	gHCN1bar = 0.00001 (S/cm2) 
	BBiD = 9 
	ehcn = -45.0 (mV)
}

ASSIGNED	{
	v	(mV)
	ihcn1	(mA/cm2)
	gHCN1	(S/cm2)
	mInf
	mTau
	iother (mA/cm2)
}

STATE	{ 
	m
}

BREAKPOINT	{
	SOLVE states METHOD cnexp
	gHCN1 = gHCN1bar*m
	ihcn1 = gHCN1*(v-ehcn)
	iother = ihcn1				:Added by SG
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
		mInf = 1.0000/(1+exp((v- -94)/8.1)) 
		mTau = 30.0000
	UNITSON
}
