# -*- coding: utf-8 -*-
"""
Created in April 2021

@author: sgupta
"""

import sys, os
import numpy as np
import inspect
from netpyne import specs
from netpyne.batch import Batch

def batch():
        params = specs.ODict()
        params['amp'] = [0.1, 0.2, 0.3, 0.4, 0.5]                       # indexed 
        # params['vc']= [v for v in np.arange(-100,101,10)]             # indexed
        params['cellnum'] = [x for x in range(104)]                     # indexed          
        params['phi']= [0.2] # indexed  

        # To be used with sobol.py

        # ± 20% change in channel conductance

        # params['na'] = [0.06, 0.09]  
        # params['ka'] = [0.0144, 0.0216] 
        # params['kc'] = [0.0144, 0.0216]                               
        # params['kj'] = [0.0028, 0.0042]
        # params['h1'] = [0.0024, 0.0036]           
        # params['h2'] = [0.0072, 0.0108]           
        # params['h3'] = [0.008, 0.012]           
        # params['h4'] = [0.0028, 0.0042]           
        # params['c1i'] = [0.00048, 0.00072]                
        # params['c1g'] = [0.00024, 0.00036]        
        # params['c1d'] = [0.00036, 0.00054]
        # params['c1c'] = [0.0048, 0.0072]           
        # params['c1b'] = [0.00008, 0.00012]          
        # params['c1a'] = [0.00004, 0.00006] 


        b = Batch(params=params, cfgFile='cfg.py', netParamsFile='netParams_M1.py')
        # Set output folder, grid method (all param combinations), and run configuration
        b.batchLabel = '23jun13a'
        b.saveFolder = b.batchLabel
        b.method = 'grid'
        # b.method = 'list'  # Used with sobol.py; params.csv will be read by default; else need name in cfg.paramListFile
        b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}
        b.run()

batch()
