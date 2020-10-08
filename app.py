from flask import Flask, request
import json
import pandas as pd  
from KPIs import get_basic_kpis

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>hey there</h1>"


@app.route('/api/getkpi', methods = ['GET', 'POST'])

def get_kpi():
    content = request.get_json(silent= True)
    content = json.loads(content)
    data = content[1]
    key = content[3]
    
    if(key != 'iorusjkldfh#7lkhfa#adf88ayhwgfhhdfhthweasdfasjytk'):
        return "<h1> Could not verify</h1>"
    d = pd.DataFrame(data)
    savings,inc_grad, s_grad, rs_grad,inc_median, s_median, rs_median, p, df = get_basic_kpis(d)
    return {"income_gradient": inc_grad, "savings_gradient": s_grad, "cumulative_savings_gradient": s_grad, "median_income": inc_median, "median_savings": s_median, "cumulative_savings_median": rs_median, "peristance": p}
    

if __name__ == "__main__":
    app.run()

