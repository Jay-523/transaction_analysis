import os 
import struct
import numpy as np

def generate_sample(n_players, freebies):
    p = []
    for i in range(n_players):
        p.append([i,freebies])

    return p
rt = 15
def get_random(n):
    #gives a random unsigned integer below n
    return (struct.unpack('I', os.urandom(4))[0]%n)

def spin(plr, rt, chance,stake):
    """
    plr: list of players, the first considers there id, and the second considers there chips balance
    rt: times the reward
    chance: chance of winning in percentage
    returns the list of winners, final chips that everyone has.
    """
    u_plr = plr.copy()
    n_winners = int(chance*len(plr)/100)
    no_chip = set()
    
    for i in plr:
        if(i[1] <stake):
            no_chip.add(i[0])
        
        
    n_players = len(plr)
    #print("the number of winners are " + str(n_winners))
    winners = set()
    c = 0
    while((n_winners>0) & (c<len(plr))):
        
        wid = get_random(n_players)
        if((wid not in winners) & (wid  not in no_chip)):
            winners.add(wid)
            n_winners-=1
        c+=1
    # updating the account balances
    for i in u_plr:
        if(i[0] in winners):
            i[1]+=stake*rt
        elif (i[0] not in no_chip):
            i[1]-=stake
    return (winners),u_plr
def run_round(i_plr, plr_added, num_spins, rt, chance, stake, freebie):
    """
    i_plr: initial players with there chip counts
    plr_added: number of players added after each rounds
    num_spins
    rt: times factor
    chance: what's winning chance
    stake: what's at stake
    freebie: free chips given
    
    """
    winn = []

    f_plr = i_plr.copy()
    for i in range(num_spins):
        w, f_plr = spin(f_plr, rt, chance, stake)
        if(i!=num_spins-1):
            
            for i in range(plr_added):
                f_plr.append([f_plr[-1][0] + 1,freebie])
        winn.append(w)
        
    return winn, f_plr

def run_rounds(n_rounds, i_plr, plr_added_r, plr_added_s, num_spins, rt, chance, stake, freebie, print_logs = False):
    """
    n_rounds: number of rounds conducted
    i_plr: initial players with there chip counts
    plr_added_r: number of players added after each rounds
    plr_added_s: number of players added after each spin
    num_spins: number of spins per round
    rt: times factor
    chance: what's winning chance
    stake: what's at stake
    freebie: free chips given
    
    
    """
    f = i_plr.copy()
    for i in range(n_rounds):
       
        winn = []
        w, f = run_round(f, plr_added_s, num_spins, rt, chance, stake, freebie)
        if(i!=n_rounds-1):
            for i in range(plr_added_r):
                f.append([f[-1][0] + 1,freebie])
        winn.append(w)
        if(print_logs == True):
            print("Results of round "+ str(i+1) + " are follows:")
            print("winners of the round are ")
            print(w)
            print("status after the round is")
            print(f)
            print('\n')
    return winn, f



def run_rounds_api(n_rounds, n_plr, plr_added_r, plr_added_s, num_spins, rt, chance, stake, freebie, print_logs = False):
    """
    n_rounds: number of rounds conducted
    n_plr: initial player number
    plr_added_r: number of players added after each rounds
    plr_added_s: number of players added after each spin
    num_spins: number of spins per round
    rt: times factor
    chance: what's winning chance
    stake: what's at stake
    freebie: free chips given
    
    
    """
    i_plr = generate_sample(n_plr, freebie)
    f = i_plr.copy()
    for i in range(n_rounds):
       
        winn = []
        w, f = run_round(f, plr_added_s, num_spins, rt, chance, stake, freebie)
        if(i!=n_rounds-1):
            for i in range(plr_added_r):
                f.append([f[-1][0] + 1,freebie])
        winn.append(w)
        if(print_logs == True):
            print("Results of round "+ str(i+1) + " are follows:")
            print("winners of the round are ")
            print(w)
            print("status after the round is")
            print(f)
            print('\n')
    return winn, f

def weekly_combat_1(n_plr, fpm, spm, tpm, initial_chip_count):
    """
    n_plr: initial state of players
    fpm: first category winning multiplier
    spm: second category winning multiplier
    tpm: thrid category winning multiplier
    initial_chip_count: initial_chip_count"""
    plr = generate_sample(100, initial_chip_count)
    fpwi = spin(plr, fpm, 50, initial_chip_count)[0]
    fpw = [plr[i] for i in fpwi]



    swc = dict()
    for i in plr:
        if(i[0] in fpwi):
            continue
        else:
            swc[i[0]] = i[1]

    swcl= [[i,swc[i]] for i in swc]

    spwi = spin(swcl, 0, 50, 0)[0]



    spw = [swcl[i] for i in spwi]

    fpwr = set([i[0] for i in fpw])
    spwr = set([i[0] for i in spw])


    tpwr_temp = set([i[0] for i in plr])

    tpwr = (tpwr_temp-(set(list(fpwr) + list(spwr))))

    plr_new = ([[i,initial_chip_count*(fpm)] for i in fpwr] + [[i,initial_chip_count*(spm)] for i in spwr]) + [[i,initial_chip_count*(tpm)] for i in tpwr]

    plr_new = sorted(plr_new)
    return {"plr_new":plr_new, "fpwr":fpwr, "spwr":spwr, "tpwr":tpwr}