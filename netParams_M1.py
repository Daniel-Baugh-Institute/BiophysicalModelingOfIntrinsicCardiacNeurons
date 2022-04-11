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
}

# add mechanism to the model -- blocked by default but can be changed by cfg
addtional_mech = {}

np.random.seed(cfg.seed)
phasic_cells = [i for i in range(cell_identities.shape[0]) if i not in cfg.tonic_cells]
tonic_count = int(cfg.ganglion_size * cfg.tonic_ratio)
phasic_count = cfg.ganglion_size - tonic_count
for idx in range(cfg.num_ganglion):
    # generate a random sample of cell types
    cell_count = defaultdict(lambda: 0)
    for i in np.random.randint(len(cfg.tonic_cells), size=tonic_count):
        cell_count[cfg.tonic_cells[i]] += 1
    for i in np.random.randint(len(cfg.tonic_cells), size=phasic_count):
        cell_count[phasic_cells[i]] += 1

    # add population of each cell type to the ganglion
    cells = {}
    for k, v in cell_count.items():
        CEL = cell_base.copy()
        for mod, onoff in zip(genemod, cell_identities[k]):
            if onoff:
                CEL["secs"]["soma"]["mechs"][mod] = genemod[mod]

        for mech, param in addtional_mech.items():
            CEL["soma"]["mechs"][mech] = param
        netParams.cellParams[f"CEL{k}"] = CEL
        netParams.popParams[f"ganglion{idx}_CEL{k}"] = {
            "cellType": f"CEL{k}",
            "numCells": v,
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
        "conds": {"cellType": "CEL"},
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
    netParams.stimSourceParams["vagal"] = {
        "type": "NetStim",
        "rate": cfg.vagal_rate,
        "noise": cfg.vagal_noise,
    }

    vagal_cells = [f"CEL{i}" for i in cfg.tonic_cells]
    symp_cells = [
        f"CEL{i}" for i in range(cell_identities.shape[0]) if i not in cfg.tonic_cells
    ]

    vagal_pop = [f"ganglion0_CEL{i}" for i in cfg.tonic_cells]
    symp_pop = [
        f"ganglion0_CEL{i}"
        for i in range(cell_identities.shape[0])
        if i not in cfg.tonic_cells
    ]
    netParams.stimTargetParams["vagal->exc"] = {
        "source": "vagal",
        "conds": {"cellType": vagal_cells},
        "weight": cfg.vagal_weight,
        "delay": cfg.vagal_delay,
        "synMech": "exc",
    }
    netParams.stimSourceParams["symp"] = {
        "type": "NetStim",
        "rate": cfg.symp_rate,
        "noise": cfg.symp_noise,
    }
    netParams.stimTargetParams["symp->exc"] = {
        "source": "symp",
        "conds": {"cellType": symp_cells},
        "weight": cfg.symp_weight,
        "delay": cfg.symp_delay,
        "synMech": "exc",
    }
    netParams.connParams["symp->symp"] = {
        "preConds": {"cellType": symp_cells},
        "postConds": {"cellType": symp_cells},
        "probability": cfg.symp_symp_prob,
        "weight": cfg.symp_symp_weight,
        "delay": cfg.symp_symp_delay,
        "synMech": "exc",
    }

    netParams.connParams["symp->vagal"] = {
        "preConds": {"cellType": symp_cells},
        "postConds": {"cellType": symp_cells},
        "probability": cfg.symp_vagal_prob,
        "weight": cfg.symp_vagal_weight,
        "delay": cfg.symp_vagal_delay,
        "synMech": "exc",
    }

    netParams.connParams["vagal->vagal"] = {
        "preConds": {"cellType": vagal_cells},
        "postConds": {"cellType": vagal_cells},
        "probability": cfg.vagal_vagal_prob,
        "weight": cfg.vagal_vagal_weight,
        "delay": cfg.vagal_vagal_delay,
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
