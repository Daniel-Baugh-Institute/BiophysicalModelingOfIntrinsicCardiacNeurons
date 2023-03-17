from netpyne import specs
from netpyne.batch import Batch
from cfg import cfg
from neuron import h
import numpy as np
import os

h.load_file("mod/nte.hoc")


def calcNTE(NA, DMV, typeM, typeP, bins, numShuffle=200):
    tNA = len(NA) > 0
    tDMV = len(DMV) > 0
    tM = len(typeM) > 0
    tP = len(typeP) > 0
    hstP, _ = np.histogram(typeP, bins=bins)
    hstM, _ = np.histogram(typeM, bins=bins)
    hstNA, _ = np.histogram(NA, bins=bins)
    hstDMV, _ = np.histogram(DMV, bins=bins)

    NA = h.Vector().from_python(hstNA)
    DMV = h.Vector().from_python(hstDMV)
    P = h.Vector().from_python(hstP)
    M = h.Vector().from_python(hstM)
    return [
        h.normte(NA, M, numShuffle).x[2] if tNA and tM else -1,
        h.normte(DMV, P, numShuffle).x[2] if tDMV and tP else -1,
        h.normte(P, M, numShuffle).x[2] if tP and tM else -1,
        h.normte(DMV, M, numShuffle).x[2] if tDMV and tM else -1,
    ]


def batch():
    # parameters space to explore

    params = specs.ODict()
    params["phasic_phasic_weight"] = [0, 1e-2]
    params["mixed_mixed_weight"] = [0, 1e-2]
    params["phasic_mixed_weight"] = [0, 1e-2]
    params["phasic_weight"] = [0, 1e-2]
    params["mixed_weight"] = [0, 1e-2]

    # fitness function
    fitnessFuncArgs = {}
    fitnessFuncArgs["maxFitness"] = 100_000
    fitnessFuncArgs["simConfig"] = {
        "cluster_size": cfg.cluster_size,
        "duration": cfg.duration,
        "phasic_ratio": cfg.phasic_ratio,
        "DMVDivergence": cfg.DMVDivergence,
        "NADivergence": cfg.NADivergence,
        "DMVConvergence": cfg.DMVConvergence,
        "NAConvergence": cfg.NAConvergence,
    }
    fitnessFuncArgs["binSize"] = list(range(10, 50, 5))
    fitnessFuncArgs["target"] = {"mean": 0.11, "var": 0.29**2}

    def fitnessFunc(sd, **kwargs):
        sc = kwargs["simConfig"]
        Pcells = int(sc["cluster_size"] * sc["phasic_ratio"])
        Mcells = sc["cluster_size"] - Pcells
        DMVcells = int(np.ceil(sc["DMVConvergence"] * Pcells / sc["DMVDivergence"]))
        NAcells = int(np.ceil(sc["NAConvergence"] * Mcells / sc["NADivergence"]))

        ids = np.array(sd["spkid"])
        st = np.array(sd["spkt"])
        typeP = ids < Pcells
        typeM = (ids >= Pcells) * (ids < sc["cluster_size"])
        typeDmv = (ids >= sc["cluster_size"]) * (ids < sc["cluster_size"] + DMVcells)
        typeNa = ids >= sc["cluster_size"] + DMVcells

        spkP = st[typeP]
        spkM = st[typeM]
        spkDmv = st[typeDmv]
        spkNa = st[typeNa]

        # caclulate nTE for each populations
        nTEmax = [0, 0, 0, 0] # ignore negative values
        nTEbin = [None, None, None, None]
        print(kwargs["binSize"], sc["duration"])
        for sz in kwargs["binSize"]:
            bins = np.linspace(0, sc["duration"], 1 + int(sc["duration"] / sz))
            ntes = calcNTE(spkNa, spkDmv, spkM, spkP, bins)
            for i, nte in enumerate(ntes):
                if nte > nTEmax[i]:
                    nTEmax[i] = nte
                    nTEbin[i] = sz

        nTENaM, nTEDmvP, nTEDmvM, nTEPM = nTEmax
        print(f"NA->M {nTENaM}, DMV->P {nTEDmvP}, DMV->M {nTEDmvM}, P->M {nTEPM}")
        # prioritize tranfer through the network
        weights = [1,1,3,1]
        fitness = [(np.exp(w*(1.0-nte)) -1.0) for nte,w in zip(nTEmax,weights)]
        print(nTEmax,fitness)
        fitnessN = sum(fitness)
        # calculate rates
        rateP = 1e3 * sum(spkP) / sc["duration"]
        rateM = 1e3 * sum(spkM) / sc["duration"]

        target = kwargs["target"]
        fitnessR = np.exp(abs(rateP - target["mean"]) / target["var"]) -1.0
        fitnessR += np.exp(abs(rateM - target["mean"]) / target["var"]) -1.0
        print(f"fitness, {fitnessN}, {fitnessR}")
        return min(fitnessN + min(100,fitnessR)/5.0, kwargs['maxFitness'])

    # create Batch object with paramaters to modify, and specifying files to use
    b = Batch(params=params, cfgFile="cfg.py", netParamsFile="netParams_M1.py")

    # Set output folder, grid method (all param combinations), and run configuration
    b.method = "optuna"
    b.runCfg = {
        "type": "mpi_direct",  #'hpc_slurm',
        "script": "init.py",
        # options required only for mpi_direct or hpc
        "mpiCommand": "",
        "nodes": 1,
        "coresPerNode": 1,
        # 'allocation': 'default',
        # 'email': 'salvadordura@gmail.com',
        # 'reservation': None,
        "folder": "/u/adam/models/ragp.network/"
        #'custom': 'export LD_LIBRARY_PATH="$HOME/.openmpi/lib"' # only for conda users
    }
    b.batchLabel = "16mar23fit"
    b.saveFolder = "/tera/" + os.getlogin() + "/" + b.batchLabel

    b.optimCfg = {
        "fitnessFunc": fitnessFunc,  # fitness expression (should read simData)
        "fitnessFuncArgs": fitnessFuncArgs,
        "maxFitness": fitnessFuncArgs["maxFitness"],
        "maxiters": 50_000, #    Maximum number of iterations (1 iteration = 1 function evaluation)
        "maxtime": 8*60*60,  #    Maximum time allowed, in seconds
        "maxiter_wait": 60*60,
        "time_sleep": 30,
    }

    # Run batch simulations
    b.run()


# Main code
if __name__ == "__main__":
    batch()  # 'simple' or 'complex'
