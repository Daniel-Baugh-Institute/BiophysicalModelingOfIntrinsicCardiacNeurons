from netpyne import specs, sim
import numpy as np
from warnings import warn
import csv
from collections import defaultdict

netParams = specs.NetParams()
try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import (
        cfg,
    )  # if no simConfig in parent module, import directly from cfg.py:cfg

netParams.defaultThreshold = -10
# order in genemod MUST be preserved to match cell_identities channel order
# From 'Model P'
genemod = {
    "ch_Hcn3_cp11": {"gHCN3bar": 0.01},
    "ch_Hcn1_cp9": {"gHCN1bar": 0.003},
    "ch_Cacna1g_cp41": {"gCav3_1bar": 0.0003},
    "ch_Cacna1a_cp5": {"gCav2_1bar": 0.00005},
    "ch_Cacna1d_md150284": {"pcaLbar": 0.00045},
    "ch_Hcn4_cp12": {"gHCN4bar": 0.0035},
    "ch_Cacna1c_cp3": {"gLbar": 0.006},
    "ch_Cacna1i_md279": {"gcabar": 0.0006},
    "ch_Kcna1ab1_md80769": {"gbar": 0.018},
    "ch_Kcnj3_md2488": {"gbar": 0.0035},
    "ch_Cacna1b_cp6": {"gCav2_2bar": 0.0001},
    "ch_Hcn2_cp10": {"gHCN2bar": 0.009},  # 0.0011
    "ch_Kcnc1_rothman": {"gbar": 0.018, "phi": cfg.phi},
    "ch_Scn1a_cp35": {"gNabar": 0.075},
}  # 0.0015
cell_identities = np.bool_(
    np.transpose(np.genfromtxt("red_tdata_all_15_m2l.csv", delimiter=","))
)

## Cell parameters/rules
cell_base = {"secs": {}}

cell_base["secs"]["soma"] = {
    "geom": {"diam": cfg.sze, "L": cfg.sze, "Ra": 35.4, "cm": 1},
    "mechs": {"pas": {"g": 0.00078, "e": -65}, "nm_In_md149739": {"gbar": 0}},
}  # 1e-5


# mechanisms to modulate
netParams.neuromod = {
    "ach": {
        mech: {"ach": cfg.ach}
        for mech in ["ch_Cacna1a_cp5", "ch_Cacna1b_cp6", "ch_Kcnj3_md2488.mod"]
    },
    "npy": {
        mech: {"npy": cfg.npy}
        for mech in [
            "ch_Cacna1a_cp5",
            "ch_Cacna1b_cp6",
            "ch_Cacna1c_cp3",
            "ch_Hcn1_cp9",
            "ch_Hcn2_cp10",
            "ch_Hcn3_cp11",
            "ch_Hcn4_cp12",
        ]
    },
    "ne": {mech: {"ne": cfg.ne} for mech in ["ch_Cacna1b_cp6"]},
}
# add mechanism to the model -- blocked by default but can be changed by cfg
addtional_mech = {}

np.random.seed(cfg.seed)
cfg.seeds.conn = cfg.seed
cfg.seeds.stim = cfg.seed
cfg.seeds.loc = cfg.seed

mixed_cells = [i for i in range(cell_identities.shape[0]) if i not in cfg.phasic_cells]
if hasattr(cfg, "cluster_distribution"):
    if hasattr(cfg, "cluster_size"):
        warn(
            "cfg has a cluster_distribution and a cluster_size, cluster_distribution is ignored"
        )
    else:
        rndgen = getattr(np.random, cfg.cluster_distribution["method"])
        cfg.cluster_size = rndgen(
            **{k: v for k, v in cfg.cluster_distribution.items() if k != "method"},
            size=int(cfg.num_cluster),
        )
for idx in range(cfg.num_cluster):
    cluster_size = (
        cfg.cluster_size[idx]
        if hasattr(cfg.cluster_size, "__len__")
        else cfg.cluster_size
    )
    phasic_count = int(cluster_size * cfg.phasic_ratio)
    mixed_count = cluster_size - phasic_count
    # generate a random sample of cell types
    cell_count = defaultdict(lambda: 0)
    for i in np.random.randint(len(cfg.phasic_cells), size=phasic_count):
        cell_count[cfg.phasic_cells[i]] += 1
    for i in np.random.randint(len(mixed_cells), size=mixed_count):
        cell_count[mixed_cells[i]] += 1

    # add population of each cell type to the cluster
    cells = {}
    for k, v in cell_count.items():
        CEL = cell_base.copy()
        for mod, onoff in zip(genemod, cell_identities[k]):
            if onoff:
                CEL["secs"]["soma"]["mechs"][mod] = genemod[mod]

        for mech, param in addtional_mech.items():
            CEL["soma"]["mechs"][mech] = param
        if k in cfg.phasic_cells:
            CEL["conds"] = {"cellType": "phasic"}
            CEL["diversityFraction"] = v / phasic_count
        else:
            CEL["conds"] = {"cellType": "mixed"}
            CEL["diversityFraction"] = v / mixed_count
        netParams.cellParams[f"CEL{k}"] = CEL
    netParams.popParams[f"cluster{idx}_P"] = {
        "cellType": "phasic",
        "numCells": phasic_count,
        "diversity": True,
    }
    netParams.popParams[f"cluster{idx}_M"] = {
        "cellType": "mixed",
        "numCells": mixed_count,
        "diversity": True,
    }


if cfg.stim == "IClamp":
    netParams.stimSourceParams["iclamp"] = {
        "type": "IClamp",
        "amp": cfg.amp,
        "dur": 400,
        "delay": 100,
    }
    netParams.stimTargetParams["iclamp->CEL"] = {
        "source": "iclamp",
        "conds": {"cellType": "CEL"},
        "sec": "soma",
        "loc": 0.5,
    }
elif cfg.stim == "exp2syn":
    netParams.synMechParams["exc"] = {
        "mod": "Exp2Syn",
        "tau1": cfg.tau1,
        "tau2": cfg.tau2,
        "e": cfg.e,
    }
    netParams.stimSourceParams["bkg"] = {
        "type": "NetStim",
        "rate": cfg.rate,
        "noise": cfg.noise,
    }
    netParams.stimTargetParams["bkg->exc"] = {
        "source": "bkg",
        "conds": {"cellType": "CEL"},
        "weight": cfg.weight,
        "delay": cfg.delay,
        "synMech": "exc",
    }
elif cfg.stim == "expsyn":
    netParams.synMechParams["exc"] = {"mod": "ExpSyn", "tau": cfg.tau1, "e": cfg.e}
    netParams.stimSourceParams["bkg"] = {
        "type": "NetStim",
        "rate": cfg.rate,
        "noise": cfg.noise,
    }
    netParams.stimTargetParams["bkg->exc"] = {
        "source": "bkg",
        "conds": {"cellType": "CEL"},
        "weight": cfg.weight,
        "delay": cfg.delay,
        "synMech": "exc",
    }
elif cfg.stim == "fdexp2syn":
    netParams.synMechParams["exc"] = {
        "mod": "FDSExp2Syn",
        "tau1": cfg.tau1,
        "tau2": cfg.tau2,
        "e": cfg.e,
        "f": cfg.f,
        "d1": cfg.d1,
        "d2": cfg.d2,
        "tau_F": cfg.tau_F,
        "tau_D1": cfg.tau_D1,
        "tau_D2": cfg.tau_D2,
    }
    netParams.stimSourceParams["bkg"] = {
        "type": "NetStim",
        "rate": cfg.rate,
        "noise": cfg.noise,
    }
    netParams.stimTargetParams["bkg->exc"] = {
        "source": "bkg",
        "conds": {"pop": "cluster0_M"},
        "weight": cfg.weight,
        "delay": cfg.delay,
        "synMech": "exc",
    }
elif cfg.stim == "dexp2syn":
    netParams.synMechParams["exc"] = {
        "mod": "DExp2Syn",
        "tau1": cfg.tau1,
        "tau2": cfg.tau2,
        "e": cfg.e,
        "d": cfg.d,
        "rrate": cfg.rrate,
    }
elif cfg.stim == "network":
    netParams.synMechParams["exc"] = {
        "mod": "FDSExp2Syn",
        "tau1": cfg.tau1,
        "tau2": cfg.tau2,
        "e": cfg.e,
        "f": cfg.f,
        "d1": cfg.d1,
        "d2": cfg.d2,
        "tau_F": cfg.tau_F,
        "tau_D1": cfg.tau_D1,
        "tau_D2": cfg.tau_D2,
    }
    for idx in range(cfg.num_cluster):
        netParams.popParams[f"DMV{idx}"] = {
            "cellModel": "GammaStim",
            "type": "NetStim",
            "k": cfg.DMVShape,
            "theta": cfg.DMVScale,
            "noise": cfg.DMVNoise,
            "number": max(10_000, 5 * cfg.duration),
            "numCells": 1
            + int(
                netParams.popParams[f"cluster{idx}_P"]["numCells"] / cfg.DMVDivergence
            ),
        }
        netParams.popParams[f"NA{idx}"] = {
            "cellModel": "NetStim",
            "type": "NetStim",
            "rate": cfg.NARate,
            "noise": cfg.NANoise,
            "number": max(10_000, 5 * cfg.duration),
            "numCells": 1
            + int(
                netParams.popParams[f"cluster{idx}_M"]["numCells"] / cfg.NADivergence
            ),
        }
        netParams.connParams[f"NA{idx}->M{idx}"] = {
            "preConds": {"pop": f"NA{idx}"},
            "postConds": {"pop": f"cluster{idx}_M"},
            "convergence": 1,
            "divergence": cfg.NADivergence,
            "weight": cfg.mixed_weight,
            "delay": cfg.mixed_delay,
            "synMech": "exc",
        }
        netParams.connParams[f"DMV{idx}->P{idx}"] = {
            "preConds": {"pop" : f"DMV{idx}"},
            "postConds": {"pop": f"cluster{idx}_P"},
            "weight": cfg.phasic_weight,
            "delay": cfg.phasic_delay,
            "convergence": 1,
            "divergence": cfg.DMVDivergence,
            "synMech": "exc",
        }
        for j in range(cfg.num_cluster):

            def getVal(param):
                p = eval(param) if isinstance(param, str) else param
                return p[idx == j] if hasattr(p, "__len__") else p

            netParams.connParams[f"P{idx}->P{j}"] = {
                "preConds": {"pop": f"cluster{idx}_P"},
                "postConds": {"pop": f"cluster{j}_P"},
                "probability": getVal(cfg.phasic_phasic_prob),
                "weight": getVal(cfg.phasic_phasic_weight),
                "delay": getVal(cfg.phasic_phasic_delay),
                "synMech": "exc",
            }

            netParams.connParams[f"P{idx}->M{j}"] = {
                "preConds": {"pop": f"cluster{idx}_P"},
                "postConds": {"pop": f"cluster{j}_M"},
                "probability": getVal(cfg.phasic_mixed_prob),
                "weight": getVal(cfg.phasic_mixed_weight),
                "delay": getVal(cfg.phasic_mixed_delay),
                "synMech": "exc",
            }

            netParams.connParams[f"M{idx}->M{j}"] = {
                "preConds": {"pop": f"cluster{idx}_M"},
                "postConds": {"pop": f"cluster{j}_M"},
                "probability": getVal(cfg.mixed_mixed_prob),
                "weight": getVal(cfg.mixed_mixed_weight),
                "delay": getVal(cfg.mixed_mixed_delay),
                "synMech": "exc",
            }


if cfg.hyp != 0:
    netParams.stimSourceParams["iclamp"] = {
        "type": "IClamp",
        "amp": cfg.hyp,
        "dur": 1e9,
        "delay": 100,
    }
    netParams.stimTargetParams["iclamp->CEL"] = {
        "source": "iclamp",
        "conds": {"cellType": "CEL"},
        "sec": "soma",
        "loc": 0.5,
    }


# 'ch_Kcna1ab1_md80769g':{'gbar': cfg.ka}
# 'ch_Scn1a_cp35':{'gNabar': cfg.na}
# 'ch_Scn1a_md264834':{'gNav11bar': cfg.na}
