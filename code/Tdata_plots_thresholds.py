# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 17:17:01 2023

@author: sgupta & mmgee 
"""

import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import plotly.graph_objects as go
import math as m
import plotly.io as pio
import seaborn as sns

font = 16
plt.rcParams.update({'font.size': font})

name = 'tdata_all_15'
wr = 20 # width of reduced heatmap
wf = 20 # width of full heatmap

df = pd.read_csv(f"{name}.csv")

def plotHeatmap(dfr, gene, phy, l, w, x1, xe, y, t1, t2, cs, title):
    """
    Generate a heatmap plot based on provided data.

    Parameters:
    -----------
    dfr : DataFrame
        The input DataFrame containing the data to be visualized as a heatmap.

    gene : list
        List of labels for the genomic identity axis.

    phy : list
        List of labels for the physiological identity axis.

    l : int
        Length of some specific parameter.

    w : int
        Width of the generated figure for the heatmap.

    x1 : int
        x-coordinate for the placement of text 't1'.

    xe : int
        x-coordinate for the placement of text 't2'.

    y : int
        y-coordinate for the placement of texts 't1' and 't2'.

    t1 : str
        Text to be displayed at position (x1, y).

    t2 : str
        Text to be displayed at position (xe, y).

    cs : str or colormap
        Colormap to be used for the heatmap colors.

    title : str
        Title of the heatmap plot.

    Returns:
    --------
    None
    """

    f = plt.figure(figsize=(w, 7))
    ax = sns.heatmap(dfr.transpose(), linewidth=0.4, xticklabels=False, yticklabels=gene, cmap=cs, cbar=False)
    ax.set_ylabel('Genomic Identity', fontsize=font)
    ax2 = ax.twinx()
    ax2.yaxis.set_ticks_position('right')
    ax2 = sns.heatmap(dfr.transpose(), linewidth=0.5, xticklabels=False, yticklabels=phy, cmap=cs, cbar=False)
    ax2.set_ylabel('Physiological Identity', fontsize=font)
    ax2.set_yticklabels(ax2.get_ymajorticklabels(), fontsize=font)
    plt.text(x1, y, t1, fontdict={'size': font})
    plt.text(xe, y, t2, fontdict={'size': font})
    ax2.set_title(title, fontsize=font)
    sns.set(font_scale=1.8)
    # plt.savefig(f"{name}_{l}_heatmap.png",dpi=300,bbox_inches='tight')
    # plt.show()
    return


# org yaxis: most # to least # of genes
df['sum'] = df.sum(axis=1,numeric_only=True)
dfasc = df.sort_values(by=['sum'],ascending=[True])
dfasc = dfasc.reset_index()
del dfasc['index']
del df['sum']
gfull = dfasc['Gene']

# org xaxis: cells with most to least common genes
dfm2l = dfasc.drop(['Gene','sum'],axis=1).transpose()
dfm2l['bitsum'] = [sum([2**(indx)*row for indx,row in enumerate(cell)]) for cell in dfm2l.values]
dfm2l = dfm2l.sort_values(by=['bitsum'],ascending=[False])
del dfm2l['bitsum']
tx1 = -38
txe = 318
ty = 15.8
txt1 = 'Single Neurone: #1'
txt2 = '#321'
cs = 'copper_r'
phys = ["HCN3","Cav 3.1 (T)","Cav 2.1 (P/Q)","Cav 1.3 (L)","HCN1","HCN4","Cav 1.2 (L)","Cav 2.2 (N)","Kv 1.1 ($\u03B1$ unit)","Kir 3.1","HCN2","Cav 3.3 (T)","Kv 3.1","Kv 1.1 ($\u03B21$ unit)","Nav 1.1"]
plotHeatmap(dfm2l,gfull,phys,'full',wf,tx1, txe, ty,txt1,txt2,cs,title='') # beige and balck plot

# max # of genes is different in 321 cells vs in 104 cells

# dropping Kcnab1 from red. binary map
dfwob = df.drop(df['Gene'].tolist().index("Kcnab1"))
gwob = dfwob['Gene']
dfred = dfwob.drop('Gene',axis=1).transpose().drop_duplicates(keep='first').transpose()

# sort yaxis: maximally expressed genes at the bottom
dfred.insert(0,"Gene",gwob)
dfred['sum'] = dfred.sum(axis=1,numeric_only=True)
dfred = dfred.sort_values(by=['sum'],ascending=[True])
gred = dfred['Gene']
gr = gred.tolist()
gr[gr.index('Kcna1')]=gr[gr.index('Kcna1')]+'+ab1'

# sort xaxis: most to least common genes
dfrm2l = dfred.drop(['Gene','sum'],axis=1).transpose()
dfrm2l['bitsum'] = [sum([2**(indx)*row for indx,row in enumerate(cell)]) for cell in dfrm2l.values]
dfrm2l = dfrm2l.sort_values(by=['bitsum'],ascending=[False])
del dfrm2l['bitsum']

tx1 = -12# -15
txe = 103
ty = 14.8
txt1 = 'Neuronal Phenotype ID: T1'
txt2 = 'T104'
cs = 'binary'
phys =["HCN3 (h)","HCN1 (h)","Cav 3.1 (T)","Cav 2.1 (P/Q)","Cav 1.3 (L)","HCN4 (h)","Cav 1.2 (L)","Cav 3.3 (T)","Kv 1.1 (Kdr)","Kir 3.1 (Kir)","Cav 2.2 (N)","HCN2 (h)","Kv 3.1 (Kdr)","Nav 1.1 (Naf)"]

plotHeatmap(dfrm2l,gr,phys,'red',wr,tx1, txe, ty,txt1,txt2,cs,title='')


z = dfrm2l.transpose()
z.insert(0,"Gene",gred)
z = z.reset_index()
del z['index']
df104 = z.set_index('Gene')
g104 = gred

def orgHeatmap(d, g):
    """
    Rearrange and filter data for generating an organized heatmap.

    Parameters:
    -----------
    d : DataFrame
        The input DataFrame containing gene expression data.

    g : list
        List of genes to be included in the rearranged heatmap.

    Returns:
    --------
    DataFrame
        A rearranged DataFrame filtered based on the provided gene list ('g').
        The returned DataFrame contains organized data suitable for creating a heatmap.
    """
    d = d.drop(d['Gene'].tolist().index("Kcnab1"))
    # sort y-axis: maximally expressed genes at the bottom
    d['sum'] = d.sum(axis=1, numeric_only=True)
    dfasc = d.sort_values(by=['sum'], ascending=[True])
    dfasc = dfasc.reset_index()
    del dfasc['index']
    del d['sum']
    gfull = dfasc['Gene']
    # org x-axis: cells with most to least common genes
    dfm2l = dfasc.drop(['Gene', 'sum'], axis=1).transpose()
    dfm2l['bitsum'] = [sum([2**(indx)*row for indx, row in enumerate(cell)]) for cell in dfm2l.values]
    dfm2l = dfm2l.sort_values(by=['bitsum'], ascending=[False])
    del dfm2l['bitsum']

    z = dfm2l.transpose()
    z.insert(0, "Gene", gfull)
    z = z.reset_index()
    del z['index']
    y = z.set_index('Gene')
    x = y.reindex(index=g)
    return x


def freqBar(z, a, s):
    """
    Compute frequency of each neuronal type.

    Parameters:
    -----------
    z : DataFrame
        DataFrame or matrix of neuronal types.

    a : DataFrame
        DataFrame or matrix of binarized gene expression data for all cells.

    s : str
        A string identifier or description related to the comparison.

    Returns:
    --------
    list
        A list containing frequency counts for matches between z and a.
    
    int
        Counter indicating the number of non-matching instances.
    
    list
        A list of newly encountered elements in 'a' not found in 'z'.
    """
    p = []
    new_nt_cnt = 0
    new_nt_idx = np.zeros(len(a.index)) # 1 if ol, 0 if new
    
    for i in range(len(z.index)):
        cnt = 0
        nomatch_cnt = 0
        
        for j in range(len(a.index)):
            if np.array_equal(z.values[i], a.values[j]):
                cnt += 1
                nomatch_cnt = -10
                new_nt_idx[j] = 1
            else:
                nomatch_cnt += 1
                if nomatch_cnt == 321:
                    new_nt_cnt += 1
                    
        p.append(cnt)

    new_nt = a.iloc[new_nt_idx == 0,:]
    new_nt = new_nt.transpose()
    return p, nomatch_cnt, new_nt, new_nt_idx

        
    print(f"{s}:\n \t Total No. {sum(p)}\n \t Highest repetitions = {sorted(p)[-1]} @ Cell no. {p.index(sorted(p)[-1]) + 1}\n \t 2nd Highest repetitions = {sorted(p)[-2]} @ Cell no. {p.index(sorted(p)[-2]) + 1}\n")
    print("Number of new neuronal types: ", new_nt_cnt)
    dovr = pd.DataFrame()
    dovr['Overall'] = p
    return dovr['Overall'], nomatch_cnt, new_nt

"""
dovr = pd.DataFrame()
draw = orgHeatmap(df, g104)
dovr['Overall'], nomatch_cnt, new_nt = freqBar(df104.transpose(),draw.transpose(),'')
# import IPython; IPython.embed()
#print(f"No. of cells wrt frequency \n {dovr.value_counts()}")
#print(f"Summary statistics \n {dovr.describe()}")

# recolor T4, T7, T14, T15, T30, T73, T91 in heatmap by replacing 1 in gene expression with -1
df_new = dfrm2l
common_type = [4, 7, 14, 15, 23, 30, 73, 91] # indices of commonly occuring neuronal-types
for i in common_type:
    df_new.iloc[[i-1],:]=-1 * df_new.iloc[[i-1],:]

fnt = 32
plt.rcParams['font.size']=fnt
f,axs = plt.subplots(2,1, figsize=(25,15))
sns.set(font_scale = 1.8)
sns.heatmap(dfrm2l.transpose(),linewidth = 0.4,xticklabels=False,yticklabels = gr,cmap="PiYG",cbar=False, ax=axs[0])
axs[0].set_ylabel('Genomic Identity',fontsize=fnt)
axs[0].set_yticklabels(axs[0].get_ymajorticklabels(), fontsize = fnt)
ax2 = axs[0].twinx()
ax2.yaxis.set_ticks_position('right')
ax2 = sns.heatmap(dfrm2l.transpose(),linewidth = 0.5,xticklabels=False,yticklabels = phys,cmap="PiYG",cbar=False)
ax2.set_ylabel('Physiological Identity',fontsize=fnt)
ax2.set_yticklabels(ax2.get_ymajorticklabels(), fontsize = fnt)
plt.text(tx1,ty,txt1, fontdict={'size':fnt})
plt.text(txe,ty,txt2, fontdict={'size':fnt})

# bar plot

cols = ['mediumvioletred' if z > 10 else 'green' for z in dovr['Overall']]
sns.barplot(x = dovr.index+1, y = dovr['Overall'],palette=cols, ax=axs[1])
axs[1].set_xticks(np.arange(1, 104, step=5))
axs[1].set_xlabel('Neuronal-Type ID (T#)',fontsize=fnt)
axs[1].set_ylabel('Number of Occurences',fontsize=fnt)
plt.tight_layout()
plt.savefig("tdata_red_freq.png",dpi=300,bbox_inches='tight')
plt.show()


# determine number of neuronal types and number of total cells (occurences) that lack T channel (Cacna1g) and Hcn1
# Cacna1g = df_new.iloc[:,2]
# Cacna1g_idx = df_new.iloc[:,2]#.gt(0.5) # vector of true/false for indices where Cacna1g is present
df_array = df_new.to_numpy()
df_array = np.absolute(df_array) # change -1's inserted for plotting to 1's
df_num = pd.DataFrame(df_array)
Cacna1g_idx = df_num.index[df_num.iloc[:,2]>0].tolist() # Cacna1g index = 2
Hcn1_idx = df_num.index[df_num.iloc[:,1]>0].tolist() # Hcn1 index = 1
cell_occur_vec_Cacna1g = dovr.loc[Cacna1g_idx,:]
with_Cacna1g = cell_occur_vec_Cacna1g.sum(axis=0)
without_Cacna1g = 321-with_Cacna1g

cell_occur_vec_Hcn1 = dovr.loc[Hcn1_idx,:]
with_Hcn1 = cell_occur_vec_Hcn1.sum(axis=0)
without_Hcn1 = 321-with_Hcn1
"""

# Distribution of neuronal types when ct threshold is changed
# bar plot
def barplot(dovr_13, plot_name, title, new_nt_idx):
    """
    Generate a bar plot based on given data.

    Parameters:
    -----------
    dovr_13 : DataFrame or Series
        DataFrame or Series containing data to be visualized in the bar plot.

    plot_name : str
        File name (including path) to save the generated plot.

    title : str
        Title of the generated bar plot.

    Returns:
    --------
    None

    """
    fnt = 32
    dovr_13 = dovr_13.to_frame()  # Convert to DataFrame if input is a Series
    f, axs = plt.subplots(1, 1, figsize=(25, 7.5))
    sns.set(font_scale=1.8)
    cols = ['mediumvioletred' if z > 10 else 'green' for z in dovr_13['Overall']]
    sns.barplot(x=dovr_13.index + 1, y=dovr_13['Overall'], palette=cols, ax=axs)
    axs.set_xticks([])  # Disable x-axis ticks
    axs.set_ylabel('Number of Occurrences', fontsize=fnt)
    axs.set_xlabel('Neuronal Phenotype ID', fontsize=fnt)
    axs.set_title(title, fontsize=fnt)
    axs.set(ylim=(0, 50))  # Set y-axis limits for better visualization
    plt.tight_layout()
    plt.savefig(plot_name, dpi=300, bbox_inches='tight')  # Save the plot
    plt.show()  # Display the plot

def plotHeatmap_compare(dfr, gene, phy, l, w, x1, xe, y, t1, t2, cs, title,thresh_15_nt):
    """
    Generate a heatmap plot based on provided data that highlights the new neuronal types in red

    Parameters:
    -----------
    dfr : DataFrame
        The input DataFrame containing the data to be visualized as a heatmap.

    gene : list
        List of labels for the genomic identity axis.

    phy : list
        List of labels for the physiological identity axis.

    l : int
        Length of some specific parameter.

    w : int
        Width of the generated figure for the heatmap.

    x1 : int
        x-coordinate for the placement of text 't1'.

    xe : int
        x-coordinate for the placement of text 't2'.

    y : int
        y-coordinate for the placement of texts 't1' and 't2'.

    t1 : str
        Text to be displayed at position (x1, y).

    t2 : str
        Text to be displayed at position (xe, y).

    cs : str or colormap
        Colormap to be used for the heatmap colors.

    title : str
        Title of the heatmap plot.

    Returns:
    --------
    None
    """
    dfr = dfr.transpose()
    #determine which neuronal types are new compared to ct threshold of 15 and get their column index in dfr
    p = []
    new_nt_idx = np.zeros(dfr.shape[1]) # 1 if ol, 0 if new
    
    for i in range(thresh_15_nt.shape[1]):
        cnt = 0 # frequency of nt occurrence
        nomatch_cnt = 0 # counter to determine if there is any match for an nt
        
        for j in range(dfr.shape[1]):
            if np.array_equal(thresh_15_nt.values[:,i], dfr.values[:,j]):
                cnt += 1
                nomatch_cnt = -10
                new_nt_idx[j] = 1
            else:
                nomatch_cnt += 1
                    
        p.append(cnt)
    # recolor new neuronal types by replacing 1 in gene expression with -1
    new_type = np.where(new_nt_idx == 0)[0]    

    for i in range(len(new_type)):
        dfr.iloc[:,new_type[i]]=-1 * dfr.iloc[:,new_type[i]]
        # construct dataframe with just new neuronal types by removing columns without -1
        columns_to_keep = dfr.columns[dfr.apply(lambda col: -1 in col.values)].tolist()
        df_new_nt = -1*dfr[columns_to_keep] # reset to 1

    font = 18
    f = plt.figure(figsize=(w, 7))
    ax = sns.heatmap(dfr, linewidth=0.4, xticklabels=False, yticklabels=gene, cmap="RdGy", cbar=False)
    ax.set_ylabel('Genomic Identity', fontsize=font)
    ax2 = ax.twinx()
    ax2.yaxis.set_ticks_position('right')
    ax2 = sns.heatmap(dfr, linewidth=0.5, xticklabels=False, yticklabels=phy, cmap="RdGy", cbar=False)
    ax2.set_ylabel('Physiological Identity', fontsize=font)
    ax2.set_yticklabels(ax2.get_ymajorticklabels(), fontsize=font)
    plt.text(x1, y, t1, fontdict={'size': font})
    plt.text(xe, y, t2, fontdict={'size': font})
    ax2.set_title(title, fontsize=font)
    sns.set(font_scale=2.4)
    # plt.savefig(f"{name}_{l}_heatmap.png",dpi=300,bbox_inches='tight')
    # plt.show()
    


    return   df_new_nt
    
# ct threshold <= 13
# Load dataframe with 13 used as threshold
name = 'tdata_all_13'
df13 = pd.read_csv(f"{name}.csv")

# organize 321 cells
draw = orgHeatmap(df13,g104)
# count frequency of each neuronal type as defined by Ct threshold of 15
dovr_13 = pd.DataFrame()
dovr_13['Overall'], nomatch_cnt, new_nt_13, new_nt_idx_13 = freqBar(df104.transpose(), draw.transpose(), '')

# Assuming dovr_13['Overall'] is your Pandas Series
dovr_13['Overall'] = dovr_13['Overall'].astype(int)  # Optional: Ensure values are integers

dovr_13 = pd.DataFrame({'Overall': dovr_13['Overall']})  # Convert the Series to a DataFrame with a specified column name


# plot frequency
plot_name = "tdata_red_freq_13.png"
title13 = r'$C_t \leq 13$'
barplot(dovr_13['Overall'], plot_name,title13,new_nt_idx_13)



# ct threshold <= 14
# Load dataframe with 13 used as threshold
name = 'tdata_all_14'
df14 = pd.read_csv(f"{name}.csv")

# organize 321 cells
draw = orgHeatmap(df14,g104)

# count frequency of each neuronal type as defined by Ct threshold of 15
dovr_14 = pd.DataFrame()
dovr_14['Overall'], nomatch_cnt, new_nt_14, new_nt_idx_14 = freqBar(df104.transpose(), draw.transpose(), '')

# Assuming dovr_13['Overall'] is your Pandas Series
dovr_14['Overall'] = dovr_14['Overall'].astype(int)  # Optional: Ensure values are integers

dovr_14 = pd.DataFrame({'Overall': dovr_14['Overall']})  # Convert the Series to a DataFrame with a specified column name

# plot frequency
plot_name = "tdata_red_freq_14.png"
title14 = r'$C_t \leq 14$'
barplot(dovr_14['Overall'], plot_name,title14,new_nt_idx_14)

# ct threshold <= 16
# Load dataframe with 13 used as threshold
name = 'tdata_all_16'
df16 = pd.read_csv(f"{name}.csv")

# organize 321 cells
draw = orgHeatmap(df16,g104)

# count frequency of each neuronal type as defined by Ct threshold of 15
dovr_16 = pd.DataFrame()
dovr_16['Overall'], nomatch_cnt, new_nt_16, new_nt_idx_16 = freqBar(df104.transpose(), draw.transpose(), '')

# Assuming dovr_13['Overall'] is your Pandas Series
dovr_16['Overall'] = dovr_16['Overall'].astype(int)  # Optional: Ensure values are integers

dovr_16 = pd.DataFrame({'Overall': dovr_16['Overall']})  # Convert the Series to a DataFrame with a specified column name

# plot frequency
plot_name = "tdata_red_freq_16.png"
title16 = r'$C_t \leq 16$'
barplot(dovr_16['Overall'], plot_name, title16,new_nt_idx_16)


# ct threshold <= 17
# Load dataframe with 13 used as threshold
name = 'tdata_all_17'
df17 = pd.read_csv(f"{name}.csv")

# organize 321 cells
draw = orgHeatmap(df17,g104)

# count frequency of each neuronal type as defined by Ct threshold of 15
dovr_17 = pd.DataFrame()
dovr_17['Overall'], nomatch_cnt, new_nt_17, new_nt_idx_17 = freqBar(df104.transpose(), draw.transpose(), '')

# Assuming dovr_13['Overall'] is your Pandas Series
dovr_17['Overall'] = dovr_17['Overall'].astype(int)  # Optional: Ensure values are integers

dovr_17 = pd.DataFrame({'Overall': dovr_17['Overall']})  # Convert the Series to a DataFrame with a specified column name

# plot frequency
title17 = r'$C_t \leq 17$'
plot_name = "tdata_red_freq_17.png"
barplot(dovr_17['Overall'], plot_name, title17,new_nt_idx_17)


# Heatmaps for ct threshold 13-14, 16-17
    
# ct13
# name = 'tdata_all_13'
# df13 = pd.read_csv(f"{name}.csv")
# draw = orgHeatmap(df13,g104)
def actual_orgHeatmap(df):
    # dropping Kcnab1 from red. binary map
    dfwob = df.drop(df['Gene'].tolist().index("Kcnab1"))
    gwob = dfwob['Gene']
    dfred = dfwob.drop('Gene',axis=1).transpose().drop_duplicates(keep='first').transpose()
    
    # sort yaxis: maximally expressed genes at the bottom
    dfred.insert(0,"Gene",gwob)
    dfred['sum'] = dfred.sum(axis=1,numeric_only=True)
    dfred = dfred.sort_values(by=['sum'],ascending=[True])
    gred = dfred['Gene']
    gr = gred.tolist()
    gr[gr.index('Kcna1')]=gr[gr.index('Kcna1')]+'+ab1'
    
    # sort xaxis: most to least common genes
    dfrm2l = dfred.drop(['Gene','sum'],axis=1).transpose()
    dfrm2l['bitsum'] = [sum([2**(indx)*row for indx,row in enumerate(cell)]) for cell in dfrm2l.values]
    dfrm2l = dfrm2l.sort_values(by=['bitsum'],ascending=[False])
    del dfrm2l['bitsum']
    return dfrm2l

tx1 = -12# -15
txe = 77
ty = 14.8
txt1 = 'Neuronal Phenotype ID: T1'
txt2 = 'T78'
cs = "binary"#"PiYG"
l = 7
phys =["HCN3 (h)","HCN1 (h)","Cav 3.1 (T)","Cav 2.1 (P/Q)","Cav 1.3 (L)","HCN4 (h)","Cav 1.2 (L)","Cav 3.3 (T)","Kv 1.1 (Kdr)","Kir 3.1 (Kir)","Cav 2.2 (N)","HCN2 (h)","Kv 3.1 (Kdr)","Nav 1.1 (Naf)"]

df_org_13 = actual_orgHeatmap(df13)
# df_org_13 = df_org_13.transpose()
# df_org_13.to_csv("tdata_13.csv")
df_new_nt_13 = plotHeatmap_compare(df_org_13,gr,phys,'red',wr,tx1, txe, ty,txt1,txt2,cs,title13,dfrm2l.transpose())
df_new_nt_13.to_csv("new_nt_13.csv")

txt2 = 'T86'
txe = 85
df_org_14 = actual_orgHeatmap(df14)
# df_org_14 = df_org_14.transpose()
# df_org_14.to_csv("tdata_14.csv")
df_new_nt_14 = plotHeatmap_compare(df_org_14,gr,phys,'red',wr,tx1, txe, ty,txt1,txt2,cs,title14,dfrm2l.transpose())
df_new_nt_14.to_csv("new_nt_14.csv")

txt2 = 'T114'
txe = 111
df_org_16 = actual_orgHeatmap(df16)
# df_org_16 = df_org_16.transpose()
# df_org_16.to_csv("tdata_16.csv")
df_new_nt_16 = plotHeatmap_compare(df_org_16,gr,phys,'red',wr,tx1, txe, ty,txt1,txt2,cs,title16,dfrm2l.transpose())
df_new_nt_16.to_csv("new_nt_16.csv")

txt2 = 'T122'
txe = 121
df_org_17 = actual_orgHeatmap(df17)
# df_org_17 = df_org_17.transpose()
# df_org_17.to_csv("tdata_17.csv")
df_new_nt_17 = plotHeatmap_compare(df_org_17,gr,phys,'red',wr,tx1, txe, ty,txt1,txt2,cs,title17,dfrm2l.transpose())
df_new_nt_17.to_csv("new_nt_17.csv")