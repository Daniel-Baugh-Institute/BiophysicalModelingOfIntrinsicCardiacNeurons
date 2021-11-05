import sys, os
sys.path.insert(0,'/u/suri/NetPyNE_repo/netpyne')
#sys.path.insert(0,'/u/billl/nrniv/netpyne') # CHANGE -- make sure which netpyne we're reading
import numpy as np
import inspect
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        params['amp'] = [0.3] #, 0.6, 0.9] # indexed
        params['cellnum'] = [0,1] #[x for x in range(101)] # indexed
        #params['rybak'] = [0, 0.01, 0.03, 0.05, 0.07, 0.1, 0.12, 0.15] 
        params['ka'] = [0] #[0.08, 0.1, 0.12, 0.15] 

        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_A.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '21nov5n' 
        b.saveFolder = '/tera/' + os.getlogin() + '/' + b.batchLabel
        b.method = 'grid'  # params.csv will be read by default; else need name in cfg.paramListFile
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
