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
        params['cellnum'] = [0] #[x for x in range(104)] # indexed          all_15: 104
        # params['phi']= [0.2] 
        params['na'] = [0.075]  
        params['ka'] = [0.018] 
        params['kc'] = [0.018]                               
        params['kj'] = [0.0035]
        params['h1'] = [0.003]           
        params['h2'] = [0.09, 0.2,0.5,0.7,0.9]           
        params['h3'] = [0.01]           
        params['h4'] = [0.0035]           
        params['c1i'] = [0.0006]                
        params['c1g'] = [0.0003]        
        params['c1d'] = [0.00045]
        params['c1c'] = [0.006]           
        params['c1b'] = [0.0001]          
        params['c1a'] = [0.00033]         
        # params['g']=[5e-4,6e-4,7e-4,8e-4,9e-4]        # indexed
        # params['vc']= [v for v in np.arange(-100,101,10)]             # indexed


        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_M1.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '22aug23p'
        b.saveFolder = b.batchLabel #'/tera/' + os.getlogin() + '/' + b.batchLabel
        b.method = 'grid'  # params.csv will be read by default; else need name in cfg.paramListFile
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
