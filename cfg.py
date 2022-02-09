import sys, os
from netpyne import specs
from netpyne.specs import simConfig
cfg = specs.SimConfig() 

cfg.hParams = {'celsius':35, 'v_init':-61}
cfg.duration = 60000  #1500 #1*1e3 #(ms)
cfg.dt = 0.01
cfg.verbose = False     
cfg.recordCells = ['all']
cfg.recordTraces = {'V_soma':{'sec': 'soma','loc': 0.5,'var': 'v'},
                    'isyn' : {'synMech': 'exc', 'var': 'i'},
                    'gsyn' : {'synMech': 'exc', 'var': 'g'}}
"""
                     'cai':{'sec': 'soma','loc': 0.5,'var': 'cai'},
                     'epas' : {'sec': 'soma', 'loc': 0.5,'var': 'e_pas'},
                     'ih':{'sec': 'soma', 'loc': 0.5,'var': 'iother'}, 
                     'ina': {'sec': 'soma', 'loc': 0.5,'var': 'ina'},
                     'ica': {'sec': 'soma', 'loc': 0.5,'var': 'ica'},
                     'ik': {'sec': 'soma', 'loc': 0.5,'var': 'ik'},
                     'ipas':{'sec': 'soma', 'loc': 0.5,'var': 'i_pas'},
                     'ica1a':{'sec': 'soma', 'loc': 0.5,'var': 'ica1a_ch_Cacna1a_cp5'},
                     'ica1b':{'sec': 'soma', 'loc': 0.5,'var': 'ica1b_ch_Cacna1b_cp6'},
                     'ica1c':{'sec': 'soma', 'loc': 0.5,'var': 'ica1c_ch_Cacna1c_cp3'},
                     'ica1g':{'sec': 'soma', 'loc': 0.5,'var': 'ica1g_ch_Cacna1g_cp41'},
                     'ica1i':{'sec': 'soma', 'loc': 0.5,'var': 'ica1i_ch_Cacna1i_md279'},
                     'ihcn1':{'sec': 'soma', 'loc': 0.5,'var': 'ihcn1_ch_Hcn1_cp9'},
                     'ihcn2':{'sec': 'soma', 'loc': 0.5,'var': 'ihcn2_ch_Hcn2_cp10'},
                     'ihcn3':{'sec': 'soma', 'loc': 0.5,'var': 'ihcn3_ch_Hcn3_cp11'},
                     'ihcn4':{'sec': 'soma', 'loc': 0.5,'var': 'ihcn4_ch_Hcn4_cp12'},
                     'ikcna1':{'sec': 'soma', 'loc': 0.5,'var': 'ik_ch_Kcna1ab1_md80769'},
                     'ikcnc1':{'sec': 'soma', 'loc': 0.5,'var': 'ik_ch_Kcnc1_md74298'},
                     'ikcnd2':{'sec': 'soma', 'loc': 0.5,'var': 'ik_ch_Kcnd2_md143100'},
                     'ikcnq':{'sec': 'soma', 'loc': 0.5,'var': 'ik_ch_Kcnq1_md183949'},
                     'iscn1':{'sec': 'soma', 'loc': 0.5,'var': 'ina_ch_Scn1a_md264834'},
                     'ikar':{'sec': 'soma', 'loc': 0.5,'var': 'ik_KAAR_rybak'},
                     'ika':{'sec': 'soma', 'loc': 0.5,'var': 'ik_ka'}
                    }
cfg.stim = 'IClamp'
cfg.amp = 0.6  
"""

ih_scale=1
cfg.hyp = 0
cfg.stim = 'dexp2syn'
cfg.tau1 = 5
cfg.tau2 = 18
cfg.rrate = 0.31177/0.43708360077316477 # for hyp=0
cfg.d = 0.2
cfg.e = 0 
cfg.rate = 2.1
interval = 1000/cfg.rate
cfg.noise = 1-10/interval # 10ms min interval
cfg.weight = 0.055
cfg.delay = 5 
cfg.cellnum = 94
cfg.ka = 0.1100761264562606
cfg.na = 1.25*0.8412111341953278
cfg.kcnc = 0.5*0.012420394539833
cfg.kcnab = 0.0125053287744522
cfg.h1 = ih_scale*1.5432371459901335e-05
cfg.h2 = ih_scale*0.0554111278653144
cfg.h3 = ih_scale*0.0001832456760108
cfg.h4 = ih_scale*0.0006318431615829
cfg.c1a = 0.25*5.084903478622437e-05
cfg.c1b = 0.0009565910220146
cfg.c1c = 0.0002832042902708
cfg.c1g = 2.3639085143804552e-05
cfg.c1i = 0.0021365472203493

cfg.recordStep = 0.02
cfg.recordStim = True 
# cfg.filename = '21sep14d/'
cfg.simLabel = '09feb22_hyp0_w0055_d02'
cfg.saveFolder = cfg.simLabel
cfg.saveJson = True
cfg.analysis['plotTraces'] = {'include': [0], 'saveFig': False}
cfg.analysis['plotRaster'] = {'saveFig': False}         

cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']
