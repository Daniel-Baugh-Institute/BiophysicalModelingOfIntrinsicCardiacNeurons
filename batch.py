import sys, os
# sys.path.insert(0,'/u/suri/NetPyNE_repo/netpyne')
#sys.path.insert(0,'/u/billl/nrniv/netpyne') # CHANGE -- make sure which netpyne we're reading
import numpy as np
import inspect
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        # params['amp'] = [0.1, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2] # indexed
        # params['cellnum'] = [x for x in range(70)] # indexed          NSP 15: 70 cells
        # params['cellnum'] = [x for x in range(84)] # indexed          NSP NA: 84 cells
        params['cellnum'] = [x for x in range(67)] # indexed          SP 15: 67 cells
        # params['cellnum'] = [x for x in range(86)] # indexed          SP NA: 86 cells
        # params['sze'] = [16,18,20,23,25,27,30] 
        # params['na'] = [0.1, 1]                 # log
        # params['h1'] =[0.0001, 0.00001]         # log


        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_M1.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '22mar21c'
        b.saveFolder = b.batchLabel #'/tera/' + os.getlogin() + '/' + b.batchLabel
        b.method = 'grid'  # params.csv will be read by default; else need name in cfg.paramListFile
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
