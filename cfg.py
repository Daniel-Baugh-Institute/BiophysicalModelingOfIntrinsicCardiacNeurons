from netpyne import specs
from netpyne.specs import simConfig
cfg = specs.SimConfig() 
#cfg = simConfig()

cfg.hParams = {'celsius':35, 'v_init':-61}
cfg.duration = 5 #500 # 1*1e3
cfg.dt = 0.025          
cfg.verbose = False     
cfg.recordCells = ['all']
cfg.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}} #var':'epas'}}
# Recording/plotting parameters
#simConfig.recordTraces = {'V_soma':{'sec': 'soma','loc': 0.5,'var': 'v'},
#                          'ik_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'ik'},
#                          'cai_soma': {'sec': 'soma', 'loc':0.5, 'var': 'cai'},
#                          'cao_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'cao'}}
cfg.recordTraces = {'V_soma':{'sec': 'soma','loc': 0.5,'var': 'v'},
                    'V_soma':{'sec': 'soma', 'loc': 0.5,'var': 'epas'},
                          'ik_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'ik'},
                          'cai_soma': {'sec': 'soma', 'loc':0.5, 'var': 'cai'},
                          'cao_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'cao'}}


cfg.recordStep = 0.1       
cfg.filename = 'test2'
cfg.saveJson = True
cfg.analysis['plotTraces'] = {'include': [0], 'saveFig': True}
cfg.analysis['plotRaster'] = {'saveFig': True}                   # Plot a raster

cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net', 'epas']

cfg.stim = 'IClamp'
cfg.amp= 0	#1
cfg.cellnum = 0 #105
