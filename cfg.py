import sys, os
from netpyne import specs
from netpyne.specs import simConfig
cfg = specs.SimConfig() 

cfg.hParams = {'celsius':35, 'v_init':-61}
cfg.duration = 1000  #1500 #1*1e3 #(ms)
cfg.dt = 0.025          
cfg.verbose = False     
cfg.recordCells = ['all']
cfg.recordTraces = {'V_soma':{'sec': 'soma','loc': 0.5,'var': 'v'}}
                        #'cai':{'sec': 'soma','loc': 0.5,'var': 'cai'}}
#                         'epas' : {'sec': 'soma', 'loc': 0.5,'var': 'e_pas'},
#                     'ih':{'sec': 'soma', 'loc': 0.5,'var': 'iother'}, 
#                     'ina': {'sec': 'soma', 'loc': 0.5,'var': 'ina'},
#                     'ica': {'sec': 'soma', 'loc': 0.5,'var': 'ica'},
#                     'ik': {'sec': 'soma', 'loc': 0.5,'var': 'ik'},
#                     'ipas':{'sec': 'soma', 'loc': 0.5,'var': 'i_pas'}}
                    # 'ica1a':{'sec': 'soma', 'loc': 0.5,'var': 'ica1a_ch_Cacna1a_cp5'},
                    # 'ica1b':{'sec': 'soma', 'loc': 0.5,'var': 'ica1b_ch_Cacna1b_cp6'},
                    # 'ica1c':{'sec': 'soma', 'loc': 0.5,'var': 'ica1c_ch_Cacna1c_cp3'},
                    # 'ica1g':{'sec': 'soma', 'loc': 0.5,'var': 'ica1g_ch_Cacna1g_cp41'},
                    # 'ica1i':{'sec': 'soma', 'loc': 0.5,'var': 'ica1i_ch_Cacna1i_md279'},
                    # 'ihcn1':{'sec': 'soma', 'loc': 0.5,'var': 'ihcn1_ch_Hcn1_cp9'},
                    # 'ihcn2':{'sec': 'soma', 'loc': 0.5,'var': 'ihcn2_ch_Hcn2_cp10'},
                    # 'ihcn3':{'sec': 'soma', 'loc': 0.5,'var': 'ihcn3_ch_Hcn3_cp11'},
                    # 'ihcn4':{'sec': 'soma', 'loc': 0.5,'var': 'ihcn4_ch_Hcn4_cp12'}}

cfg.stim = 'IClamp'
cfg.amp = 0.6    
cfg.cellnum = 28
cfg.km = 0.001
cfg.ka = 0.11


cfg.recordStep = 0.1       
# cfg.filename = '21sep14d/'
cfg.simLabel = '21sep14f'
cfg.saveFolder = '/tera/' + os.getlogin() + '/' +cfg.simLabel
cfg.saveJson = True
cfg.analysis['plotTraces'] = {'include': [0], 'saveFig': False}
cfg.analysis['plotRaster'] = {'saveFig': False}         

cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']
