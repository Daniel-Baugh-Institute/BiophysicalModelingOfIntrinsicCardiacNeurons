import sys, os
# sys.path.insert(0,'/u/suri/NetPyNE_repo/netpyne')
#sys.path.insert(0,'/u/billl/nrniv/netpyne') # CHANGE -- make sure which netpyne we're reading
import numpy as np
import inspect
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        params['amp'] = [0.1, 0.2, 0.3, 0.4, 0.5] # indexed 
        params['cellnum'] = [x for x in range(104)] # indexed          all_15: 104
        params['phi']= [0,0.2,0.6,1] # indexed  
        params['na'] = [0.068, 0.102]  
        params['ka'] = [0.02, 0.03] 
        params['kc'] = [0.02, 0.03]                               
        params['kj'] = [0.00344, 0.00516]
        params['h1'] = [0.0056, 0.0084]           
        params['h2'] = [0.048, 0.072]           
        params['h3'] = [0.0064, 0.0096]           
        params['h4'] = [0.00064, 0.00096]           
        params['c1i'] = [0.0016, 0.0024]                
        params['c1g'] = [0.00008, 0.00012]        
        params['c1d'] = [0.00008, 0.00012]
        params['c1c'] = [0.0016, 0.0024]           
        params['c1b'] = [0.0008, 0.0012]          
        params['c1a'] = [0.000056, 0.000084]         
        # params['g']=[5e-4,6e-4,7e-4,8e-4,9e-4]        # indexed
        # params['vc']= [v for v in np.arange(-100,101,10)]             # indexed


        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_M1.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '22aug24Qe'
        b.saveFolder = '/tera/' + os.getlogin() + '/' + b.batchLabel
        b.method = 'list'  # params.csv will be read by default; else need name in cfg.paramListFile
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
