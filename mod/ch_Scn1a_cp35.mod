COMMENT 

Source: Channelpedia
		Model Na (ID 35)
ENDCOMMENT


:[$URL: https://bbpteam.epfl.ch/svn/analysis/trunk/IonChannel/xmlTomod/CreateMOD.c $]
:[$Revision: 1499 $]
:[$Date: 2012-01-28 10:45:44 +0100 (Sat, 28 Jan 2012) $]
:[$Author: rajnish $]
:Comment :
:Reference :Developmental changes in Na+ conductances in rat neocortical neurons: appearance of a slowly inactivating component. J. Neurophysiol., 1988, 59, 778-95

NEURON	{
	SUFFIX ch_Scn1a_cp35
	USEION na READ ena WRITE ina
	RANGE gNabar, gNa, ina, BBiD 
}

UNITS	{
	(S) = (siemens)
	(mV) = (millivolt)
	(mA) = (milliamp)
}

PARAMETER	{
	gNabar = 0.00001 (S/cm2) 
	BBiD = 189 
}

ASSIGNED	{
	v	(mV)
	ena	(mV)
	ina	(mA/cm2)
	gNa	(S/cm2)
	mInf
	mTau
	mAlpha
	mBeta
	hInf
	hTau
}

STATE	{ 
	m
	h
}

BREAKPOINT	{
	SOLVE states METHOD cnexp
	gNa = gNabar*m*m*m*h
	ina = gNa*(v-ena)
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

PROCEDURE rates(v (mV)){
	UNITSOFF
		if(v == -35){
			v = v + 0.000001
		}
		mAlpha = (0.182 * (v- -35))/(1-(exp(-(v- -35)/9)))
		if(v == -35){
			v = v + 0.000001
		}
		mBeta = (0.124 * (-v -35))/(1-(exp(-(-v -35)/9)))
		mInf = mAlpha/(mAlpha + mBeta)
		mTau = 1/(mAlpha + mBeta) 
		hInf = 1.0/(1+exp((v- -65)/6.2))
		if(v == -50){
			v = v + 0.000001
		}
		hTau = 1/((0.024 * (v- -50))/(1-(exp(-(v- -50)/5))) +(0.0091 * (-v - 75.000123))/(1-(exp(-(-v - 75.000123)/5))))
	UNITSON
}
