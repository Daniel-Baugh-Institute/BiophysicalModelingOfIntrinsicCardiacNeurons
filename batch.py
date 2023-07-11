import sys, os
import numpy as np
import inspect
from netpyne import specs
from netpyne.batch import Batch
import itertools


def batch():
    params = specs.ODict()
    params["P_P_weight_scale"] = [i*0.5 for i in range(11)]  # indexed
    params["M_M_weight_scale"] = [i*0.5 for i in range(11)]  # indexed
    params["P_M_weight_scale"] = [i*0.5 for i in range(11)]  # indexed
    #params["seed"] = list(range(5))  # indexed
    b = Batch(params=params, cfgFile="cfg.py", netParamsFile="netParams_M1.py")
    # Set output folder, grid method (all param combinations), and run configuration
    b.batchLabel = "10jul23NTE"
    b.saveFolder = "/tera/" + os.getlogin() + "/" + b.batchLabel
    b.method = "list"  # params.csv will be read by default; else need name in cfg.paramListFile
    b.runCfg = {"type": "mpi_bulletin", "script": "init.py", "skip": True}
    b.run()


if __name__ == "__main__":
    batch()
