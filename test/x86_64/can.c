/* Created by Language version: 7.7.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib_ansi.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__CaN
#define _nrn_initial _nrn_initial__CaN
#define nrn_cur _nrn_cur__CaN
#define _nrn_current _nrn_current__CaN
#define nrn_jacob _nrn_jacob__CaN
#define nrn_state _nrn_state__CaN
#define _net_receive _net_receive__CaN 
#define rate rate__CaN 
#define states states__CaN 
 
#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define gcaNbar _p[0]
#define cainit _p[1]
#define ica _p[2]
#define gcaN _p[3]
#define micaN _p[4]
#define hicaN1 _p[5]
#define hicaN2 _p[6]
#define tmcaN _p[7]
#define thcaN1 _p[8]
#define thcaN2 _p[9]
#define ecal _p[10]
#define mcaN _p[11]
#define hcaN2 _p[12]
#define hcaN1 _p[13]
#define DmcaN _p[14]
#define DhcaN2 _p[15]
#define DhcaN1 _p[16]
#define eca _p[17]
#define cai _p[18]
#define cao _p[19]
#define v _p[20]
#define _g _p[21]
#define _ion_cai	*_ppvar[0]._pval
#define _ion_ica	*_ppvar[1]._pval
#define _ion_dicadv	*_ppvar[2]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 /* declaration of user functions */
 static void _hoc_rate(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_CaN", _hoc_setdata,
 "rate_CaN", _hoc_rate,
 0, 0
};
 /* declare global and static user variables */
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "gcaNbar_CaN", 0, 1e+09,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "gcaNbar_CaN", "S/cm2",
 "cainit_CaN", "mM",
 "ica_CaN", "mA/cm2",
 "gcaN_CaN", "S/cm2",
 "tmcaN_CaN", "ms",
 "thcaN1_CaN", "ms",
 "thcaN2_CaN", "ms",
 "ecal_CaN", "mV",
 0,0
};
 static double delta_t = 0.01;
 static double hcaN10 = 0;
 static double hcaN20 = 0;
 static double mcaN0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(_NrnThread*, _Memb_list*, int);
static void nrn_state(_NrnThread*, _Memb_list*, int);
 static void nrn_cur(_NrnThread*, _Memb_list*, int);
static void  nrn_jacob(_NrnThread*, _Memb_list*, int);
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(_NrnThread*, _Memb_list*, int);
static void _ode_matsol(_NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[3]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"CaN",
 "gcaNbar_CaN",
 "cainit_CaN",
 0,
 "ica_CaN",
 "gcaN_CaN",
 "micaN_CaN",
 "hicaN1_CaN",
 "hicaN2_CaN",
 "tmcaN_CaN",
 "thcaN1_CaN",
 "thcaN2_CaN",
 "ecal_CaN",
 0,
 "mcaN_CaN",
 "hcaN2_CaN",
 "hcaN1_CaN",
 0,
 0};
 static Symbol* _ca_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 22, _prop);
 	/*initialize range parameters*/
 	gcaNbar = 7.07355e-05;
 	cainit = 5.00713e-05;
 	_prop->param = _p;
 	_prop->param_size = 22;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 4, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_ca_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[0]._pval = &prop_ion->param[1]; /* cai */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ica */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dicadv */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _thread_mem_init(Datum*);
 static void _thread_cleanup(Datum*);
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _can_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("ca", -10000.);
 	_ca_sym = hoc_lookup("ca_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 5);
  _extcall_thread = (Datum*)ecalloc(4, sizeof(Datum));
  _thread_mem_init(_extcall_thread);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 1, _thread_mem_init);
     _nrn_thread_reg(_mechtype, 0, _thread_cleanup);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 22, 4);
  hoc_register_dparam_semantics(_mechtype, 0, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 CaN /Users/jessicafeldman/Desktop/ragp/ragp/test/mod/can.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "CaN channel from Vadigepalli et al. (2001)";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rate(_threadargsprotocomma_ double, double);
 
#define _deriv1_advance _thread[0]._i
#define _dith1 1
#define _recurse _thread[2]._i
#define _newtonspace1 _thread[3]._pvoid
extern void* nrn_cons_newtonspace(int);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist2[3];
  static int _slist1[3], _dlist1[3];
 static int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset = 0; {
   rate ( _threadargscomma_ v , cai ) ;
   DmcaN = 1000.0 * ( micaN - mcaN ) / tmcaN ;
   DhcaN1 = 1000.0 * ( hicaN1 - hcaN1 ) / thcaN1 ;
   DhcaN2 = 1000.0 * ( hicaN2 - hcaN2 ) / thcaN2 ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
 rate ( _threadargscomma_ v , cai ) ;
 DmcaN = DmcaN  / (1. - dt*( ( ( 1000.0 )*( ( ( - 1.0 ) ) ) ) / tmcaN )) ;
 DhcaN1 = DhcaN1  / (1. - dt*( ( ( 1000.0 )*( ( ( - 1.0 ) ) ) ) / thcaN1 )) ;
 DhcaN2 = DhcaN2  / (1. - dt*( ( ( 1000.0 )*( ( ( - 1.0 ) ) ) ) / thcaN2 )) ;
  return 0;
}
 /*END CVODE*/
 
static int states (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset=0; int error = 0;
 { double* _savstate1 = _thread[_dith1]._pval;
 double* _dlist2 = _thread[_dith1]._pval + 3;
 int _counte = -1;
 if (!_recurse) {
 _recurse = 1;
 {int _id; for(_id=0; _id < 3; _id++) { _savstate1[_id] = _p[_slist1[_id]];}}
 error = nrn_newton_thread(_newtonspace1, 3,_slist2, _p, states, _dlist2, _ppvar, _thread, _nt);
 _recurse = 0; if(error) {abort_run(error);}}
 {
   rate ( _threadargscomma_ v , cai ) ;
   DmcaN = 1000.0 * ( micaN - mcaN ) / tmcaN ;
   DhcaN1 = 1000.0 * ( hicaN1 - hcaN1 ) / thcaN1 ;
   DhcaN2 = 1000.0 * ( hicaN2 - hcaN2 ) / thcaN2 ;
   {int _id; for(_id=0; _id < 3; _id++) {
if (_deriv1_advance) {
 _dlist2[++_counte] = _p[_dlist1[_id]] - (_p[_slist1[_id]] - _savstate1[_id])/dt;
 }else{
_dlist2[++_counte] = _p[_slist1[_id]] - _savstate1[_id];}}}
 } }
 return _reset;}
 
static int  rate ( _threadargsprotocomma_ double _lv , double _lcai ) {
   micaN = 1.0 / ( 1.0 + ( exp ( - ( _lv + 20.0 ) / 4.5 ) ) ) ;
   tmcaN = ( 0.364 * exp ( - ( pow( 0.042 , 2.0 ) ) * ( pow( ( _lv + 31.0 ) , 2.0 ) ) ) ) + 0.442 ;
   hicaN1 = 1.0 / ( 1.0 + ( exp ( ( _lv + 20.0 ) / 25.0 ) ) ) ;
   thcaN1 = ( 3.752 * ( exp ( - ( pow( 0.0395 , 2.0 ) ) * ( pow( ( _lv + 30.0 ) , 2.0 ) ) ) ) ) + 0.56 ;
   hicaN2 = ( 0.2 / ( 1.0 + ( exp ( - ( _lv + 40.0 ) / 10.0 ) ) ) ) + ( 1.0 / ( 1.0 + ( exp ( ( _lv + 20.0 ) / 40.0 ) ) ) ) ;
   thcaN2 = ( 25.2 * exp ( - ( pow( 0.0275 , 2.0 ) ) * ( pow( ( _lv + 40.0 ) , 2.0 ) ) ) ) + 8.4 ;
    return 0; }
 
static void _hoc_rate(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r = 1.;
 rate ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 3;}
 
static void _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  cai = _ion_cai;
     _ode_spec1 (_p, _ppvar, _thread, _nt);
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 3; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 (_p, _ppvar, _thread, _nt);
 }
 
static void _ode_matsol(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  cai = _ion_cai;
 _ode_matsol_instance1(_threadargs_);
 }}
 
static void _thread_mem_init(Datum* _thread) {
   _thread[_dith1]._pval = (double*)ecalloc(6, sizeof(double));
   _newtonspace1 = nrn_cons_newtonspace(3);
 }
 
static void _thread_cleanup(Datum* _thread) {
   free((void*)(_thread[_dith1]._pval));
   nrn_destroy_newtonspace(_newtonspace1);
 }
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_ca_sym, _ppvar, 0, 1);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 2, 4);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
  hcaN1 = hcaN10;
  hcaN2 = hcaN20;
  mcaN = mcaN0;
 {
   mcaN = 0.0 ;
   hcaN1 = 0.0 ;
   hcaN2 = 0.0 ;
   cai = cainit ;
   }
 
}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
  cai = _ion_cai;
 initmodel(_p, _ppvar, _thread, _nt);
 }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   gcaN = gcaNbar * mcaN * ( ( 0.55 * hcaN1 ) + ( 0.45 * hcaN2 ) ) ;
   ica = 1000.0 * gcaN * ( v - ( 13.27 * log ( 4.0 / cai ) ) ) ;
   }
 _current += ica;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
  cai = _ion_cai;
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ double _dica;
  _dica = ica;
 _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
  _ion_dicadv += (_dica - ica)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ica += ica ;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}
 
}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}
 
}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
double _dtsav = dt;
if (secondorder) { dt *= 0.5; }
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
  cai = _ion_cai;
 {  _deriv1_advance = 1;
 derivimplicit_thread(3, _slist1, _dlist1, _p, states, _ppvar, _thread, _nt);
_deriv1_advance = 0;
     if (secondorder) {
    int _i;
    for (_i = 0; _i < 3; ++_i) {
      _p[_slist1[_i]] += dt*_p[_dlist1[_i]];
    }}
 } }}
 dt = _dtsav;
}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(mcaN) - _p;  _dlist1[0] = &(DmcaN) - _p;
 _slist1[1] = &(hcaN1) - _p;  _dlist1[1] = &(DhcaN1) - _p;
 _slist1[2] = &(hcaN2) - _p;  _dlist1[2] = &(DhcaN2) - _p;
 _slist2[0] = &(hcaN1) - _p;
 _slist2[1] = &(hcaN2) - _p;
 _slist2[2] = &(mcaN) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/Users/jessicafeldman/Desktop/ragp/ragp/test/mod/can.mod";
static const char* nmodl_file_text = 
  "TITLE CaN channel from Vadigepalli et al. (2001)\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX CaN\n"
  "	USEION ca READ cai WRITE ica\n"
  "	RANGE gcaN, gcaNbar, ica, ecal, cail\n"
  "	RANGE micaN, tmcaN, hicaN1, thcaN1, hicaN2, thcaN2, cainit\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(mA) = (milliamp)\n"
  "	(mV) = (millivolt)	\n"
  "	(molar) = (1/liter)\n"
  "  	(mM) = (millimolar)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	gcaNbar=7.07355E-05 (S/cm2) <0,1e9>\n"
  "	cainit = 5.007132151536936e-05 (mM)\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	 mcaN hcaN2 hcaN1\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	v (mV)\n"
  "	ica (mA/cm2)\n"
  "	gcaN (S/cm2)\n"
  "	micaN\n"
  "	hicaN1\n"
  "	hicaN2 \n"
  "	tmcaN (ms)  \n"
  "	thcaN1 (ms)\n"
  "	thcaN2 (ms)  \n"
  "	eca (mV) \n"
  "	ecal (mV) \n"
  "	cai (mM)\n"
  "	cao (mM)    \n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	:rate(v,cai)\n"
  "	mcaN = 0\n"
  "	hcaN1 = 0\n"
  "	hcaN2 = 0\n"
  "	cai = cainit\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE states METHOD derivimplicit\n"
  "	gcaN=gcaNbar*mcaN*((0.55*hcaN1)+(0.45*hcaN2))\n"
  "	ica=1000*gcaN*(v-(13.27*log(4/cai)))\n"
  "}\n"
  "\n"
  "DERIVATIVE states {	\n"
  "	rate(v,cai)\n"
  "	mcaN' = 1000*(micaN - mcaN)/tmcaN\n"
  "	hcaN1' = 1000*(hicaN1 - hcaN1)/thcaN1\n"
  "	hcaN2' = 1000*(hicaN2 - hcaN2)/thcaN2\n"
  "}\n"
  "\n"
  "UNITSOFF\n"
  "\n"
  "PROCEDURE rate(v(mV),cai(mM)) {\n"
  "	micaN = 1/(1+(exp(-(v+20)/4.5)))\n"
  "	tmcaN = (0.364*exp(-(0.042^2)*((v+31)^2)))+0.442\n"
  "	hicaN1 = 1/(1+(exp((v+20)/25)))\n"
  "	thcaN1 = (3.752*(exp(-(0.0395^2)*((v+30)^2))))+0.56\n"
  "	hicaN2 = (0.2/(1+(exp(-(v+40)/10))))+(1/(1+(exp((v+20)/40))))\n"
  "	thcaN2 = (25.2*exp(-(0.0275^2)*((v+40)^2)))+8.4\n"
  "}\n"
  "UNITSON\n"
  ;
#endif