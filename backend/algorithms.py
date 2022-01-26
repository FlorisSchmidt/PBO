from typing import List
from math import sqrt, log, pow

def run_test(website_list, budget, algorithm, accuracy):
    #1 Unpack data 
    #2 Pass to right test
    if algorithm == "se":
        results = succesive_elimination(website_list, budget, accuracy)
    elif algorithm == 'thompson':
        results = thompson_sampling(website_list, budget)
    elif algorithm == 'epsilon_greedy':
        results = epsilon_greedy(website_list, budget)
    return results

def standard_multivariate_test(data, budget):
    pass


def thompson_sampling(data, budget):
    pass


def epsilon_greedy(data, budget):
    pass


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

### HELPER FUNCTIONS ###

def calculate_means(unpacked_data):
    pass
