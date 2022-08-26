import sys, os
# sys.path.insert(0,'/u/suri/NetPyNE_repo/netpyne')
#sys.path.insert(0,'/u/billl/nrniv/netpyne') # CHANGE -- make sure which netpyne we're reading
import numpy as np
import inspect
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        params['amp'] = [0.08, 0.1, 0.2, 0.3] # indexed 
        params['cellnum'] = [x for x in range(104)] # indexed          all_15: 104
        params['phi']= [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1] #[0,0.2,0.6,1] # indexed  
        # params['na'] = [0.076, 0.114]  
        # params['ka'] = [0.0144, 0.0216] 
        # params['kc'] = [0.08, 0.12]                               
        # params['kj'] = [0.00464, 0.00696]
        # params['h1'] = [0.008, 0.012]           
        # params['h2'] = [0.16, 0.24]           
        # params['h3'] = [0.004, 0.006]           
        # params['h4'] = [0.0016, 0.0024]           
        # params['c1i'] = [0.00072, 0.00108]                
        # params['c1g'] = [0.000064, 0.000096]        
        # params['c1d'] = [0.000056, 0.000084]
        # params['c1c'] = [0.008, 0.012]           
        # params['c1b'] = [0.0004, 0.0006]                  
        # params['c1a'] = [0.00008, 0.00012]        
        # params['g']=[5e-4,6e-4,7e-4,8e-4,9e-4]        # indexed
        # params['vc']= [v for v in np.arange(-100,101,10)]             # indexed


        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_P.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '22aug25c'
        b.saveFolder = '/tera/' + os.getlogin() + '/' + b.batchLabel
        b.method = 'grid'  # params.csv will be read by default; else need name in cfg.paramListFile
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
