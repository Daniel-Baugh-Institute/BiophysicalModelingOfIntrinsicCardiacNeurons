from netpyne import sim
from neuron import h
import numpy as np
from scipy.stats import kendalltau

h.load_file("mod/nte.hoc")


def calcNTE(NA, DMV, typeM, typeP, bins, numShuffle=200):
    hstP, _ = np.histogram(typeP, bins=bins)
    hstM, _ = np.histogram(typeM, bins=bins)
    hstNA, _ = np.histogram(NA, bins=bins)
    hstDMV, _ = np.histogram(DMV, bins=bins)

    NA = h.Vector().from_python(hstNA)
    DMV = h.Vector().from_python(hstDMV)
    P = h.Vector().from_python(hstP)
    M = h.Vector().from_python(hstM)
    return [
        h.normte(NA, M, numShuffle).x[2],
        h.normte(DMV, P, numShuffle).x[2],
        h.normte(P, M, numShuffle).x[2],
        h.normte(DMV, M, numShuffle).x[2],
    ]


def calcTau(NA, DMV, typeM, typeP, bins):
    if len(bins) == 4:
        res = []
        hstDMV, _ = np.histogram(DMV, bins=bins[0])
        hstP, _ = np.histogram(typeP, bins=bins[0])
        res.append(kendalltau(hstDMV, hstP))

        hstM, _ = np.histogram(typeM, bins=bins[1])
        hstNA, _ = np.histogram(NA, bins=bins[1])
        res.append(kendalltau(hstM, hstNA))

        hstP, _ = np.histogram(typeP, bins=bins[2])
        hstM, _ = np.histogram(typeM, bins=bins[2])
        res.append(kendalltau(hstP, hstM))

        hstDMV, _ = np.histogram(DMV, bins=bins[3])
        hstM, _ = np.histogram(typeM, bins=bins[3])
        res.append(kendalltau(hstDMV, hstM))
        return res
    hstP, _ = np.histogram(typeP, bins=bins[0])
    hstM, _ = np.histogram(typeM, bins=bins[0])
    hstNA, _ = np.histogram(NA, bins=bins[0])
    hstDMV, _ = np.histogram(DMV, bins=bins[0])
    return [
        kendalltau(hstNA, hstM).statistic,
        kendalltau(hstDMV, hstP).statistic,
        kendalltau(hstDMV, hstM).statistic,
        kendalltau(hstP, hstM).statistic,
    ]


def getTimes(nTE=None, tau=None):
    # params
    DMVCon = sim.cfg.DMVConvergence
    DMVDiv = sim.cfg.DMVDivergence
    duration = sim.cfg.duration
    cluster_size = sim.cfg.cluster_size
    Pcells = int(cluster_size * sim.cfg.phasic_ratio)

    # data
    ids = sim.simData["spkid"].as_numpy()
    st = sim.simData["spkt"].as_numpy()
    Ps = st[ids < Pcells]
    Ms = st[(ids >= Pcells) * (ids < cluster_size)]
    DmvSz = int(np.ceil(DMVCon * Pcells / DMVDiv))
    Dmv = st[(ids >= cluster_size) * (ids < cluster_size + DmvSz)]
    Na = st[ids >= cluster_size + DmvSz]
    tauNaM, tauDmvP, tauDmvM, tauPM = [], [], [], []
    if tau is not None:
        for sz in tau:
            binsTau = np.linspace(0, duration, 1 + int(duration / sz))
            tNaM, tDmvP, tDmvM, tPM = calcTau(Na, Dmv, Ms, Ps, [binsTau])
            tauNaM.append(tNaM)
            tauDmvP.append(tDmvP)
            tauDmvM.append(tDmvM)
            tauPM.append(tPM)
    nTENaM, nTEDmvP, nTEDmvM, nTEPM = [], [], [], []
    if nTE is not None:
        for sz in nTE:
            binsNTE = np.linspace(0, duration, 1 + int(duration / sz))
            nNaM, nDmvP, nPM, nDmvM = calcNTE(Na, Dmv, Ms, Ps, binsNTE)
            nTENaM.append(nNaM)
            nTEDmvP.append(nDmvP)
            nTEPM.append(nPM)
            nTEDmvM.append(nDmvM)

    return (
        {
            "NA0": {"cluster0_M": tauNaM},
            "DMV0": {"cluster0_P": tauDmvP, "cluster0_M": tauDmvM},
            "cluster0_P": {"cluster0_M": tauPM},
        },
        {
            "NA0": {"cluster0_M": nTENaM},
            "DMV0": {"cluster0_P": nTEDmvP, "cluster0_M": nTEDmvM},
            "cluster0_P": {"cluster0_M": nTEPM},
        },
    )


def fi(cells):
    """set steady state RMP for 1 cell"""
    for c in cells:

        # skip artificial cells
        if not hasattr(c.secs, "soma"):
            continue
        seg = c.secs.soma.hObj(0.5)
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
                (-(10000) * seg.ica / (2 * h.FARADAY * seg.depth_cadad))
                * seg.taur_cadad
            )
        for modulation in netParams.neuromod.values():
            for mod, param in modulation.items():
                if hasattr(seg, mod):
                    for k, v in param.items():
                        setattr(getattr(seg, mod), k, v)


def simSim(np0, sc0):

    sim.create(netParams=np0, simConfig=sc0)
    fih = [h.FInitializeHandler(2, lambda: fi(sim.net.cells))]
    print("BEFORE simulate")
    sim.simulate()
    sim.analyze()
    sim.saveData()
    clusters = list(netParams.popParams)
    sources = list(netParams.stimSourceParams)
    h.load_file("mod/nte.hoc")
    with open(f"{sim.cfg.filename}_nte.csv", "w") as f:
        # header
        for label in sources + clusters:
            f.write(f"{label},")
        f.write("avgRate\n")

        rates = sim.analysis.popAvgRates()
        # nTE data
        for target in clusters:
            f.write(f"{target}")
            for src in sources + clusters:
                if src in sim.cfg.nTEBins and target in sim.cfg.nTEBins[src]:
                    nte = sim.analysis.nTE(
                        cells1=[src],
                        cells2=[target],
                        numShuffle=200,
                        binSize=sim.cfg.nTEBins[src][target],
                    )
                else:
                    nte = None
                f.write(f",{nte}")
            f.write(f",{rates[target]}\n")

    if hasattr(cfg, "nTERange"):
        with open(f"{sim.cfg.filename}_nTE_timescales.csv", "w") as f:
            sizes = np.linspace(*cfg.nTERange)
            _, nTE = getTimes(nTE=sizes)
            f.write("source, target, ")
            for sz in sizes:
                f.write(f"{sz}, ")
            for src, dat in nTE.items():
                for tar, val in dat.items():
                    f.write(f"{src}, {tar}, ")
                    for v in val:
                        f.write(f"{v}, ")
                    f.write("\n")
    if hasattr(cfg, "tauRange"):
        with open(f"{sim.cfg.filename}_tau_timescales.csv", "w") as f:
            sizes = np.linspace(*cfg.tauRange)
            tau, _ = getTimes(tau=sizes)
            f.write("source, target, ")
            for sz in sizes:
                f.write(f"{sz}, ")
            for src, dat in tau.items():
                for tar, val in dat.items():
                    f.write(f"{src}, {tar}, ")
                    for v in val:
                        f.write(f"{v}, ")
                    f.write("\n")
    print("AFTER save")
    for k, v in sim.timingData.items():
        print(f"{k}: {v:.2f} sec")


simConfig, netParams = sim.readCmdLineArgs(
    simConfigDefault="cfg.py", netParamsDefault="netParams_M1.py"
)
simSim(netParams, simConfig)
