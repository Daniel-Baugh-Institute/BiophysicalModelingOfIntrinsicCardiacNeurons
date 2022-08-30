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
        params['phi']= [0.2] # indexed  
        # params['na'] = [0.06, 0.065, 0.07, 0.075, 0.08, 0.085, 0.09, 0.095, 0.1] 
        # params['ka'] = [0.01, 0.02, 0.03,0.04, 0.05, 0.06, 0.07]
        # params['kc'] = [0.00018, 0.00048, 0.00078, 0.0018, 0.0048, 0.0078, 0.018, 0.048, 0.078, 0.18]                              
        # params['kj'] = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007]
        # params['h1'] = [0.0024, 0.0036]           
        # params['h2'] = [0.009, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08,0.09]
        # params['h3'] = [0.008, 0.012]           
        # params['h4'] = [0.0028, 0.0042]           
        # params['c1i'] = [0.00048, 0.00072]                
        # params['c1g'] = [0.00024, 0.00036]        
        # params['c1d'] = [0.00036, 0.00054]
        # params['c1c'] = [0.0048, 0.0072]           
        # params['c1b'] = [0.00008, 0.00012]          
        params['c1a'] = [0.00001, 0.00002, 0.00003, 0.00004, 0.00005, 0.00006, 0.00007, 0.00008, 0.00009, 0.0001]
        # params['g']=[5e-4,6e-4,7e-4,8e-4,9e-4]        # indexed
        # params['vc']= [v for v in np.arange(-100,101,10)]             # indexed


        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_P.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '22aug29f'
        b.saveFolder = '/tera/' + os.getlogin() + '/' + b.batchLabel
        b.method = 'grid'  # params.csv will be read by default; else need name in cfg.paramListFile
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
