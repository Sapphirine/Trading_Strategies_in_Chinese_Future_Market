# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 16:48:28 2016

@author: yutingan
"""

import pandas as pd
import numpy as np
data=pd.read_csv('/Users/angela/Desktop/columbia_life/big_data_analytics/project/HC1_test.csv')
indicator=pd.read_csv('/Users/angela/Desktop/columbia_life/big_data_analytics/project/HC1_BSP.csv')
data['indicator']=indicator.x


data = data[pd.notnull(data['return.ret_duration_5_TimeDelay_1'])]



def strategy(x):
    if x>0:
        return 1
    elif x<=0:
        return 0
data.rename(columns={'df.amt': 'amt', 'df.open': 'O','df.close':'C','df.low':'L','df.high':'H','return.ret_duration_5_TimeDelay_1':'return', 'indicator':'BSP'}, inplace=True)


#data['indicator']=pd.Series(a)
a=np.empty(len(data))
a[:] = np.NAN
data['strategy']=data['return'].apply(strategy)

data['H-C']=data['H']-data['C']
data['C-L']=data['C']-data['L']


data['H-C_pct']=pd.Series(a, index=data.index)
data['C-L_pct']=pd.Series(a, index=data.index)


data['C-diff1']=pd.Series(a, index=data.index)
data['C-diff2']=pd.Series(a, index=data.index)
data['C-diff3']=pd.Series(a, index=data.index)


data['C-diff1_pct']=pd.Series(a, index=data.index)
data['C-diff2_pct']=pd.Series(a, index=data.index)
data['C-diff3_pct']=pd.Series(a, index=data.index)

list=data.columns.values
index_number=range(0,len(list))
index_dict=dict(zip(list, index_number))

for i in range(0, len(data)):
    
        if i-3>=0:
            data.iloc[i,index_dict['C-diff1']]=data.iloc[i,index_dict['C']]-data.iloc[i-1,index_dict['C']]
            data.iloc[i,index_dict['C-diff2']]=data.iloc[i,index_dict['C']]-data.iloc[i-2,index_dict['C']]
            data.iloc[i,index_dict['C-diff3']]=data.iloc[i,index_dict['C']]-data.iloc[i-3,index_dict['C']]
            if data.iloc[i,index_dict['C']] != 0:
                    data.iloc[i,index_dict['H-C_pct']]=data.iloc[i,index_dict['H-C']]/float(data.iloc[i,index_dict['C']])
                    data.iloc[i,index_dict['C-L_pct']]=data.iloc[i,index_dict['C-L']]/float(data.iloc[i,index_dict['C']])
            if data.iloc[i-1,index_dict['C']] != 0:
                data.iloc[i,index_dict['C-diff1_pct']]=data.iloc[i,index_dict['C-diff1']]/float(data.iloc[i-1,index_dict['C']])
            if data.iloc[i-1,index_dict['C']] != 0:
                         data.iloc[i,index_dict['C-diff1_pct']]=data.iloc[i,index_dict['C-diff1']]/float(data.iloc[i-1,index_dict['C']])
            if data.iloc[i-2,index_dict['C']] != 0:
                         data.iloc[i,index_dict['C-diff2_pct']]=data.iloc[i,index_dict['C-diff2']]/float(data.iloc[i-2,index_dict['C']])
            if data.iloc[i-3,index_dict['C']] != 0:
                         data.iloc[i,index_dict['C-diff3_pct']]=data.iloc[i,index_dict['C-diff3']]/float(data.iloc[i-3,index_dict['C']])



list_new=list[1:]
index_number_new=range(0,len(list_new))
index_dict_new=dict(zip(list_new, index_number_new))

data1=data

data1 = data1[pd.notnull(data1['H-C_pct'])]
data1 = data1[pd.notnull(data1['C-L_pct'])]
#data1 = data1[pd.notnull(data1['BSP'])]

#data1 = data1[pd.notnull(data1['C-diff1'])]
#data1 = data1[pd.notnull(data1['C-diff2'])]
#data1 = data1[pd.notnull(data1['C-diff3'])]

#data1 = data1[pd.notnull(data1['C-diff1_pct'])]
#data1 = data1[pd.notnull(data1['C-diff2_pct'])]
#data1 = data1[pd.notnull(data1['C-diff3_pct'])]


data_clean=data1[list_new]

total=len(data_clean)
split=total/10*7

train_data=data_clean[0:split]
test_data=data_clean[split:]

train_data.to_csv("/Users/angela/Desktop/columbia_life/big_data_analytics/project/train_data.txt",header=False,index=False,sep="\t")
test_data.to_csv("/Users/angela/Desktop/columbia_life/big_data_analytics/project/test_data.txt",header=False,index=False,sep="\t")



sum(data['strategy']) / float(len(data))


