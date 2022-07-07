import sys, os
from netpyne import specs
from netpyne.specs import simConfig

cfg = specs.SimConfig()

# simulation configuration
cfg.duration = 1_000
cfg.dt = 0.025
cfg.recordStep = 0.05
cfg.simLabel = "22apr11net"
cfg.saveFolder = cfg.simLabel
cfg.verbose = False
cfg.saveJson = True
cfg.recordStim = True

# recording
cfg.recordCells = ["cluster0_typeT"]
cfg.recordTraces = {
    "V_soma": {"sec": "soma", "loc": 0.5, "var": "v"},
    "isyn": {"synMech": "exc", "var": "i"},
    "gsyn": {"synMech": "exc", "var": "g"},
    "ica1a": {"sec": "soma", "loc": 0.5, "var": "ica1a_ch_Cacna1a_cp5"},
    "ica1b": {"sec": "soma", "loc": 0.5, "var": "ica1b_ch_Cacna1b_cp6"},
    "ica1c": {"sec": "soma", "loc": 0.5, "var": "ica1c_ch_Cacna1c_cp3"},
    "ica1d": {"sec": "soma", "loc": 0.5, "var": "ica1d_ch_Cacna1d_md150284"},
    "ica1g": {"sec": "soma", "loc": 0.5, "var": "ica1g_ch_Cacna1g_cp41"},
    "ica1i": {"sec": "soma", "loc": 0.5, "var": "ica1i_ch_Cacna1i_md279"},
}
"""
    #'cai':{'sec': 'soma','loc': 0.5,'var': 'cai'}}
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
cfg.analysis["plotRaster"] = {"saveFig": True}
cfg.saveDataInclude = ["simData", "simConfig", "netParams", "net"]

# globals
cfg.hParams = {"celsius": 35, "v_init": -61}

# ganglion parameters
cfg.num_cluster = 1
cfg.cluster_size = 100
cfg.SIFcount = 20
cfg.xRange = [[0,100]]
cfg.yRange = [[0,100]]
cfg.zRange = [[0,100]]

cfg.tonic_ratio = 13 / 32
cfg.tonic_cells = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    10,
    11,
    12,
    13,
    14,
    16,
    17,
    18,
    20,
    21,
    55,
    58,
]
cfg.cluster_shape = [100, 100, 100]
cfg.seed = 0

# cell size
cfg.sze = 21
cfg.SIFsze = 5


# modulation parameters
cfg.dx = 20
cfg.margin = 20

## Boundary/Initial conditions
cfg.BCne = 0.0
cfg.BCnpy = 0.0
cfg.BCach = 0.0
cfg.BCser = 0.0
cfg.BCda = 0.0

## Diffusion coefficients
cfg.Dne = 0.077 # Rice et al 1985
cfg.Dnpy = 1.31e-5  # Sanghaiv et al 1994 (check temperature)
D20 = 0.447 # (Sattarahmady et al 2013) room temperature ~20C?
eta20 = 10e-4 # Pa s
eta37 = 6.91e-4 # Pa s
cfg.Dach = D20 * ((274.15+37)/eta37) * (eta20)/(274.15+25)

eta25 = 8.9e-4 # Pa s
D25 = 0.54 # Gerhardt et al 1982
cfg.Dser = D25 * ((274.15+37)/eta37) * (eta25)/(274.15+25)
cfg.Dda = 0.068 # Rice et al 1985



# stimulus
cfg.hyp = 0.0
cfg.amp = 0
cfg.stim = "dexp2syn"
cfg.rate = 5.0
interval = 1000 / cfg.rate
cfg.noise = 1 - 10 / interval  # 10ms min interval
cfg.weight = 1e-2  # 0.0184014564752578
interval = 1000.0 / cfg.rate
cfg.delay = 5
cfg.e = -7.0
cfg.tau1 = 5
cfg.tau2 = 18
cfg.rrate = 0.31177 / 0.43708360077316477  # for hyp=0
cfg.d = 0.15

# phasic connections
cfg.phasic_rate = 5.0
interval = 1000 / cfg.phasic_rate
cfg.phasic_noise = 1 - 10 / interval  # 10ms min interval
cfg.phasic_weight = 0.07
cfg.phasic_delay = 5
cfg.phasic_phasic_prob = [0.25, 0.25]
cfg.phasic_phasic_weight = [0, 0.25]
cfg.phasic_phasic_delay = [5, 5]

cfg.phasic_tonic_prob = [0.25, 0.25]
cfg.phasic_tonic_weight = [5e-3, 0]
cfg.phasic_tonic_delay = [5, 5]


# tonic connections
cfg.tonic_rate = 5.0
interval = 1000 / cfg.tonic_rate
cfg.tonic_noise = 1 - 10 / interval  # 10ms min interval
cfg.tonic_weight = 0.07
cfg.tonic_delay = 5
cfg.tonic_tonic_prob = [0.25, 0.25]
cfg.tonic_tonic_weight = [0, 5e-3]
cfg.tonic_tonic_delay = [5, 5]

# SIF
cfg.SIFdelay = 5.0
cfg.SIFweight = 1.0
cfg.SIFprob = 1.0

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
