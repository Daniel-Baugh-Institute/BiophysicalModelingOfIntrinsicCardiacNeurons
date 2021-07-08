import sys
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        params['amp'] = [0.3, 0.5, 0.8, 1, 1.2]                                    
        params['cellnum'] = [x for x in range(115)]
        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_D.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '21jul08c'                               #if sys.argv[-1]=='batch.py' else sys.argv[-1]
        b.saveFolder = b.batchLabel                             #'/tera/suri/'+b.batchLabel        /tera/jessica/data   #'data'
        b.method = 'grid'
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
