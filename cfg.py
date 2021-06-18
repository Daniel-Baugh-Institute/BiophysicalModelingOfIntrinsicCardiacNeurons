from netpyne import specs
cfg = specs.SimConfig() 

cfg.hParams = {'celsius':35, 'v_init':-61}
cfg.duration = 5 #500 # 1*1e3
cfg.dt = 0.025          
cfg.verbose = False     
cfg.recordCells = ['all']
cfg.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}}
cfg.recordStep = 0.1       
cfg.filename = 'test2'
cfg.saveJson = True
cfg.analysis['plotTraces'] = {'include': [0], 'saveFig': True}
cfg.analysis['plotRaster'] = {'saveFig': True}                   # Plot a raster

cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']

cfg.stim = 'IClamp'
cfg.amp= 0	#1
cfg.cellnum = 0 #105
