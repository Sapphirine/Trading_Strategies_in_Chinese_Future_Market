# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 14:49:12 2016

@author: yutingan
"""

import pandas as pd
import numpy as np
data=pd.read_csv('~/Desktop/BigDataAnalysis/finalproject/HI1_test.csv')
data = data[pd.notnull(data['ret_duration_5_TimeDelay_1'])]
def strategy(x):
    if x>0:
        return 1
    elif x<=0:
        return 0
data['strategy']=data['ret_duration_5_TimeDelay_1'].apply(strategy)
a=np.empty(len(data))
a.fill(np.nan)
#data['previous_return'] = pd.Series(a, index=data.index)
data['previous1_close']=pd.Series(a, index=data.index)
data['previous2_close']=pd.Series(a,index=data.index)
data['previous1_diff']=pd.Series(a,index=data.index)
data['previous2_diff']=pd.Series(a, index=data.index)

for i in range(2,len(data)):
    data.iloc[i,8]=data.iloc[i-1,3]
    data.iloc[i,9]=data.iloc[i-2,3]
    data.iloc[i,10]=data.iloc[i,3]-data.iloc[i,8]
    data.iloc[i,11]=data.iloc[i,3]-data.iloc[i,9]
data = data[pd.notnull(data['previous2_diff'])&pd.notnull(data['previous1_diff'])] 
data_clean=data[['df.open','df.close','df.low','df.high','previous1_diff','previous2_diff','strategy']]   
train_data=data_clean[0:4000]
test_data=data_clean[4001:]

train_data.to_csv("~/Desktop/BigDataAnalysis/finalproject/HI1_train_data.txt",header=False,index=False,sep="\t",mode='a')
test_data.to_csv("~/Desktop/BigDataAnalysis/finalproject/HI1_test_data.txt",header=False,index=False,sep="\t",mode='a')