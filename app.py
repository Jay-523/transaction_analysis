from flask import Flask, request
import json
import pandas as pd  
from KPIs import get_basic_kpis
from clustering import *
from flask_cors import CORS
import numpy as np
from clustering import cluster
from KPIs import key
from clustering import trim
from clustering import get_cluster_val
from clustering import prepare




app = Flask(__name__)
CORS(app)
@app.route('/')
def hello():
    return "<h1>FlatFolder KPI</h1>"


@app.route('/api/getkpi', methods = ['GET', 'POST'])

def func():
    
    
    content = request.get_json(silent = True)
    d = content['data']
    amounts = pd.DataFrame(d[1][0]['transactions'])['transactionAmount'].apply(lambda x: x['amount'])

    date = pd.DataFrame(d[1][0]['transactions'])['bookingDate']
    df = pd.DataFrame()
    df['date'] = date
    df['amount'] = amounts
    df.amount = df.amount.apply(lambda x: float(x))
    df.date = pd.to_datetime(df.date)
    df.amount*=-1
    sd = df.copy()
    sd = sd[sd.amount>300]
    if(sd.shape[0] < 5 ):
        return "Could not find rent"
    labels = cluster(sd.amount,1, sd.amount.median()*0.1, 3 , plot = False)
    sd['labels'] = labels
    sd = sd[sd.labels!=-1]
    labels = sd.labels.unique()
    clusters = []
    for i in labels:
        clusters.append(sd[sd.labels == i])
#     cluster_val = get_cluster_val(clusters)
    ans = get_cluster_val(clusters)
    ans.sort(key = key,reverse= True)
    return str({'duration': ans[0][1]['duration_testdf'], 'amount': ans[0][0]['med_testdf']})
  
if __name__ == "__main__":
    app.run()
