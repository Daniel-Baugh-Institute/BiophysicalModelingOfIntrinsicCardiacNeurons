from netpyne import specs
from netpyne.specs import simConfig
cfg = specs.SimConfig() 

cfg.hParams = {'celsius':35, 'v_init':-70}
cfg.duration = 100#00 # 1*1e3
cfg.dt = 0.025          
cfg.verbose = False     
cfg.recordCells = ['all']
cfg.recordTraces = {'V_soma':{'sec': 'soma','loc': 0.5,'var': 'v'},
                        'epas' : {'sec': 'soma', 'loc': 0.5,'var': 'e_pas'},
                    'ih':{'sec': 'soma', 'loc': 0.5,'var': 'iother'}, 
                    'ina': {'sec': 'soma', 'loc': 0.5,'var': 'ina'},
                    'ica': {'sec': 'soma', 'loc': 0.5,'var': 'ica'},
                    'ik': {'sec': 'soma', 'loc': 0.5,'var': 'ik'}}

cfg.recordStep = 0.1       
cfg.filename = 'output'
cfg.saveJson = True
cfg.analysis['plotTraces'] = {'include': [0], 'saveFig': True}
cfg.analysis['plotRaster'] = {'saveFig': False}         

cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']

cfg.stim = 'IClamp'
cfg.amp= 0.2      
cfg.cellnum = 6              

