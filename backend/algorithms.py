from typing import List
from math import sqrt, log, pow, inf
from . import ugape as ugap

def run_test(website_list, budget, algorithm, accuracy, confidence, m):
    #1 Unpack data 
    #2 Pass to right test
    if algorithm == "se":
        results = succesive_elimination(website_list, budget, accuracy)
    elif algorithm == 'ugape':
        results = ugap.UGapE(website_list, budget, accuracy, confidence, m, c=0.5)
    return results


def succesive_elimination(S, budget, accuracy):
    t = 1
    c = 4
    delta = 1 - accuracy

    while (len(S) > 1) and (budget-t>0):
        for site in S:
            site.pull()
        p_a = [site.average for site in S]
        p_max = max(p_a)
        n = len(p_a)
        alpha_t = sqrt(log((c*n*pow(t,2))/delta)/t)

        for a in S:
            if(p_max - a.average>=2*alpha_t):
                S.remove(a)
        t+=1
    return S


