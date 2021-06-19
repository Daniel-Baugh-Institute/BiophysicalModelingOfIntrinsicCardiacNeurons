''' run analysis.py to generate batchLabel_allData.json
    load batchLabel_allData.json
    extract params and data
    LOADS A SINGLE AMP_CELLNUM COMBINATION FOR NOW
    TO ADD: runs thru all combination - e_pas list for all combinations
    
'''
import json
from netpyne import sim, specs

# to use later:
#batchLabel = '21june18a'; dataFolder = '/Users/jessicafeldman/Desktop/ragp/ragp/data/'
#data = json.load(open(['%\s' + '%\s' + '_allData.json'] (dataFolder, batchLabel))
data = json.load(open('test_epas.json'))
e_pas = data['simData']['epas']['cell_0'][1]
cai = data['simData']['cai_soma']['cell_0'][0]
cao = data['simData']['cao_soma']['cell_0'][0]
ik_soma = data['simData']['ik_soma']['cell_0'][0]

