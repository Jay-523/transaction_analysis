from flask import Flask, redirect, url_for, render_template,request
from chancealgo import run_rounds_api, generate_sample, weekly_combat_1
appp = Flask(__name__)
@app.route("/weekly", methods = ['GET', 'POST'])
def home2():
    if request.method == "POST":
        data = request.form.copy()

        for i in data.keys():
            data[i] = float(data[i])
        n_plr = data["n_plr"]
        fpm = data["fpm"]
        spm = data["spm"]
        tpm = data["tpm"]
        initial_chip_count = data["initial_chip_count"]

        result = weekly_combat_1(n_plr, fpm, spm, tpm, initial_chip_count)
        cssadd=" <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css' rel='stylesheet' >"
        return str(
           cssadd+ "<div class='px-2'><h1 class='text-primary mt-2'>Final updated values  :</h1> <p class='px-2'>" 
             +  str(result['plr_new']) +"</p><h4 class='text-primary mt-2 '>First prize winners: </h4><p class='px-2'>" + str(result['fpwr'])+ "</p><h4 class='text-primary mt-2' >Second prize winners: </h4><p class='px-2'>" + str(result['spwr']) + "</p><h4 class='text-primary mt-2'>Third prize winnners:</h4><p class='px-2'>" + str(result['tpwr']) +"</p></div>"
             
        )   
      
    else:
        return render_template("index2.html")
    return render_template('index2.html')

@app.route("/", methods = ['GET', 'POST'])
def home():
    if request.method == "POST":
        data = request.form.copy()

        for i in data.keys():
            data[i] = int(data[i])
        

        n_rounds = data['n_rounds']
        n_plr = data['n_plr']
        plr_added_r = data['plr_added_r']
        plr_added_s = data['plr_added_s']
        num_spins = data['num_spins']
        rt = data['rt']
        chance = data['chance']
        stake = data['stake']
        freebie = data['freebie']
       
        w, f = run_rounds_api( n_rounds,n_plr,plr_added_r,    plr_added_s,    num_spins,rt,    chance,    stake,    freebie)
        cssadd=" <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css' rel='stylesheet' >"
        return str(
           cssadd+ "<div class='px-2'><h1 class='text-primary mt-2'>These are the final chip stakes</h1> <p class='text-dark px-3'>" 
             + str(f) + "</p></div>"
             
        )   
    else:
        return render_template("index.html")
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True)
