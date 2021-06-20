from netpyne import specs
from netpyne.specs import simConfig
cfg = specs.SimConfig() 

cfg.hParams = {'celsius':35, 'v_init':-61}
cfg.duration = 5 #500 # 1*1e3
cfg.dt = 0.025          
cfg.verbose = False     
cfg.recordCells = ['all']
cfg.recordTraces = {'V_soma':{'sec': 'soma','loc': 0.5,'var': 'v'},
                        'epas' : {'sec': 'soma', 'loc': 0.5,'var': 'e_pas'}}
#cfg.recordTraces = {'V_soma':{'sec': 'soma','loc': 0.5,'var': 'v'},
#                          'ik_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'ik'},
#                          'cai_soma': {'sec': 'soma', 'loc':0.5, 'var': 'cai'},
#                          'cao_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'cao'},
#                          'ina_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'ina'},
#                          'iother_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'iother'},
#                          'epas' : {'sec': 'soma', 'loc': 0.5,'var': 'e_pas'}}
cfg.recordStep = 0.1       
cfg.filename = 'test_epas'
cfg.saveJson = True
cfg.analysis['plotTraces'] = {'include': [0], 'saveFig': True}
cfg.analysis['plotRaster'] = {'saveFig': True}         

cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']

cfg.stim = 'IClamp'
cfg.amp= 0
cfg.cellnum = 0 
