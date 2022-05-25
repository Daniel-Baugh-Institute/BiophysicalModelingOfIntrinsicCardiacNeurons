import sys, os
# sys.path.insert(0,'/u/suri/NetPyNE_repo/netpyne')
#sys.path.insert(0,'/u/billl/nrniv/netpyne') # CHANGE -- make sure which netpyne we're reading
import numpy as np
import inspect
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        params['amp'] = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1] #indexed
        params['cellnum'] = [x for x in range(104)] # indexed          all_15: 104
        # params['phi']= [0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1] # indexed
        # params['na'] = [0.8, 1]
        # params['ka'] = [0.011, 0.014, 0.018, 0.025, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.06]
        # params['kc'] = [0.011, 0.1]
        # params['kj'] = [0.001,0.009]
        # params['h1'] = [0.1,0.00001]           #log
        # params['h2'] = [0.9,0.009]           #log
        # params['h3'] = [0.1,0.0001]           #log
        # params['h4'] = [0.02,0.0002]           #log
        # params['c1i'] = [0.006,0.0008]
        # params['c1g'] = [0.001,0.00001]
        # params['c1d'] = [8.7e-4,1.7e-4]
        # params['c1c'] = [0.01,0.0001]           #log
        # params['c1b'] = [0.001,0.0001]          # log
        # params['c1a'] = [0.001,0.00001]         # log
        # params['g']=[5e-4,6e-4,7e-4,8e-4,9e-4]


        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_M1.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '22may25b'
        b.saveFolder = '/tera/' + os.getlogin() + '/' + b.batchLabel
        b.method = 'grid'  # params.csv will be read by default; else need name in cfg.paramListFile
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
