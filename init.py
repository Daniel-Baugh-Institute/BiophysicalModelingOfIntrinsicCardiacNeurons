from netpyne import sim
from neuron import h


def fi(seg):
    """set steady state RMP for 1 cell"""
    print(seg.v)
    isum = 0
    isum = (
        (seg.ina if h.ismembrane("na_ion") else 0)
        + (seg.ik if h.ismembrane("k_ion") else 0)
        + (seg.ica if h.ismembrane("ca_ion") else 0)
        + (seg.iother if h.ismembrane("other_ion") else 0)
    )
    seg.e_pas = cfg.hParams["v_init"] + isum / seg.g_pas
    if h.ismembrane("cadad"):
        seg.cainf_cadad = seg.cai - (
            (-(10000) * seg.ica / (2 * h.FARADAY * seg.depth_cadad)) * seg.taur_cadad
        )
    for modulation in netParams.neuromod.values():
        for mod, param in modulation.items():
            if hasattr(seg, mod):
                for k, v in param.items():
                    setattr(getattr(seg, mod), k, v)


def simSim(np0, sc0):
    sim.create(netParams=np0, simConfig=sc0)
    fih = [h.FInitializeHandler(2, lambda: fi(sim.net.cells[0].secs.soma.hObj(0.5)))]
    print("BEFORE simulate")
    sim.simulate()
    sim.analyze()
    sim.saveData()

    with open(f"{sim.cfg.filename}_nte.csv",'w') as f:
        for target in ['cluster0_phasic', 'cluster0_tonic']:
            for source in ['drive A', 'drive B', 'cluster0_phasic', 'cluster0_tonic']:
                nte = sim.analysis.nTE(cells1=[source],cells2=[target],numShuffle=200)
                f.write(f"{nte}, ")
            f.write("\n")
    print("AFTER save")
    for k, v in sim.timingData.items():
        print(f"{k}: {v:.2f} sec")


simConfig, netParams = sim.readCmdLineArgs(
    simConfigDefault="cfg.py", netParamsDefault="netParams_M1.py"
)
simSim(netParams, simConfig)
