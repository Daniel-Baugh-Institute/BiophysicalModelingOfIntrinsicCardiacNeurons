import sys
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        params['amp'] = [1]                                     #[0.6, 0.8, 1.0, 1.2, 1.4] #[-0.001, -0.002, -0.003,-0.004,-0.005]              
        params['cellnum'] = [x for x in range(115)]
        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_sur.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '21jul07b'                               #if sys.argv[-1]=='batch.py' else sys.argv[-1]
        b.saveFolder = b.batchLabel                             #'/tera/suri/'+b.batchLabel        /tera/jessica/data   #'data'
        b.method = 'grid'
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
