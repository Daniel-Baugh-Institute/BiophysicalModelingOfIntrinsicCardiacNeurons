from netpyne import specs, sim
import numpy as np
import csv
from collections import defaultdict

netParams = specs.NetParams()
try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import (
        cfg,
    )  # if no simConfig in parent module, import directly from cfg.py:cfg

# order in genemod MUST be preserved to match cell_identities channel order
genemod = {
    "ch_Cacna1a_cp5": {"gCav2_1bar": cfg.c1a},
    "ch_Cacna1b_cp6": {"gCav2_2bar": cfg.c1b},
    "ch_Cacna1c_cp3": {"gLbar": cfg.c1c},
    "ch_Cacna1d_md150284": {"pcaLbar": cfg.c1d},
    "ch_Cacna1g_cp41": {"gCav3_1bar": cfg.c1g},
    "ch_Cacna1i_md279": {"gcabar": cfg.c1i},
    "ch_Hcn1_cp9": {"gHCN1bar": cfg.h1},
    "ch_Hcn2_cp10": {"gHCN2bar": cfg.h2},
    "ch_Hcn3_cp11": {"gHCN3bar": cfg.h3},
    "ch_Hcn4_cp12": {"gHCN4bar": cfg.h4},
    "ch_Kcna1ab1_md80769": {"gbar": cfg.ka},
    "ch_Kcnc1_rothman": {"gbar": cfg.kc, "phi": cfg.phi},  # 0.0011
    "ch_Kcnj3_md2488": {"gbar": cfg.kj},
    "ch_Scn1a_md264834": {"gNav11bar": cfg.na},
}  # 0.0015
cell_identities = np.bool_(
    np.transpose(np.genfromtxt("red_tdata_all_15.csv", delimiter=","))
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
phasic_cells = [i for i in range(cell_identities.shape[0]) if i not in cfg.tonic_cells]
for idx in range(cfg.num_cluster):
    cluster_size = (
        cfg.cluster_size[idx]
        if hasattr(cfg.cluster_size, "__len__")
        else cfg.cluster_size
    )
    tonic_count = int(cluster_size * cfg.tonic_ratio)
    phasic_count = cluster_size - tonic_count
    # generate a random sample of cell types
    cell_count = defaultdict(lambda: 0)
    for i in np.random.randint(len(cfg.tonic_cells), size=tonic_count):
        cell_count[cfg.tonic_cells[i]] += 1
    for i in np.random.randint(len(phasic_cells), size=phasic_count):
        cell_count[phasic_cells[i]] += 1

    # add population of each cell type to the cluster
    cells = {}
    for k, v in cell_count.items():
        CEL = cell_base.copy()
        for mod, onoff in zip(genemod, cell_identities[k]):
            if onoff:
                CEL["secs"]["soma"]["mechs"][mod] = genemod[mod]

        for mech, param in addtional_mech.items():
            CEL["soma"]["mechs"][mech] = param
        if k in cfg.tonic_cells:
            CEL["conds"] = {"cellType": "tonic"}
            CEL["diversityFraction"] = v / tonic_count
        else:
            CEL["conds"] = {"cellType": "phasic"}
            CEL["diversityFraction"] = v / phasic_count
        netParams.cellParams[f"CEL{k}"] = CEL
    netParams.popParams[f"cluster{idx}_tonic"] = {
        "cellType": "tonic",
        "numCells": tonic_count,
        "diversity": True,
    }
    netParams.popParams[f"cluster{idx}_phasic"] = {
        "cellType": "tonic",
        "numCells": phasic_count,
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
        "conds": {"pop": "cluster0_tonic"},
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
    netParams.stimSourceParams["drive A"] = {
        "type": "NetStim",
        "rate": cfg.tonic_rate,
        "noise": cfg.tonic_noise,
    }

    netParams.stimSourceParams["drive B"] = {
        "type": "NetStim",
        "rate": cfg.phasic_rate,
        "noise": cfg.phasic_noise,
    }

    for idx in range(cfg.num_cluster):
        netParams.stimTargetParams[f"drive A->tonic{idx}"] = {
            "source": "drive A",
            "conds": {"pop": f"cluster{idx}_tonic"},
            "weight": cfg.tonic_weight,
            "delay": cfg.tonic_delay,
            "synMech": "exc",
        }
        netParams.stimTargetParams[f"drive B->phasic{idx}"] = {
            "source": "drive B",
            "conds": {"pop": f"cluster{idx}_phasic"},
            "weight": cfg.phasic_weight,
            "delay": cfg.phasic_delay,
            "synMech": "exc",
        }
        for j in range(cfg.num_cluster):
            def getVal(p):
                return p[idx==j] if hasattr(p,'__len__') else p
            netParams.connParams[f"phasic{idx}->phasic{j}"] = {
                "preConds": {"pop": f"cluster{idx}_phasic"},
                "postConds": {"pop": f"cluster{j}_phasic"},
                "probability": getVal(cfg.phasic_phasic_prob),
                "weight": getVal(cfg.phasic_phasic_weight),
                "delay": getVal(cfg.phasic_phasic_delay),
                "synMech": "exc",
            }

            netParams.connParams[f"phasic{idx}->tonic{j}"] = {
                "preConds": {"pop": f"cluster{idx}_phasic"},
                "postConds": {"pop": f"cluster{j}_tonic"},
                "probability": getVal(cfg.phasic_tonic_prob),
                "weight": getVal(cfg.phasic_tonic_weight),
                "delay": getVal(cfg.phasic_tonic_delay),
                "synMech": "exc",
            }

            netParams.connParams[f"tonic{idx}->tonic{j}"] = {
                "preConds": {"pop": f"cluster{idx}_tonic"},
                "postConds": {"pop": f"cluster{j}_tonic"},
                "probability": getVal(cfg.tonic_tonic_prob),
                "weight": getVal(cfg.tonic_tonic_weight),
                "delay": getVal(cfg.tonic_tonic_delay),
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

#'ch_Kcna1ab1_md80769':{'gbar': 0.011},
# 'ch_Kcna1_gupta':{'gbar': 0.011,'zeta':1}
# 'ch_Kcna_cp18':{'gKv1_1bar': 0.01},
# 'ch_Kcnc1_md74298':{'gk': cfg.kcnc}
