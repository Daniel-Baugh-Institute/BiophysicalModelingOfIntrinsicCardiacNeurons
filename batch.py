import sys
import numpy as np
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        params['amp'] = [0.6]   #[0.6, 0.9]                                    
        params['cellnum'] = [1]    #[x for x in range(115)]
        params['gsk'] =  [0.01]       #[0, 0.001, 0.003, 0.005, 0.008, 0.01, 0.03, 0.05, 0.08]
        params['tau'] =  [3, 5, 9]       #[x for x in np.arange(1,6,0.5)]
        params['gkcna'] = [0.015]      #[0.015, 0.03, 0.05, 0.08, 0.1]
        params['gkcnc'] = [0.015]             #[0.015, 0.03, 0.05, 0.08, 0.1]
        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_A.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '21aug02b'                               #if sys.argv[-1]=='batch.py' else sys.argv[-1]
        b.saveFolder = b.batchLabel                             #'/tera/suri/'+b.batchLabel        /tera/jessica/data   #'data'
        b.method = 'grid'
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
