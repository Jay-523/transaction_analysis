import time 
import datetime


import pandas as pd
import numpy as np
from scipy import stats
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from KPIs import *

# Helper functions until get cluster info

def cluster(x, y, eps, s, plot=  False):
    """x, y , eps, s      
    x-> x dimension, y-> y dimension, eps -> epsilon, s -> minimum sample for DBSCAN
    Clusters all the amounts"""
    estimator = DBSCAN(eps =eps, min_samples=s)
    
    a = pd.DataFrame()
    a['x'] = x
    a['y'] = y
    estimator.fit(a['x y'.split()])
    a['labels'] =estimator.labels_
    if(plot == True):
        for i in a.labels.unique():
            if(i != -1):
                l = a[a.labels == i]
                plt.scatter(l.x, l.y)
        plt.show()
    return a.labels.values
def filter(x):
    return x[x['amount'] > 100]

def print_cluster_info(data):
    """Returns list of cluster seperated dataframes, takes in data, with column label"""
    for i in data.label.unique():

        
        
        print(" Number of entries in Cluster No. {} : {}".format(i, data[data.label == i].shape[0]) )
   
    clusters = []
    for i in data.label.unique():
       
        clusters.append(data[data.label == i])
    return clusters
def get_expenses_dataframe(df, convert_date = True, plot = False):
    try:
        if (convert_date == True):
            df.date = (df.date/1000).apply(lambda  x :datetime.datetime.fromtimestamp(x))     
    except:
        pass
    
    df = prepare(df, convert_date = False)
    exp = df[df.amount < 0]
    exp = exp[exp.amount < -100]    
    e = exp['amount date month_number'.split()]

    e['amount'] = e.amount.apply(np.abs)
    e['day'] = e.date.apply(lambda x: x.day)
    e['label'] = cluster(e.day, e.amount, 16, 4, plot = False)
    e['label'] = cluster(e.day, e.amount, 16, 4, plot = False)
    if(plot == True):
        e['label'] = cluster(e.day, e.amount, 5, 4)
    ez = []
    for i in e.label.unique():
        
        d = e[e.label == i]
        median_amount = d.amount.median()
        median_day =  d.day.median()
        t= d.groupby('month_number').count().label.reset_index()
        t.columns=  ['month_number', 'rep']
        d = pd.merge(d, t, on = 'month_number' )
    
        nrdf = d[d.rep == 1]
    
        rdf = d[d.rep > 1]
        rdf['day_lag'] = np.abs(rdf.day - median_day)
        rdf['amount_lag'] = np.abs(rdf.amount - median_amount)
        rdf['total_lag'] = rdf.day_lag + rdf.amount_lag
        lag = rdf['month_number total_lag'.split()].groupby('month_number').min().reset_index()
    
    
        to_drop = []
        for i, j in rdf.iterrows():
            if(j.total_lag != lag[lag.month_number == j.month_number].total_lag.values):
                to_drop.append(i)
    
    
        for i in to_drop:
            rdf.drop(i, inplace = True)
    
        rdf = rdf.groupby('month_number').min()
        
        x = pd.concat([rdf.reset_index()['amount date month_number day label rep'.split()], nrdf])
        ez.append(x)
    e = pd.concat(ez)
    dev = e.groupby('label').std()
    m = e.groupby('label').median()
    dev['count'] = e.label.value_counts()
    m['count'] = e.label.value_counts()
    m['amount_std']=  dev.amount
    m['day_std'] = dev.day
    return m


def verify_expense(expenses, frequencies, df, tm, convert_date = True):
    """amount refers to the amount of expence, frequency is the number of months she needs to pay in an year
        and m is the expense analytics dataframe obtained from the about function"""
    verification_status = []
    m = get_expenses_dataframe(df, convert_date = convert_date)
    for i in range(len(expenses)):
        d = m.copy()
        d['diff'] = d.amount - expenses[i]
        if(d[d['diff'] == (np.abs((m.amount - expenses[i])).min())].shape[0] >=1):
            frequency = d[d['diff'] == (np.abs((df.amount + expenses[i])).min())]['count'].max()
           
            if (np.abs(frequency - (tm/12)*frequencies[i]) >3):
                verification_status.append('can_not_verify')
            else:
                verification_status.append('verified')
        else:
            (verification_status.append('can_not_verify'))
    
    return verification_status
        
def get_recurrent_expenses(m, tm):
    
    "returns the recurrent expenses and standard deviations of respective payment dates"
    return list(m[m['count'] > tm-4].reset_index()[m[m['count'] > tm-4].reset_index().label != -1].amount.values), list(m[m['count'] > tm-4].reset_index()[m[m['count'] > tm-4].reset_index().label != -1].day_std.values)
        

def get_rental_month_duration(d, rent):
    a = d[d.amount == -1*rent].month_number.min()
    b = d[d.amount == -1*rent].month_number.max()
    if (a <=12):
        a_year = 2019
    else:
        a_year = 2020
    if(b <=12):
        b_year = 2019
    else:
        b_year = 2020
    
    return (a%12, a_year, b%12, b_year)




