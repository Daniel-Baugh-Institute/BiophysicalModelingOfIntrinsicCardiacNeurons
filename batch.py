import sys, os
import numpy as np
import inspect
from netpyne import specs
from netpyne.batch import Batch


def batch():
    params = specs.ODict()
    params['phasic_phasic_weight'] = [i*1e-2 for i in range(0,11,2)] # indexed
    params['phasic_tonic_weight'] = [i*1e-2 for i in range(0,11,2)]  # indexed 
    params['tonic_tonic_weight'] = [i*1e-2 for i in range(0,11,2)]   # indexed
    params['cluster_size'] = [5, 10, 50, 100, 500] # indexed
    b = Batch(params=params, cfgFile="cfg.py", netParamsFile="netParams_M1.py")
    # Set output folder, grid method (all param combinations), and run configuration
    b.batchLabel = "29aug22net"
    b.saveFolder = "/tera/" + os.getlogin() + "/" + b.batchLabel
    b.method = "list"  # params.csv will be read by default; else need name in cfg.paramListFile
    b.runCfg = {"type": "mpi_bulletin", "script": "init.py", "skip": True}
    b.run()


batch()
