# ragp
Model Documentation: Biophysical Modelling of Neuronal Phenotypes of the Right Atrial Ganglionic Plexus from Single Neuron Transcriptomics

Context of use: Simulation of single compartment neuron electrical activity in the RAGP.

Instructions for reproducing figures using data generated by models:

A.	Figure 2 and 3
  1.	Clone GitHub repository and checkout to tag-v2.0.2
git clone https://github.com/Daniel-Baugh-Institute/BiophysicalModelingOfIntrinsicCardiacNeurons.git
  2.   Figure 2: Execute ct_genes.py, which reads data from threshold.py
  3.   Figure 3A: Run Tdata_plots.py, which reads the data from tdata_all_15.csv. Also run Tdata_plots_thresholds.py for plots showing the alternative Ct thresholds tested.
  4.   Figure 3B and 3C: Run Tdata_plots_thresholds.py. Plots for Ct thresholds of 14 and 16 can also be generated using this script by switching out the csv file names.

B.  Figure 4 
  1. In code/IC_comp run CaTplot.py and Naplot.py

C.	Figures 5 and 6
  1.   Figure 5A:
    i.   Read data file 22aug25b_allData.json
    ii.  Execute the 'classification' function in scAnalysis.py
    iii. Download classification.json and classification_firing_sequence.py
    iv.  Run classification_firing_sequence.py
  2.  Figure 5B and 5C: To produce the distribution of firing types at different thresholds, use analysis_ct.py. The dataFolder, batchLabel, paramFile, and filename must be updated. For example for a Ct threshold of 13, use dataFolder = "24jan24_13", batchLabel = '24jan24_13', paramFile = 'params_13.csv', filename = 'your_working_directory_path//24jan24_13_allData.json'
  3.  Figure 6: Use analysis_ct.py but switch out the file paths to be filename = '25jan24_scn1a_-20_allData.json' and filename = '25jan24_scn1a_allData+20.json' for a negative 20% change and positive 20% change in h_inf. Note that these files are available on the SPARC portal (https://doi.org/10.26275/cy9w-ttjn). Use paramFile = 'params.csv', dataFolder = '25jan24_scn1a_-20' and batchLabel='25jan24_scn1a_-20'. You will need to comment out any part of scAnalysis.py and classification_firing_sequence.py that is not a function (at the end of the script).

 Note that a large amount of RAM is required to run this file 
 
D.	Figure 7
  1.	Read data file 22aug25b_allData.json 
  2.	Execute the 'IV' function in scAnalysis.py  
  Note that a large amount of RAM is required to run this file 

E.	Figure 8
  1. Raw transcriptomic data and calculations for fold change difference in expression between ion channel genes can be found in primary/RAGP_4subs_raw_Ct_analyzed_Differential_expression.xlsx. The figure is also provided in the spreadsheet.

Instructions for running the models: 
Detailed instructions for running the model in NetPyNE and on the O2S2PARC platform are as follows:

I. NetPyNE implementation
1.	Open a new Terminal window
2.	Make a new directory into which to clone the repository
3.	Clone GitHub repository and checkout to tag-v2.0.2
git clone https://github.com/suny-downstate-medical-center/ragp.git
4.	Install NEURON and NetPyNE: 
pip3 install NEURON / pip install NEURON
pip3 install netpyne / pip3 install netpyne
5.	Compile mod files: 
nrnivmodl mod
6.	On successful compilation, x86_64 folder is created
7.	In order to run a single simulation, execute the following command:
nrniv -python init.py
8.	In order to run a batch simulation, MPI installation is mandatory: 
mpiexec --oversubscribe -np 32 nrniv -python -mpi batch.py

    a.	Once the simulations are complete, run scAnalysis.py
ipython -i scAnalysis.py
  
    b.	Create _allData.json file by running the function 
readBatchData(dataFolder, batchLabel, paramFile = 'params.csv')
  
    c.	Load the _allData.json file by running the function 
readAllData(jsonfilename)
  
    d.	Analyse the data in _allData.json using the functions in scAnalysis.py
10.	In order to run sobol sampling on the parameter space, execute sobol.py, following which a csv file (default name: params.csv) is generated that will contain the parameter values
11.	In order to plot the binarized transcriptomics data, execute 
ipython Tdata_plots.py
12. In order to create the bar plot that compares Ct values, execute
ipython ct_genes.py

II. O2S2PARC implementation:  
1.	Login to https://osparc.io/
2.	Use the Jupyter Octave+Python Math service from the Dashboard
3.	Clone the repository from GitHub checkout to tag-v2.0.2: 
https://github.com/suny-downstate-medical-center/ragp.git
4.	Launch Terminal
5.	Type the following commands on the Terminal

    a.	cd work/ragp
  
    b.	pip install --quiet NEURON
  
    c.	pip install --quiet netpyne
7.	Resume the steps from I.5. 


Additional analysis:

Effect of varying phi_kcnc1 parameter on  firing frequency (see generated plot in docs folder)
1. Use scAnalysis.py to run readAllData('22aug25c_allData.json') then fphi(df)





