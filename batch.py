# -*- coding: utf-8 -*-
"""
Created in April 2021

@author: sgupta
"""

import sys, os
os.system('nrnivmodl mod')
import numpy as np
import inspect
from netpyne import specs
from netpyne.batch import Batch
import csv



def batch():
    # Things to change
    batchlabel = '12jun24'
    num_cells = 104
    
    
    params = specs.ODict()
    params['amp'] = [0.1,0.3,0.5]                       # indexed
    # params['vc']= [v for v in np.arange(-100,101,10)]             # indexed
    params['cellnum'] = [x for x in range(104)]                     # indexed          
    # params['phi']= [0.2]                                          # indexed  

    # To be used with sobol.py

    # ± 20% change in channel conductance
    params['na'] = [0.017, 0.6] #0.1 
    params['ka'] = [0.0017, 0.06] # 0.01 
    params['kc'] = [0.0017, 0.06] # 0.01
    params['phi'] = [0.1,1]                              
    params['kj'] = [0.0017, 0.06] # 0.01
    params['h1'] = [0.0017, 0.06] # 0.01          
    params['h2'] = [0.0017, 0.06] # 0.01         
    params['h3'] = [0.0017, 0.06] # 0.01          
    params['h4'] = [0.0017, 0.06] # 0.01          
    params['c1i'] = [0.00017, 0.006] # 0.001               
    params['c1g'] = [0.00017, 0.006] # 0.001       
    params['c1d'] = [0.00017, 0.006] # 0.001
    params['c1c'] = [0.00017, 0.006] # 0.001          
    params['c1b'] = [0.00017, 0.006] # 0.001         
    params['c1a'] = [0.00017, 0.006] # 0.001


    b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_M1.py')
    # Set output folder, grid method (all param combinations), and run configuration
    b.batchLabel = batchlabel
    b.saveFolder = b.batchLabel
    # b.method = 'grid'
    b.method = 'list'  # Used with sobol.py; params.csv will be read by default; else need name in cfg.paramListFile
    b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
    b.run()

batch()

