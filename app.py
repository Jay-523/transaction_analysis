from flask import Flask, request
import json
import pandas as pd  
from KPIs import get_basic_kpis
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
    if(rent != ''):
        rent_verified = verify_expense([int(rent)], [12], d, tm)[0]



    
    total_month_missed = ((tm - m[m.amount == rent]['count']).values)
    if(len(total_month_missed) == 0):
        total_month_missed = 'N.A.'
    else:
        total_month_missed = total_month_missed[0]
    
    a, a_year, b, b_year = get_rental_month_duration(d, rent)
    return {"income_gradient": inc_grad, "savings_gradient": s_grad, "cumulative_savings_gradient": s_grad, "median_income": inc_median, "median_savings": s_median, "cumulative_savings_median": rs_median, "peristance": p, "rent_verified": rent_verified,
            "start_month": a, "start_year": a_year, "end_month": b, "end_year": b_year, "total_month_missed": total_month_missed}
 

  

if __name__ == "__main__":
    app.run(debug = True)

