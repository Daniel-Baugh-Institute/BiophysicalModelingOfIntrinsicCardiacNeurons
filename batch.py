import sys, os
sys.path.insert(0,'/u/suri/NetPyNE_repo/netpyne')
#sys.path.insert(0,'/u/billl/nrniv/netpyne') # CHANGE -- make sure which netpyne we're reading
import numpy as np
import inspect
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        params['amp'] = [0.6, 0.7, 0.8, 0.9] # indexed
        params['cellnum'] = [x for x in range(101)] # indexed
        #params['rybak'] = [0, 0.01, 0.03, 0.05, 0.07, 0.1, 0.12, 0.15] 
        params['ka'] = [0.08, 0.15]
        params['na'] = [0.1, 1]                 #log10
        params['kcnc'] =[0.011, 0.015]
        params['kcnab'] =[0.011, 0.015]
        params['h1'] =[0.0001, 0.00001]         #log10
        params['h2'] =[0.09, 0.009]             #log10
        params['h3'] =[0.001, 0.0001]           #log10
        params['h4'] =[0.002, 0.0002]           #log10
        params['c1a'] =[0.0001, 0.00001]        #log10
        params['c1b'] =[0.001, 0.0001]          #log10
        params['c1c'] =[0.001, 0.0001]          #log10
        params['c1g'] =[0.0001, 0.00001]        #log10
        params['c1i'] =[0.0027, 0.00027]        #log10

        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_A.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '21dec06a'
        b.saveFolder = '/tera/' + os.getlogin() + '/' + b.batchLabel
        b.method = 'list'  # params.csv will be read by default; else need name in cfg.paramListFile
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
