# -*- coding: utf-8 -*-
import time 
import datetime


import pandas as pd
import numpy as np
from scipy import stats
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt


def getgrad(x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(x),y)
    return slope

#input can be changed as per liking




def prepare(df, convert_date = True):
    try:
        df.date = (df.date/1000).apply(lambda  x :datetime.datetime.fromtimestamp(x))
    except:
        pass
    
    
    df['is_income'] = df.amount.apply(lambda x: x > 0)
    min_date = df.date.min()
    max_date = df.date.max()
    
    df['month'] = df.date.apply(lambda x: x.month)
    df['year'] = df.date.apply(lambda x: x.year)
    
    min_year = df.year.min()
    min_month_of_min_year= min_date.month
    
   
    df['month_number'] = (df['month'] + (df.year - min_year)*12)
    min_month_number = df.month_number.min()
    max_month_number = df.month_number.max()
    

   
    
    if(min_date.day != 1):
        df = df[df['month_number'] != min_month_number]
    if(max_date.day < 28):
        df = df[df['month_number']!= max_month_number]
        
 
    return df['amount date is_income month year month_number'.split()]






def get_basic_kpis(__df, convert_date = True):
    
    """savings,inc_grad, s_grad, rs_grad,inc_median, s_median, rs_median, p, df"""
    #preparation of basic variables and tables
    df = __df.copy()
    try:
        if (convert_date == True):
            df.date = (df.date/1000).apply(lambda  x :datetime.datetime.fromtimestamp(x))
    except:
        pass
    
    df['is_income'] = df.amount.apply(lambda x: x > 0)
    min_date = df.date.min()
    max_date = df.date.max()
    
    df['month'] = df.date.apply(lambda x: x.month)
    df['year'] = df.date.apply(lambda x: x.year)
    
    min_year = df.year.min()
    min_month_of_min_year= min_date.month
    
   
    df['month_number'] = (df['month'] + (df.year - min_year)*12)
    min_month_number = df.month_number.min()
    max_month_number = df.month_number.max()
    
    
    
   
    
    if(min_date.day != 1):
        df = df[df['month_number'] != min_month_number]
    if(max_date.day < 28):
        df = df[df['month_number']!= max_month_number]
    
   
    
    #table for savings
    
    savings = df.groupby('month_number').sum()[['amount']]
    
    savings.columns = ['amount']
    savings.reset_index(inplace = True)
    
    
    
    
    
    # Table for running sum of savings
    savings['cumulative_savings'] = (savings.amount.cumsum())
    
    
    # Calculating persistence (P)
    #print(savings)
    tm = savings.month_number.max() - savings.month_number.min() + 1
    s = (savings.amount > 0).sum()
    rs = (savings.cumulative_savings > 0).sum()
    
    # This is something we have to work out 
    
    p = (rs + 10*s)/(11*tm)
    
    # Calculating standard deviation and gradient
    
    
    
    
    # Adding income to savings 
    
    # Making income columns now
    
    income = pd.DataFrame()
    income['income'] = df[df.is_income].groupby('month_number').sum()['amount']
    
    income.reset_index(inplace = True)
    savings = pd.merge(savings, income, on = 'month_number')
    
    
    
    
    # Calculating the gradients and medians and gradients of these features
    
    # Income
    
    
    
    inc_grad = getgrad( savings.month_number, savings.income)
    s_grad = getgrad( savings.month_number, savings.amount)
    rs_grad = getgrad( savings.month_number, savings.cumulative_savings)
    
    inc_median = savings.income.median()
    s_median = savings.amount.median()
    rs_median = savings.cumulative_savings.median()
    savings.columns = 'month_number savings cumulative_savings income'.split()
    return savings,inc_grad, s_grad, rs_grad,inc_median, s_median, rs_median, p, df, tm
#savings,inc_grad, s_grad, rs_grad,inc_median, s_median, rs_median, p = get_basic_kpis(data)


def get_viz_bar(df):
    """Liable to change based on frontend choice"""
    
    
    return df.plot(kind= 'bar')



# Clusterring functions:
    
def cluster(x, y, eps, s):
    """x, y , eps, s      
    x-> x dimension, y-> y dimension, eps -> epsilon, s -> minimum sample for DBSCAN
    Clusters all the amounts"""
    estimator = DBSCAN(eps =eps, min_samples=s)
    
    a = pd.DataFrame()
    a['x'] = x
    a['y'] = y
    estimator.fit(a['x y'.split()])
    a['labels'] =estimator.labels_
    for i in a.labels.unique():
        if(i != -1):
            l = a[a.labels == i]
            plt.scatter(l.x, l.y)
    plt.show()
    return a.labels.values
def filter(x):
    return x[x['amount'] > 100]

def print_cluster_info(data):
    for i in data.label.unique():
        """Returns list of cluster seperated dataframes"""
        
        
        print(" Number of entries in Cluster No. {} : {}".format(i, data[data.label == i].shape[0]) )
   
    clusters = []
    for i in data.label.unique():
       
        clusters.append(data[data.label == i])
    return clusters




        
        

