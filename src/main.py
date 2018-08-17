import math
from tabulate import tabulate
from pandas import DataFrame
from itertools import product

def simulate(standings, matches):  
    N = 0
    place = {}
    outcomes = ['outright-win', 'top4', 'top4-tbs', 'middle4', 'elim-tbs', 'elim']
    for t in standings.keys():
        place[t] = {}
        for outcome in outcomes:
            place[t][outcome] = 0
    threshold = {}

    for i in product(['>', '<', '='], repeat=len(matches)):              
        if (N % 10**5 == 0): print(N / 10**5)
        N += 1  

        res = ''.join(map(str, i))
        sta = dict(standings)

        for i, m in enumerate(matches):
            if res[i] == '=':
                sta[m[0]] = 1 + sta[m[0]]
                sta[m[1]] = 1 + sta[m[1]]
            elif res[i] == '>':
                sta[m[0]] = 2 + sta[m[0]]
            elif res[i] == '<':
                sta[m[1]] = 2 + sta[m[1]]
            else:
                print("ERRROR {}".format(res[i]))

        # evaluate standings
        res = sorted(sta.items(), key=lambda x: x[1], reverse=True)
        high_score = res[0][1]
        bottom_score = res[-1][1]
        thresh = res[3][1]

        threshold[thresh] = threshold.get(thresh, 0) + 1

        # outright-win
        ts = [_ for _ in res if _[1] == high_score]
        if len(ts) == 1:
            for t in ts:
                place[t[0]]['outright-win'] += 1

        # top 4 & # top4-tbs
        ts = [_ for _ in res if _[1] >= thresh]
        if len(ts) == 4:
            for t in ts:
                place[t[0]]['top4'] += 1
        else:
            for t in [_ for _ in res if _[1] > thresh]:
                place[t[0]]['top4'] += 1
            for t in [_ for _ in res if _[1] == thresh]:
                place[t[0]]['top4-tbs'] += 1                

        # middle 4
        ts = [_ for _ in res if (_[1] > bottom_score and _[1] < thresh)]
        for t in ts:
            place[t[0]]['middle4'] += 1

        # elim-tbs & elim
        ts = [_ for _ in res if _[1] == bottom_score]
        if len(ts) == 1:
            for t in ts:
                place[t[0]]['elim'] += 1
        else:
            for t in ts:
                place[t[0]]['elim-tbs'] += 1
        

    
    data = []
    for t in standings.keys():
        _ = [t]        
        for out in outcomes:
            _.append(place[t][out] * 100. / N)
        data.append(_)

    df = DataFrame(data, columns=['team'] + [_ + "%" for _ in outcomes]) 
    print(tabulate(df, headers='keys', tablefmt='psql'))

    print("")
    print("N: {}".format(N))
    print("Threshold")
    print("Min: {}-{} (avg: {})".format(min(threshold.keys()), max(threshold.keys()), math.ceil(10 * sum(v * fre for v, fre in threshold.items()) / sum(threshold.values()))/10))


ga = {
    'EG': 11,
    'Liquid': 7,
    'Fnatic': 6,
    'LGD': 5,
    'VGJT': 5,
    'OG': 4,
    'IG': 4,
    'Mineski': 4,
    'Winstrike': 2
}

gb = {
    'VGJS': 7,
    'TNC': 6,
    'VP': 5,
    'Newbee': 5,
    'Vici': 4,
    'Secret': 4,
    'Serenity': 3,
    'Optic': 3,
    'Pain': 3
}

gam = [
    ['IG','OG'],
    ['LGD','Fnatic'],
    ['Liquid','Winstrike'],
    ['Mineski','VGJT'],
    ['IG','LGD'],
    ['EG','Liquid'],
    ['Fnatic','Winstrike'],
    ['OG','VGJT'],
    ['LGD','Mineski'],
    ['EG','Fnatic'],
    ['Liquid','VGJT'],
    ['OG','Winstrike']
]

gbm = [
    ['Pain','Vici'],
    ['Newbee','VP'],
    ['TNC','VGJS'],
    ['Optic','Serenity'],
    ['Pain','VP'],
    ['Newbee','VGJS'],
    ['Secret','Optic'],
    ['TNC','Serenity'],
    ['Pain','Optic'],
    ['Vici','VP'],
    ['Secret','TNC'],
    ['Serenity','VGJS'],
    ['Pain','Serenity'],
    ['Vici','Optic'],
    ['Newbee','Secret'],
    ['VP','VGJS']
]

simulate(ga, gam)