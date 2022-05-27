import sys, os
from netpyne import specs
from netpyne.specs import simConfig
cfg = specs.SimConfig() 

cfg.hParams = {'celsius':35, 'v_init':-61}
cfg.duration = 1000  #1500 #1*1e3 #(ms)
cfg.dt = 0.025          
cfg.verbose = False     
cfg.recordCells = ['all']
cfg.recordTraces = {'V_soma':{'sec': 'soma','loc': 0.5,'var': 'v'},
                    # 'm_Na':{'sec': 'soma','loc': 0.5,'var': 'm_ch_Scn1a_cp35'},
                    # 'h_Na':{'sec': 'soma','loc': 0.5,'var': 'h_ch_Scn1a_cp35'}}
                         #'cai':{'sec': 'soma','loc': 0.5,'var': 'cai'}}
                       # 'epas' : {'sec': 'soma', 'loc': 0.5,'var': 'e_pas'},
                    'ih':{'sec': 'soma', 'loc': 0.5,'var': 'iother'}, 
                    'ina': {'sec': 'soma', 'loc': 0.5,'var': 'ina'},
                    'ica': {'sec': 'soma', 'loc': 0.5,'var': 'ica'},
                    'ik': {'sec': 'soma', 'loc': 0.5,'var': 'ik'},
                    'ipas':{'sec': 'soma', 'loc': 0.5,'var': 'i_pas'},
                    'ica1a':{'sec': 'soma', 'loc': 0.5,'var': 'ica1a_ch_Cacna1a_cp5'},
                    'ica1b':{'sec': 'soma', 'loc': 0.5,'var': 'ica1b_ch_Cacna1b_cp6'},
                    'ica1c':{'sec': 'soma', 'loc': 0.5,'var': 'ica1c_ch_Cacna1c_cp3'},
                    'ica1d':{'sec': 'soma', 'loc': 0.5,'var': 'ica1d_ch_Cacna1d_md150284'},
                    'ica1g':{'sec': 'soma', 'loc': 0.5,'var': 'ica1g_ch_Cacna1g_cp41'},
                    'ica1i':{'sec': 'soma', 'loc': 0.5,'var': 'ica1i_ch_Cacna1i_md279'},
                    'ihcn1':{'sec': 'soma', 'loc': 0.5,'var': 'ihcn1_ch_Hcn1_cp9'},
                    'ihcn2':{'sec': 'soma', 'loc': 0.5,'var': 'ihcn2_ch_Hcn2_cp10'},
                    'ihcn3':{'sec': 'soma', 'loc': 0.5,'var': 'ihcn3_ch_Hcn3_cp11'},
                    'ihcn4':{'sec': 'soma', 'loc': 0.5,'var': 'ihcn4_ch_Hcn4_cp12'},
                    'ikcna':{'sec': 'soma', 'loc': 0.5,'var': 'ikcna_ch_Kcna1ab1_md80769'},
                    'ikcnc':{'sec': 'soma', 'loc': 0.5,'var': 'ikcnc_ch_Kcnc1_rothman'},
                    'ikcnj3':{'sec': 'soma', 'loc': 0.5,'var': 'ikcnj3_ch_Kcnj3_md2488'}}

cfg.stim = 'VClamp' #'IClamp'  
cfg.vc = 0 
cfg.cellnum = 31
cfg.sze = 21
cfg.amp = 0.05 #-1e-5 #0.6
cfg.phi = 0.2

cfg.na = 0.1 #1

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

cfg.recordStep = 0.1       
# cfg.filename = '21sep14d/'
cfg.simLabel = 'h'
cfg.saveFolder = '22may23'
cfg.saveJson = True
cfg.analysis['plotTraces'] = {'include': [0], 'saveFig': False}
cfg.analysis['plotRaster'] = {'saveFig': False}         

cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']
