from mpi4py import MPI
import sys, os
import numpy as np
import inspect
from netpyne import specs
from netpyne.batch import Batch
import itertools


def batch():
    params = specs.ODict()
    params["DMV_P_weight"] = [1e-6, 0.01]
    params["NA_M_weight"] = [1e-6, 0.01]
    params["seed"] = list(range(5,15))  # indexed
    b = Batch(params=params, cfgFile="cfg.py", netParamsFile="netParams_M1.py")
    # Set output folder, grid method (all param combinations), and run configuration
    b.batchLabel = "03oct23disconnect"
    b.saveFolder = "/tera/" + os.getlogin() + "/" + b.batchLabel
    b.method = "list"  # params.csv will be read by default; else need name in cfg.paramListFile
    b.runCfg = {"type": "mpi_bulletin", "script": "init.py", "skip": True}
    b.run()


if __name__ == "__main__":
    batch()
