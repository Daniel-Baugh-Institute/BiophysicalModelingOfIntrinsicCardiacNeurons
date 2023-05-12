from netpyne import specs
from netpyne.batch import Batch
from scipy import stats
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
    params["phasic_phasic_weight"] = [-9, -3]
    params["phasic_phasic_weight_var"] = [-6, -3]
    params["mixed_mixed_weight"] = [-9, -3]
    params["mixed_mixed_weight_var"] = [-6, -3]
    params["phasic_mixed_weight"] = [-9, -3]
    params["phasic_mixed_weight_var"] = [-6, -3]
    params["phasic_weight"] = [-9, -3]
    params["phasic_weight_var"] = [-6, -3]
    params["mixed_weight"] = [-9, -3]
    params["mixed_weight_var"] = [-6, -3]

    # fitness function
    fitnessFuncArgs = {}
    fitnessFuncArgs["maxFitness"] = 1_000_000_000_000
    fitnessFuncArgs["simConfig"] = {
        "cluster_size": cfg.cluster_size,
        "duration": cfg.duration,
        "phasic_ratio": cfg.phasic_ratio,
        "DMVDivergence": cfg.DMVDivergence,
        "NADivergence": cfg.NADivergence,
        "DMVConvergence": cfg.DMVConvergence,
        "NAConvergence": cfg.NAConvergence,
    }
    fitnessFuncArgs["tinit"] = 1_000
    fitnessFuncArgs["binSize"] = list(range(10, 50, 5))
    fitnessFuncArgs["target"] = {
        "mean": 0.11,
        "var": 0.29**2,
        "n": 1.12009527,
        "p": 0.18394278,
    }

    def fitnessFunc(sd, **kwargs):
        sc = kwargs["simConfig"]
        Pcells = int(sc["cluster_size"] * sc["phasic_ratio"])
        Mcells = sc["cluster_size"] - Pcells
        DMVcells = int(np.ceil(sc["DMVConvergence"] * Pcells / sc["DMVDivergence"]))
        NAcells = int(np.ceil(sc["NAConvergence"] * Mcells / sc["NADivergence"]))
        tinit = kwargs["tinit"]
        target = kwargs["target"]
        duration = sc["duration"]

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

        # estimated spike count for 1min
        Pcount, Mcount = np.zeros(500), np.zeros(500)
        for idx in range(Pcells):
            count = np.round([60e3 * sum(ids == idx) / duration]).astype(int)
            if count < 500:
                Pcount[count] += 1
            else:
                Pcount[-1] += 1
        for idx in range(Pcells, sc["cluster_size"]):
            count = np.round([60e3 * sum(ids == idx) / duration]).astype(int)
            if count < 500:
                Mcount[count] += 1
            else:
                Mcount[-1] += 1

        cdf = stats.nbinom.cdf(range(500), target["n"], target["p"])
        Pks, Ppval = stats.kstest(Pcount, cdf)
        Mks, Mpval = stats.kstest(Mcount, cdf)
        print(f"Type P {Pks} {Ppval}")
        print(f"Type M {Mks} {Mpval}")
        # skip first second -- all synapses initially at max strength
        spkP = np.array(spkP[spkP > tinit]) - tinit
        spkM = np.array(spkM[spkM > tinit]) - tinit
        spkDmv = np.array(spkDmv[spkDmv > tinit]) - tinit
        spkNa = np.array(spkNa[spkNa > tinit]) - tinit

        # caclulate nTE for each populations
        nTEmax = [0, 0, 0, 0]  # ignore negative values
        nTEbin = [None, None, None, None]
        print(kwargs["binSize"], duration)
        for sz in kwargs["binSize"]:
            bins = np.linspace(0, duration - tinit, 1 + int((duration - tinit) / sz))
            ntes = calcNTE(spkNa, spkDmv, spkM, spkP, bins)
            for i, nte in enumerate(ntes):
                if nte > nTEmax[i]:
                    nTEmax[i] = nte
                    nTEbin[i] = sz

        nTENaM, nTEDmvP, nTEPM, nTEDmvM = nTEmax
        print(f"NA->M {nTENaM}, DMV->P {nTEDmvP}, DMV->M {nTEDmvM}, P->M {nTEPM}")
        # prioritize tranfer through the network
        weights = [100, 100, 100, 700]
        fitness = [
            w * (np.exp((1.0 - nte)) - 1.0) / (np.exp(1) - 1)
            for nte, w in zip(nTEmax, weights)
        ]
        print(nTEmax, fitness)
        fitnessN = sum(fitness)
        # calculate rates
        rateP = 1e3 * len(spkP) / (duration - tinit)
        rateM = 1e3 * len(spkM) / (duration - tinit)
        if rateP == 0 or rateM == 0:
            return kwargs["maxFitness"]
        print(f"P {rateP}\tM {rateM}")
        target = kwargs["target"]
        fitnessR = abs(rateP - target["mean"]) / target["var"]
        fitnessR += abs(rateM - target["mean"]) / target["var"]
        print(f"fitness, {fitnessN}, {fitnessR}, {1000*Pks}, {1000*Mks}")
        return min(
            fitnessN + 1000*fitnessR + 1000 * (Pks + Mks), kwargs["maxFitness"]
        )

    # create Batch object with paramaters to modify, and specifying files to use
    b = Batch(params=params, cfgFile="cfg.py", netParamsFile="netParams_M1.py")

    # Set output folder, grid method (all param combinations), and run configuration
    b.method = "optuna"
    b.runCfg = {
        "type": "hpc_slurm",
        "script": "init.py",
        # options required only for mpi_direct or hpc
        "mpiCommand": "",
        "nodes": 1,
        "coresPerNode": 1,
        "walltime": "0-00:20:00",
        "partition": "scavenge",
        "allocation": "mcdougal",
        # "email": "adam.newton@yale.edu",
        #'reservation': None,
        "folder": "/home/ajn48/project/ragp",
        "custom": """#SBATCH --partition=scavenge
#SBATCH --requeue
#module load miniconda
#module load OpenMPI/4.0.5-GCC-10.2.0 
#source /vast/palmer/apps/avx2/software/miniconda/23.1.0/etc/profile.d/conda.sh
#conda activate py310
"""
        #'custom': 'export LD_LIBRARY_PATH="$HOME/.openmpi/lib"' # only for conda users
    }
    b.batchLabel = "11may23log"
    print(f"/home/ajn48/palmer_scratch/{b.batchLabel}")
    b.saveFolder = "/home/ajn48/palmer_scratch/" + b.batchLabel

    b.optimCfg = {
        "fitnessFunc": fitnessFunc,  # fitness expression (should read simData)
        "fitnessFuncArgs": fitnessFuncArgs,
        "maxFitness": fitnessFuncArgs["maxFitness"],
        "maxiters": 3_000,  #    Maximum number of iterations (1 iteration = 1 function evaluation)
        "maxtime": 8 * 60 * 60,  #    Maximum time allowed, in seconds
        "maxiter_wait": 60 * 60,
        "time_sleep": 10,
    }

    # Run batch simulations
    b.run()


# Main code
if __name__ == "__main__":
    batch()  # 'simple' or 'complex'
