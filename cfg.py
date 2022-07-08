import sys, os
from netpyne import specs
from netpyne.specs import simConfig

cfg = specs.SimConfig()

# simulation configuration
cfg.duration = 10_000
cfg.dt = 0.05
cfg.recordStep = 0.25
cfg.simLabel = "07jul22Gq"
cfg.saveFolder = cfg.simLabel
cfg.verbose = False
cfg.savePickle = True 
cfg.recordStim = True

# recording
cfg.recordCells = ["all"]
cfg.recordTraces = {
    "V_soma": {"sec": "soma", "loc": 0.5, "var": "v"},
    'cai':{'sec': 'soma','loc': 0.5,'var': 'cai'},
    'AngII':{'sec': 'soma','loc': 0.5,'var': 'AngIIi'},
    'Kv': {'sec': 'soma','loc': 0.5,'var': 'Kvi'},
    'Kv1': {'sec': 'soma','loc': 0.5,'var': 'Kv1i'},
    'Kv2': {'sec': 'soma','loc': 0.5,'var': 'Kv2i'},
    'Kv12': {'sec': 'soma','loc': 0.5,'var': 'Kv12i'}
    }
"""
    "epas": {"sec": "soma", "loc": 0.5, "var": "e_pas"},
    "ih": {"sec": "soma", "loc": 0.5, "var": "iother"},
    "ina": {"sec": "soma", "loc": 0.5, "var": "ina"},
    "ica": {"sec": "soma", "loc": 0.5, "var": "ica"},
    "ik": {"sec": "soma", "loc": 0.5, "var": "ik"},
    "ipas": {"sec": "soma", "loc": 0.5, "var": "i_pas"},
    "ica1a": {"sec": "soma", "loc": 0.5, "var": "ica1a_ch_Cacna1a_cp5"},
    "ica1b": {"sec": "soma", "loc": 0.5, "var": "ica1b_ch_Cacna1b_cp6"},
    "ica1c": {"sec": "soma", "loc": 0.5, "var": "ica1c_ch_Cacna1c_cp3"},
    "ica1d": {"sec": "soma", "loc": 0.5, "var": "ica1d_ch_Cacna1d_md150284"},
    "ica1g": {"sec": "soma", "loc": 0.5, "var": "ica1g_ch_Cacna1g_cp41"},
    "ica1i": {"sec": "soma", "loc": 0.5, "var": "ica1i_ch_Cacna1i_md279"},
    "ihcn1": {"sec": "soma", "loc": 0.5, "var": "ihcn1_ch_Hcn1_cp9"},
    "ihcn2": {"sec": "soma", "loc": 0.5, "var": "ihcn2_ch_Hcn2_cp10"},
    "ihcn3": {"sec": "soma", "loc": 0.5, "var": "ihcn3_ch_Hcn3_cp11"},
    "ihcn4": {"sec": "soma", "loc": 0.5, "var": "ihcn4_ch_Hcn4_cp12"},
    "ikcna": {"sec": "soma", "loc": 0.5, "var": "ikcna_ch_Kcna1ab1_md80769"},
    # 'ikcna':{'sec': 'soma', 'loc': 0.5,'var': 'ikcna_ch_Kcna1_rothman'},
    # 'ikcna':{'sec': 'soma', 'loc': 0.5,'var': 'ikcna_ch_Kcna1_gupta'},
    "ikcnc": {"sec": "soma", "loc": 0.5, "var": "ikcnc_ch_Kcnc1_rothman"},
    "ikcnj3": {"sec": "soma", "loc": 0.5, "var": "ikcnj3_ch_Kcnj3_md2488"},
}
"""
cfg.recordStim = True
cfg.analysis["plotTraces"] = {"include": [0], "saveFig": False}
cfg.analysis["plotRaster"] = {"saveFig": False}
cfg.saveDataInclude = ["simData", "simConfig", "netParams", "net"]

# globals
cfg.hParams = {"celsius": 35, "v_init": -61}

# cell id
cfg.cellnum = 1

# cell size
cfg.sze = 21

# modulation
cfg.npy = 0
cfg.ach = 0
cfg.ne = 0
cfg.angII = 10

# stimulus

cfg.hyp = 0.0
cfg.amp = 0
cfg.rate = 5.0
interval = 1000 / cfg.rate
cfg.noise = 0  # 1 - 10 / interval  # 10ms min interval
cfg.weight = 1e-2  # 0.0184014564752578
interval = 1000.0 / cfg.rate
cfg.delay = 5
cfg.e = -7.0
cfg.tau1 = 5
cfg.tau2 = 18

"""
# power-law synapse model
cfg.stim = "dexp2syn"
cfg.rrate = 0.31177 / 0.43708360077316477  # for hyp=0
cfg.d = 0.15
"""

# exp synapse model
cfg.stim = "fdexp2syn"
cfg.tau_D1 = 3000  # 2145.7055888921022
cfg.tau_D2 = 100
cfg.tau_F = 10
cfg.d1 = 0.62
cfg.d2 = 1.0
cfg.f = 0.0

# channel parameters
cfg.phi = 0.2

cfg.na = 1

cfg.ka = 0.018
cfg.kc = 0.018
cfg.kj = 0.0018

cfg.h1 = 0.00001
cfg.h2 = 0.009
cfg.h3 = 0.0001
cfg.h4 = 0.0002

cfg.c1i = 0.00027
cfg.c1g = 0.00001
cfg.c1d = 1.7e-4
cfg.c1c = 0.0001
cfg.c1b = 0.0001
cfg.c1a = 0.00001
