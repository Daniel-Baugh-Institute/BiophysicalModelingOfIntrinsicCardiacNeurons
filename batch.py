import sys, os
# sys.path.insert(0,'/u/suri/NetPyNE_repo/netpyne')
#sys.path.insert(0,'/u/billl/nrniv/netpyne') # CHANGE -- make sure which netpyne we're reading
import numpy as np
import inspect
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        params['amp'] = [0.1] # indexed 
        params['cellnum'] = [x for x in range(104)] # indexed          all_15: 104
        # params['phi']= [0.2] 
        params['na'] = [0.075, 0.095]  
        params['ka'] = [0.018, 0.07] 
        params['kc'] = [0.018, 0.025, 0.05, 0.07, 0.1, 0.18, 0.25]                               
        # params['kj'] = [0.0015, 0.0038]
        # params['h1'] = [0.00001, 0.01]           #log
        # params['h2'] = [0.009, 0.09]           
        # params['h3'] = [0.0001, 0.01]           #log
        # params['h4'] = [0.0002, 0.02]           #log
        # params['c1i'] = [0.00025, 0.0003]                #[0.0001, 0.0003, 0.0005, 0.0007, 0.0009, 0.001] 
        # params['c1g'] = [0.00001, 0.00005]        
        # params['c1d'] = [0.7e-4, 9.7e-4]
        # params['c1c'] = [0.0001, 0.01]           #log
        # params['c1b'] = [0.0001, 0.01]          # log
        # params['c1a'] = [0.00001, 0.001]         # log
        # params['g']=[5e-4,6e-4,7e-4,8e-4,9e-4]        # indexed
        # params['vc']= [v for v in np.arange(-100,101,10)]             # indexed


        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_M1.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '22aug23c'
        b.saveFolder = '/tera/' + os.getlogin() + '/' + b.batchLabel
        b.method = 'grid'  # params.csv will be read by default; else need name in cfg.paramListFile
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
