: $Id: netstim.mod 2212 2008-09-08 14:32:26Z hines $
: comments at end

: the Random idiom has been extended to support CoreNEURON.

: For backward compatibility, noiseFromRandom(hocRandom) can still be used
: as well as the default low-quality scop_exprand generator.
: However, CoreNEURON will not accept usage of the low-quality generator,
: and, if noiseFromRandom is used to specify the random stream, that stream
: must be using the Random123 generator.

: The recommended idiom for specfication of the random stream is to use
: noiseFromRandom123(id1, id2[, id3])

: If any instance uses noiseFromRandom123, then no instance can use noiseFromRandom
: and vice versa.

: adamjhn -- Modified for gamma(k,theta) distributed ISI with
: interval = k*theta (the mean of the distribution)
: loc = (1-noise)*k*theta

NEURON    { 
  ARTIFICIAL_CELL GammaStim
  RANGE number, start
  RANGE noise, k, theta
  THREADSAFE : only true if every instance has its own distinct Random
  BBCOREPOINTER donotuse
}

PARAMETER {
    number      = 10 <0,1e9>            : number of spikes (independent of noise)
    start       = 50 (ms)               : start of first spike
    noise       = 0 <0,1>               : amount of randomness (0.0 - 1.0)
    k           = 2.5 <1e-9,1e9>  : shape
    theta       = 1 <1e-9,1e9>  : scale
}

ASSIGNED {
    event (ms)
    on
    ispike
    donotuse
    gammac
    gammad
    interval    : time between spikes (msec)
}

VERBATIM
#if !NRNBBCORE
/** If we're running in NEURON, specify the noise style for all instances.
 *  1 means noiseFromRandom was called when _ran_compat was previously 0.
 *  2 means noiseFromRandom123 was called when _ran_compat was previously 0.
 */
static int _ran_compat;
#endif
ENDVERBATIM

:backward compatibility
PROCEDURE seed(x) {
VERBATIM
#if !NRNBBCORE
ENDVERBATIM
    set_seed(x)
VERBATIM
#endif
ENDVERBATIM
}

INITIAL {
    VERBATIM
#if NRNBBCORE
    if(_p_donotuse) {
#else
    if(_p_donotuse && _ran_compat == 2) {
#endif
        /* only this style initializes the stream on finitialize */
        nrnran123_setseq(reinterpret_cast<nrnran123_State*>(_p_donotuse), 0, 0);
    }
    ENDVERBATIM
    interval = k*theta
    if(k < 1) {
        gammad = k + 2.0/3.0
    } else {
        gammad = k - 1.0/3.0
    }
    gammac = pow(9.0*gammad,-0.5)

    on = 0 : off
    ispike = 0
    if (noise < 0) {
        noise = 0
    }
    if (noise > 1) {
        noise = 1
    }
    if (start >= 0 && number > 0) {
        on = 1
        : randomize the first spike so on average it occurs at
        : start + noise*interval
        event = start + invl(interval) - interval*(1. - noise)
        : but not earlier than 0
        if (event < 0) {
            event = 0
        }
        net_send(event, 3)
    }
}

PROCEDURE init_sequence(t(ms)) {
    if (number > 0) {
        on = 1
        event = 0
        ispike = 0
    }
}

FUNCTION invl(mean (ms)) (ms) {
    if (mean <= 0.) {
        mean = .01 (ms) : I would worry if it were 0.
    }
    if (noise == 0) {
        invl = mean
    } else {
        invl = (1. - noise)*mean + mean*erand()/k
    }
}

FUNCTION erand() {
LOCAL x,v,u,break
VERBATIM
    if (_p_donotuse) {
        /*
        :Supports separate independent but reproducible streams for
        : each instance. However, the corresponding hoc Random
        : distribution MUST be set to Random.negexp(1)
        */
    double x,v,u;
#if !NRNBBCORE
        if (_ran_compat == 2) {
            nrnran123_State* state = reinterpret_cast<nrnran123_State*>(_p_donotuse);
            //_lerand = nrnran123_negexp(reinterpret_cast<nrnran123_State*>(_p_donotuse));
            while(true) {
                x = nrnran123_normal(state);
                v = (1.0 + gammac*x)*(1.0 + gammac*x)*(1.0 + gammac*x);
                if(v<0) continue;
                u = nrnran123_dblpick(state);
                if(u < 1.0 - (0.0331*x)*(0.0331*x)*(0.0331*x)*(0.0331*x) ||
                    log(u) < 0.5*x*x + gammad*(1.0 - v + log(v))) {
                    if(k < 1)
                        return gammad*v*pow(nrnran123_dblpick(state),1.0/k);
                    else
                        return gammad*v;
                }
            }

        } else {
            return nrn_random_pick(reinterpret_cast<Rand*>(_p_donotuse));
        }
#else
        //_lerand = nrnran123_negexp(reinterpret_cast<nrnran123_State*>(_p_donotuse));
        nrnran123_State* state = reinterpret_cast<nrnran123_State*>(_p_donotuse);
        while(true) {
            x = nrnran123_normal(state);
            v = (1.0 + gammac*x)*(1.0 + gammac*x)*(1.0 + gammac*x);
            if(v<0) continue;
            u = nrnran123_dblpick(state);
            if( (u < 1.0 - (0.0331*x)*(0.0331*x)*(0.0331*x)*(0.0331*x)) ||
                (log(u) < 0.5*x*x + gammad*(1.0 - v + log(v)))) {
                if(k < 1.0)
                    return gammad*v*pow(nrnran123_dblpick(state),1.0/k);
                else
                    return gammad*v;
            }
        }
#endif
    } else {
#if NRNBBCORE
        assert(0);
#else
        /*
        : the old standby. Cannot use if reproducible parallel sim
        : independent of nhost or which host this instance is on
        : is desired, since each instance on this cpu draws from
        : the same stream
        */
#endif
    }
#if !NRNBBCORE
ENDVERBATIM
    break = true 
    while(break) {
        x = normrand(0,1) 
        v = (1.0 + gammac*x)*(1.0 + gammac*x)*(1.0 + gammac*x)
        if(v>0) {
            u = scop_random()
            if((u < 1.0 - (0.0331*x)*(0.0331*x)*(0.0331*x)*(0.0331*x)) ||
               (log(u) < 0.5*x*x + gammad*(1.0 - v + log(v)))) {
                if(k < 1) {
                    erand = gammad*v*pow(scop_random(), 1.0/k)
                } else {
                    erand = gammad*v
                }
                break = false
            }
        }
    }

VERBATIM
#endif
ENDVERBATIM
}

PROCEDURE noiseFromRandom() {
VERBATIM
#if !NRNBBCORE
 {
    if (_ran_compat == 2) {
        fprintf(stderr, "NetStim.noiseFromRandom123 was previously called\n");
        assert(0);
    }
    _ran_compat = 1;
    auto& randstate = reinterpret_cast<Rand*&>(_p_donotuse);
    if (ifarg(1)) {
        randstate = nrn_random_arg(1);
    } else {
        randstate = nullptr;
    }
 }
#endif
ENDVERBATIM
}

PROCEDURE noiseFromRandom123() {
VERBATIM
#if !NRNBBCORE
    if (_ran_compat == 1) {
        fprintf(stderr, "NetStim.noiseFromRandom was previously called\n");
        assert(0);
    }
    _ran_compat = 2;
    auto& r123state = reinterpret_cast<nrnran123_State*&>(_p_donotuse);
    if (r123state) {
        nrnran123_deletestream(r123state);
        r123state = nullptr;
    }
    if (ifarg(3)) {
        r123state = nrnran123_newstream3(static_cast<uint32_t>(*getarg(1)), static_cast<uint32_t>(*getarg(2)), static_cast<uint32_t>(*getarg(3)));
    } else if (ifarg(2)) {
        r123state = nrnran123_newstream(static_cast<uint32_t>(*getarg(1)), static_cast<uint32_t>(*getarg(2)));
    }
#endif
ENDVERBATIM
}

DESTRUCTOR {
VERBATIM
    if (!noise) { return; }
    if (_p_donotuse) {
#if NRNBBCORE
        { /* but note that mod2c does not translate DESTRUCTOR */
#else
        if (_ran_compat == 2) {
#endif
            auto& r123state = reinterpret_cast<nrnran123_State*&>(_p_donotuse);
            nrnran123_deletestream(r123state);
            r123state = nullptr;
        }
    }
ENDVERBATIM
}

VERBATIM
static void bbcore_write(double* x, int* d, int* xx, int *offset, _threadargsproto_) {
    if (!noise) { return; }
    /* error if using the legacy scop_exprand */
    if (!_p_donotuse) {
        fprintf(stderr, "NetStim: cannot use the legacy scop_negexp generator for the random stream.\n");
        assert(0);
    }
    if (d) {
        char which;
        uint32_t* di = reinterpret_cast<uint32_t*>(d) + *offset;
#if !NRNBBCORE
        if (_ran_compat == 1) {
            auto* rand = reinterpret_cast<Rand*>(_p_donotuse);
            /* error if not using Random123 generator */
            if (!nrn_random_isran123(rand, di, di+1, di+2)) {
                fprintf(stderr, "NetStim: Random123 generator is required\n");
                assert(0);
            }
            nrn_random123_getseq(rand, di+3, &which);
            di[4] = which;
        } else {
#else
    {
#endif
            auto& r123state = reinterpret_cast<nrnran123_State*&>(_p_donotuse);
            nrnran123_getids3(r123state, di, di+1, di+2);
            nrnran123_getseq(r123state, di+3, &which);
            di[4] = which;
#if NRNBBCORE
            /* CoreNEURON does not call DESTRUCTOR so... */
            nrnran123_deletestream(r123state);
            r123state = nullptr;
#endif
        }
        /*printf("Netstim bbcore_write %d %d %d\n", di[0], di[1], di[3]);*/
    }
    *offset += 5;
}

static void bbcore_read(double* x, int* d, int* xx, int* offset, _threadargsproto_) {
    if (!noise) { return; }
    /* Generally, CoreNEURON, in the context of psolve, begins with an empty
     * model, so this call takes place in the context of a freshly created
     * instance and _p_donotuse is not NULL.
     * However, this function is also now called from NEURON at the end of
     * coreneuron psolve in order to transfer back the nrnran123 sequence state.
     * That allows continuation with a subsequent psolve within NEURON or
     * properly transfer back to CoreNEURON if we continue the psolve there.
     * So now, extra logic is needed for this call to work in a NEURON context.
     */
    uint32_t* di = reinterpret_cast<uint32_t*>(d) + *offset;
#if NRNBBCORE
    auto& r123state = reinterpret_cast<nrnran123_State*&>(_p_donotuse);
    assert(!r123state);
    r123state = nrnran123_newstream3(di[0], di[1], di[2]);
    nrnran123_setseq(r123state, di[3], di[4]);
#else
    uint32_t id1, id2, id3;
    assert(_p_donotuse);
    if (_ran_compat == 1) { /* Hoc Random.Random123 */
        auto* pv = reinterpret_cast<Rand*>(_p_donotuse);
        int b = nrn_random_isran123(pv, &id1, &id2, &id3);
        assert(b);
        nrn_random123_setseq(pv, di[3], (char)di[4]);
    } else {
        assert(_ran_compat == 2);
        auto* r123state = reinterpret_cast<nrnran123_State*>(_p_donotuse);
        nrnran123_getids3(r123state, &id1, &id2, &id3);
        nrnran123_setseq(r123state, di[3], di[4]);
    }
    /* Random123 on NEURON side has same ids as on CoreNEURON side */
    assert(di[0] == id1 && di[1] == id2 && di[2] == id3);
#endif
    *offset += 5;
}
ENDVERBATIM

PROCEDURE next_invl() {
    if (number > 0) {
        event = invl(interval)
    }
    if (ispike >= number) {
        on = 0
    }
}

NET_RECEIVE (w) {
    if (flag == 0) { : external event
        if (w > 0 && on == 0) { : turn on spike sequence
            : but not if a netsend is on the queue
            init_sequence(t)
            : randomize the first spike so on average it occurs at
            : noise*interval (most likely interval is always 0)
            next_invl()
            event = event - interval*(1. - noise)
            net_send(event, 1)
        }else if (w < 0) { : turn off spiking definitively
            on = 0
        }
    }
    if (flag == 3) { : from INITIAL
        if (on == 1) { : but ignore if turned off by external event
            init_sequence(t)
            net_send(0, 1)
        }
    }
    if (flag == 1 && on == 1) {
        ispike = ispike + 1
        net_event(t)
        next_invl()
        if (on == 1) {
            net_send(event, 1)
        }
    }
}

FUNCTION bbsavestate() {
    bbsavestate = 0
    : limited to noiseFromRandom123
VERBATIM
#if !NRNBBCORE
    if (_ran_compat == 2) {
        auto r123state = reinterpret_cast<nrnran123_State*>(_p_donotuse);
        if (!r123state) { return 0.0; }
        double* xdir = hoc_pgetarg(1);
        if (*xdir == -1.) {
            *xdir = 2;
            return 0.0;
        }
        double* xval = hoc_pgetarg(2);
        if (*xdir == 0.) {
            char which;
            uint32_t seq;
            nrnran123_getseq(r123state, &seq, &which);
            xval[0] = seq;
            xval[1] = which;
        }
        if (*xdir == 1) {
        nrnran123_setseq(r123state, xval[0], xval[1]);
        }
    }
#endif
ENDVERBATIM
}


COMMENT
Presynaptic spike generator
---------------------------

This mechanism has been written to be able to use synapses in a single
neuron receiving various types of presynaptic trains.  This is a "fake"
presynaptic compartment containing a spike generator.  The trains
of spikes can be either periodic or noisy (Poisson-distributed)

Parameters;
   noise: 	between 0 (no noise-periodic) and 1 (fully noisy)
   interval: 	mean time between spikes (ms)
   number: 	number of spikes (independent of noise)

Written by Z. Mainen, modified by A. Destexhe, The Salk Institute

Modified by Michael Hines for use with CVode
The intrinsic bursting parameters have been removed since
generators can stimulate other generators to create complicated bursting
patterns with independent statistics (see below)

Modified by Michael Hines to use logical event style with NET_RECEIVE
This stimulator can also be triggered by an input event.
If the stimulator is in the on==0 state (no net_send events on queue)
 and receives a positive weight
event, then the stimulator changes to the on=1 state and goes through
its entire spike sequence before changing to the on=0 state. During
that time it ignores any positive weight events. If, in an on!=0 state,
the stimulator receives a negative weight event, the stimulator will
change to the on==0 state. In the on==0 state, it will ignore any ariving
net_send events. A change to the on==1 state immediately fires the first spike of
its sequence.

ENDCOMMENT
