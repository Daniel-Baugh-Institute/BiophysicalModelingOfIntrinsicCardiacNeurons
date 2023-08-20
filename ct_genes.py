# -*- coding: utf-8 -*-
"""
Created on 18 Aug. 2022

@author: sgupta
"""

import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as pc
from matplotlib.colors import LinearSegmentedColormap
from mycolorpy import colorlist as mcp
import plotly.graph_objects as go
import plotly_express as px
import math as m
import plotly.io as pio
import seaborn as sns

font = 19 

dfth = pd.read_csv('threshold.csv')
dfth['sum'] = dfth.sum(axis=1,numeric_only=True)

uni = dfth['Expression Threshold'].nunique()
color =mcp.gen_color(cmap="viridis_r",n=uni)

thr = dfth['Expression Threshold'].tolist()
norm = [(float(t)-float(thr[0])) / (float(thr[-1])-float(thr[0])) for t in thr]
cols = plt.cm.jet(norm)
for i,j in enumerate(thr):
	thr[i]=f'$C_t \leq {j}$'

d = dfth.drop('Expression Threshold',axis=1)

d.insert(1,'Expression Threshold',thr)

f = px.bar(d,x='Gene',y='sum', color = d['Expression Threshold'], color_discrete_sequence=color, barmode='group',labels={'sum':'No. of Neurones Expressing the Genes','Gene':'Ion Channel Genes','color':''},template="simple_white")#,title = 'Comparison of Expression Thresholds')
f.update_layout(width=1100,height=550,font=dict(size=font),bargap = 0.4, yaxis = dict(tickfont = dict(size=font)),xaxis = dict(tickfont = dict(size=font)))
f.update_layout(legend = dict(font = dict(size = font), orientation = 'v',x=1.0,y=0.99,tracegroupgap=10), legend_title = dict(font = dict(size = font),text=''))

pio.write_image(f,"threshold.png",format='png',scale=10,width=1100, height=550, validate=True)
# f.show()

