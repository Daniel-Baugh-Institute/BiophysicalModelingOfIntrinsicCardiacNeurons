import sys, os
from netpyne import specs
from netpyne.specs import simConfig

cfg = specs.SimConfig()

# simulation configuration
cfg.duration = 21_000 
cfg.dt = 0.025
cfg.recordStep = 0.1
cfg.simLabel = "02may23test"
cfg.saveFolder = cfg.simLabel
cfg.verbose = False
cfg.saveJson = True
cfg.recordStim = True
cfg.log_weights = True  # all weights are log scaled -- to improve search
cfg.nTEBins = {'DMV0': {'cluster0_P':int(cfg.duration/42.6), 
                        'cluster0_M':int(cfg.duration/27.4)},
               'NA0': {'cluster0_M': int(cfg.duration/27.4)},
               'cluster0_P': {'cluster0_M':int(cfg.duration/7.6)}}


# recording
#cfg.recordCells = ["all"]
#cfg.recordTraces = {
#    "V_soma": {"sec": "soma", "loc": 0.5, "var": "v"}
#}
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
#cfg.analysis["plotTraces"] = {"include": [0], "saveFig": False}
#cfg.analysis["plotRaster"] = {"saveFig": True, "orderInverse": True}
cfg.saveDataInclude = ["simData", "simConfig"]  # , "simConfig", "netParams", "net"]

# globals
cfg.hParams = {"celsius": 35, "v_init": -61}

# ganglion parameters
cfg.num_cluster = 1
cfg.cluster_size = 100

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
cfg.seed = 1

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
# synapse model
cfg.tau1 = 5
cfg.tau2 = 18
cfg.e = -7
cfg.d1 = 0.6474533535872186
cfg.d2 = 0.9284955400450818
cfg.f = 0.850515710969614
cfg.tau_D1 = 159.33232548522594 
cfg.tau_D2 = 616.104732221748
cfg.tau_F = 19.001749499516244


# DMV (drive P) source statistics -- gamma distributed ISIs
shape, loc, theta = 7.757972182086119, 37.49386102382368, 31.14382919023644
interval = shape*theta
cfg.DMVShape = shape
cfg.DMVScale = theta
cfg.DMVNoise = 1.0 - loc/interval
cfg.DMVDivergence = 7
cfg.DMVConvergence = 1.34

# NA (drive M) source statistics -- exp distributed ISIs
scale, loc = 754.4866995207383, 105.7860115451731
interval = scale + loc
cfg.NARate = 1000/interval
cfg.NANoise = 1.0 - loc/interval

# NA Chemoreflex drive -- gamma distributed ISIs
"""
scale, loc = 14.24094070278148, 48.35404375879234
interval = scale + loc                                                          
cfg.NARate = 1000/interval                                                      
cfg.NANoise = 1.0 - loc/interval
"""
# NA Barroreflex drive -- gamma distributed ISIs
"""
shape, loc, theta = 1.518579064688518, 15.159890913518314, 14.220177825723088
interval = shape*theta
cfg.NAShape = shape
cfg.NAScale = theta
cfg.NANoise = 1.0 - loc/interval
"""
cfg.NADivergence = 30
cfg.NAConvergence = 1.32 
# phasic connections
cfg.phasic_weight = 4e-6 #0.00040247923847343216 #0.00058  
cfg.phasic_weight_var = 1e-3
cfg.phasic_delay = 5
cfg.phasic_phasic_prob = [0.25, 0.25]
cfg.phasic_phasic_weight = [5e-6, 5e-6]
cfg.phasic_phasic_weight_var = [1e-4, 1e-4]
cfg.phasic_phasic_delay = [5, 5]

cfg.phasic_mixed_prob = [0.25, 0.25]
cfg.phasic_mixed_weight = [2e-5, 2e-5]
cfg.phasic_mixed_weight_var = [5e-4, 5e-4]

cfg.phasic_mixed_delay = [5, 5]


# mixed connections
cfg.mixed_weight = 4e-6 #0.00027972942965111996 
cfg.mixed_weight_var = 1e-3 #1.0
cfg.mixed_delay = 5
cfg.mixed_mixed_prob = [0.25, 0.25]
cfg.mixed_mixed_weight = [5e-6, 5e-6]
cfg.mixed_mixed_weight_var = [5e-4, 5e-4]

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

