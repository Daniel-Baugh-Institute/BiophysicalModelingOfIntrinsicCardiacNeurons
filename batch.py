import sys
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        params['amp'] =  [0.2]
        params['cellnum'] = [x for x in range(115)]
        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '21jul03special3' #if sys.argv[-1]=='batch.py' else sys.argv[-1]
        b.saveFolder = '/tera/jessica/data' #'data'        /tera/jessica/data        #'data'
        b.method = 'grid'
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
