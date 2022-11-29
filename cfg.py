import sys, os
from netpyne import specs
from netpyne.specs import simConfig

cfg = specs.SimConfig()

# simulation configuration
cfg.duration = 1_000
cfg.dt = 0.01
cfg.recordStep = 0.01
cfg.simLabel = "21nov22largenet"
cfg.saveFolder = cfg.simLabel
cfg.verbose = False
cfg.saveJson = True
cfg.recordStim = True


# recording
cfg.recordCells = ["cluster0_M", "cluster0_P"]
# cfg.recordTraces = {
#    "V_soma": {"sec": "soma", "loc": 0.5, "var": "v"},
#    "isyn": {"synMech": "exc", "var": "i"},
#    "gsyn": {"synMech": "exc", "var": "g"},
# }
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
# cfg.recordStim = True
# cfg.analysis["plotTraces"] = {"include": [0], "saveFig": False}
cfg.analysis["plotRaster"] = {"saveFig": True, "orderInverse": True}
cfg.saveDataInclude = ["simData"]  # , "simConfig", "netParams", "net"]

# globals
cfg.hParams = {"celsius": 35, "v_init": -61}

# ganglion parameters
cfg.num_cluster = 100
cfg.cluster_distribution = {'method': 'random_integers', 'low':1, 'high':200}
#cfg.cluster_size = 100

# phasic cell from 'Model P'
cfg.phasic_ratio = 19 / 32
cfg.phasic_cells = [
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    27,
    28,
    29,
    33,
    34,
    35,
    39,
    40,
    41,
    43,
    44,
    68,
    69,
    70,
    72,
    73,
    75,
    82,
    84,
    85,
    86,
    88,
    89,
    90,
    91,
    92,
    102,
]
cfg.seed = 0

# cell size
cfg.sze = 21

# modulation
cfg.npy = 0
cfg.ach = 0
cfg.ne = 0

# stimulus
cfg.hyp = 0
cfg.amp = 0
cfg.stim = "network"
cfg.tau1 = 5
cfg.tau2 = 18
cfg.tau_D1 = 2145.7055888921022
cfg.tau_D2 = 100
cfg.tau_F = 100
cfg.d2 = 1.0
cfg.f = 1.0
cfg.e = -7.0
cfg.d1 = 0.29403361433185227
cfg.tau_D1 = 165.6813123078298
cfg.weight = 0.04350521264848694


"""
cfg.tau1 = 5
cfg.tau2 = 18
cfg.rrate = 0.31177 / 0.43708360077316477  # for hyp=0
cfg.d = 0.15
cfg.e = -7.0
"""

# phasic connections
cfg.phasic_rate = 5.0
interval = 1000 / cfg.phasic_rate
cfg.phasic_noise = 1 - 10 / interval  # 10ms min interval
cfg.phasic_weight = 0.04350521264848694
cfg.phasic_delay = 5
cfg.phasic_phasic_prob = [0.25, 0.25]
cfg.phasic_phasic_weight = [0.02, 0.02]
cfg.phasic_phasic_delay = [5, 5]

cfg.phasic_mixed_prob = [0.25, 0.25]
cfg.phasic_mixed_weight = [0.02, 0.02]
cfg.phasic_mixed_delay = [5, 5]


# mixed connections
cfg.mixed_rate = 5.0
interval = 1000 / cfg.mixed_rate
cfg.mixed_noise = 1 - 10 / interval  # 10ms min interval
cfg.mixed_weight = 0.04350521264848694
cfg.mixed_delay = 5
cfg.mixed_mixed_prob = [0.25, 0.25]
cfg.mixed_mixed_weight = [0.02, 0.02]
cfg.mixed_mixed_delay = [5, 5]

# channel parameters
cfg.na = 0.075  # 1

cfg.ka = 0.018
cfg.kc = 0.018
cfg.phi = 0.2
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
