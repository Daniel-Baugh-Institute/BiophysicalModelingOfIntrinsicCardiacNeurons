COMMENT

"NaV1.1" channel.
BBP 'fast' Na channel, but activation/inactivation vHalf and slope adjusted to fit experimental data.

ENDCOMMENT

:Reference :Colbert and Pan 2002

: Adapted by Werner Van Geit @ BBP, 2015 (with help from M.Hines):
: channel detects TTX concentration set by TTXDynamicsSwitch.mod

: 10 June 2021 - Added local iscn current

COMMENT
22 June 2021
mInf, mTau, hInf, hTau are made GLOBAL
rates(v(mV)) instead of rates()
ENDCOMMENT


NEURON {
	SUFFIX ch_Scn1a_md264834
	USEION na READ ena WRITE ina
	:USEION ttx READ ttxo, ttxi VALENCE 1
	RANGE gNav11bar, gNav11, ina,mh,ms,hh,hs, iscn
	RANGE mInf, mTau, hInf, hTau										:SG
}

UNITS	{
	(S) = (siemens)
	(mV) = (millivolt)
	(mA) = (milliamp)
}

PARAMETER	{
	gNav11bar = 0.00001 (S/cm2)
	mh=-18.46 : activation vh
	ms=7.91   : activation slope
	hh=-48.8 : inactivation vh
	hs=6.25   : inactivation slope
}

ASSIGNED {
	:ttxo (mM)
	:ttxi (mM)
	v	(mV)
	ena	(mV)
	ina	(mA/cm2)
	gNav11	(S/cm2)
	mInf
	mTau
	hInf
	hTau
	iscn (mA/cm2)
    achmod
}

STATE	{
	m
	h
}

BREAKPOINT	{
	SOLVE states METHOD cnexp
	gNav11 = gNav11bar*m*m*m*h
	iscn = gNav11*(v-ena)
	ina = iscn
}

DERIVATIVE states	{
COMMENT
	if (ttxi == 0.015625 && ttxo > 1e-12) {
		mInf = 0.0
		mTau = 1e-12
		hInf = 1.0
		hTau = 1e-12
	} else {
		rates(v)
	}
ENDCOMMENT
	rates(v)
	m' = (mInf-m)/mTau
	h' = (hInf-h)/hTau
}

INITIAL{
COMMENT
	if (ttxi == 0.015625 && ttxo > 1e-12) {
		mInf = 0.0
		mTau = 1e-12
		hInf = 1.0
		hTau = 1e-12
	} else {
		rates(v)
	}
ENDCOMMENT
	m = mInf
	h = hInf
}

PROCEDURE rates(v (mV)){
  LOCAL qt
  qt = 2.3^((34-24)/10) : recordings at 24C

  UNITSOFF
    if(v == mh){
    	v = v+0.0001
    }
		mTau = (0.0876 + 0.35 * exp((-(-25.04 - v)^2)/ 340.13))/qt
		mInf = 1.0/(1.0+exp((mh-v)/ms))

    if(v == hh){
      v = v + 0.0001
    }
		hTau = (0.438 + 12.22 * exp((-(-55.53 - v)^2)/ 547.24))/qt
		hInf = 1.0/(1.0+exp((v-hh)/hs))
	UNITSON
}
