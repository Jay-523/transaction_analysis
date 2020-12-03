from flask import Flask, request
import json
import pandas as pd  
from KPIs import get_basic_kpis
from clustering import *
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/')
def hello():
    return "<h1>FlatFolder KPI</h1>"


@app.route('/api/getkpi', methods = ['GET', 'POST'])

def get_kpi():
    
    content = request.get_json(silent= True)

    
    #content = json.loads(content)
    data = content['data']
    
    
    
    key = content['api_key']
    
    if(key != 'iorusjkldfh#7lkhfa#adf88ayhwgfhhdfhthweasdfasjytk'):
        return {'login': 'could not verify'}
    d = pd.DataFrame(data[1])
    savings,inc_grad, s_grad, rs_grad,inc_median, s_median, rs_median, p, df, tm = get_basic_kpis(d, convert_date= True)
    rent_verified = 'can_not_verify'
    rent = data[0]['qa4']['current_rent_amount']
    if(rent != ''):
        rent_verified = verify_expense([int(rent)], [12], d, tm)[0]



    m = get_expenses_dataframe(d)
    total_month_missed = ((tm - m[m.amount == rent]['count']).values)
    if(len(total_month_missed) == 0):
        total_month_missed = 'N.A.'
    else:
        total_month_missed = total_month_missed[0]
    
    a, a_year, b, b_year = get_rental_month_duration(d, rent)
    a = int(d[d.month_number == a].head(1).month.values)
    b = int(df[df.month_number == b].head(1).month.values)
    return {"income_gradient": str(inc_grad), "savings_gradient": str(s_grad), "cumulative_savings_gradient": str(s_grad), "median_income": str(inc_median), "median_savings": str(s_median), "cumulative_savings_median": str(rs_median), "peristance": str(p), "rent_verified": str(rent_verified),
            "start_month": str(a), "start_year": str(a_year), "end_month": str(b), "end_year": str(b_year), "total_month_missed": str(total_month_missed)}
 

  

if __name__ == "__main__":
    app.run()
