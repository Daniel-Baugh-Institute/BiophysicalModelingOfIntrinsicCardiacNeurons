import sys, os
import numpy as np
import inspect
from netpyne import specs
from netpyne.batch import Batch
import itertools


def batch():
    params = specs.ODict()
    params["phasic_phasic_weight"] = [i / 50000 for i in range(21)]  # indexed
    params["mixed_mixed_weight"] = [i / 50000 for i in range(21)]  # indexed
    params["phasic_mixed_weight"] = [i/500 for i in range(4)]  # indexed
    params["seed"] = list(range(10))  # indexed
    b = Batch(params=params, cfgFile="cfg.py", netParamsFile="netParams_M1.py")
    # Set output folder, grid method (all param combinations), and run configuration
    b.batchLabel = "14jan23weak"
    b.saveFolder = "/tera/" + os.getlogin() + "/" + b.batchLabel
    b.method = "list"  # params.csv will be read by default; else need name in cfg.paramListFile
    b.runCfg = {"type": "mpi_bulletin", "script": "init.py", "skip": True}
    b.run()


if __name__ == "__main__":
    batch()
