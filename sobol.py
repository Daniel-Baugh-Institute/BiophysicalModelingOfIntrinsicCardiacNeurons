#!/usr/bin/env python

import math, re, csv, os
from scipy.stats import qmc
from itertools import product
import numpy as np

def parseBatchParams (b):
    ''' read a batch.py file for NetPyNE param search; returning list of (name, valueList, [indexed]) where optional indexed means to use all the values '''
    try: 
        with open(b,'r') as fb: lines = fb.readlines()
        print(f'Reading {os.getcwd()+"/"+b}')
    except Exception as e:
        print(f"ERROR >>>{e}<<<")
    p = re.compile(r'''\s+params[^a-z]+([^]']+)'\]\s*=\s*(\[[^]]+\])\s*#*\s*(indexed|log|linear)*''') # keywords as comments in batch.py: indexed|log|linear
    bl = [(i, p.match(l)) for i,l in enumerate(lines)] # bl: lines that match regexp
    pl = {}
    for i,m in bl:
        if m:
            try:
                pl[m.group(1)] = {'vals': eval(m.group(2)), 'type':m.group(3) or 'linear'} # strings: name, valueList, [indexed]
            except Exception as e:
                print(f"ERROR >>>{e}<<<\n\tunable to evaluate '{m.group(2)}':\n\tline {i}: {m.string.strip()}")
    return pl

def sobcall (pl, num, seed=33):
    ''' determine the min, max of sobolized params and do the combos with indexed params '''
    labels, Mins, Maxs, ilabels, ivals, llabels, lMins, lMaxs = [],[],[],[],[],[],[],[]
    for k,v in pl.items():
        if v['type'] == 'linear':
            v['min'], v['max'] = min(v['vals']), max(v['vals'])
        elif v['type'] == 'log':
            v['min'], v['max'] = np.log10(min(v['vals'])), np.log10(max(v['vals']))
        elif v['type'] != 'indexed':
            raise Exception(f"{v['type']} unrecognized key word")
    return pl
    if verbose: print(f'Mins/Maxs for {labels}: Mins:{Mins}, Maxs:{Maxs}')
    sobolVals = sob(len(Mins)+len(lMins), num, seed=seed) # linear,log
    scaledVals = qmc.scale(sobolVals, Mins, Maxs)
    scaledLogVals = qmc.scale(sobolLogVals, lMins, lMaxs) # only log
    scaledAlogVals = 10**scaledLogVals
    combos = [[*p[0],*p[1], *p[2]] for p in product(scaledVals.tolist(),scaledAlogVals.tolist(),list(product(*ivals)))]
    combos.insert(0, labels+llabels+ilabels)
    return combos

def sob (dim=4, num=4096, seed=1234):
    sm = qmc.Sobol(d=dim, scramble=True, seed=seed)
    m = math.floor(math.log(num)/math.log(2) + 0.99) # round up to nearest power of 2
    if 2**m != num: print(f'\t{2**m} samples (2^{m} ; {num} requested)')
    vals = sm.random_base2(m=m) # 2^m points
    return vals

def output (out):
    try: 
        with open(ag.f, 'w') as f:
            wr = csv.writer(f)
            wr.writerows(out)
        print(f'Output of {len(out)-1} param combinations to {os.getcwd()+"/"+ag.f}')
    except Exception as e:
        print(f"ERROR >>>{e}<<<")

def getArgs ():
    global verbose
    import argparse
    msg = '''Generate at least cnt lines of sobol samples based on params definitions in batch.py.
             Params may be indicated as '# indexed' in which case the batch values given will be used.
             Other params will be scaled using a sobol quasi-monte carlo distribution'''
    parser = argparse.ArgumentParser(description=msg, )
    # parser.add_argument('-d', '--dims', nargs='?', type=int, default=4, help='dim of space to be sampled')
    parser.add_argument('-c', '--cnt', nargs='?', type=int, default=10, help='num of samples: will be rounded up to a power of 2') # input as `--` name
    # parser.add_argument("-r", default='sobol.csv', help='raw output from sobol call (default ./sobol.csv)')
    parser.add_argument("-f", default='params.csv', help='file for saving param lists (default ./params.csv)')
    parser.add_argument("-s", default=1234, type=int, help='seed')
    parser.add_argument("-v", action='store_true', default=False, help='verbose output to terminal')
    parser.add_argument("-b", default='batch.py', help='name of batchfile with "params" ranges (default ./batch.py)')
    ag = parser.parse_args()
    verbose = True if ag.v else True
    return ag

if __name__ == '__main__':
    ag = getArgs()
    if verbose: print('Verbose output')
    output(sobcall(parseBatchParams(ag.b), ag.cnt))
