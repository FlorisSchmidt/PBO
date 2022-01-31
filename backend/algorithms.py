from typing import List
from math import sqrt, log, pow, inf

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


def UGapEb(data, m, budget, a):
    '''
    Inputs:
    data: (dict) website name as key and website object as value
    m: (Int) number of arms
    budget: (Int) number of iterations (i.e. number of visitor to the website)
    a: (float) exploration parameter (0.5 is always a good choice)

    Outputs:
    Website object (the optimal arms)
    '''
    K = len(data)
    ## Initialise
    for arm_name in data.keys():
        data[arm_name].pull()
    ## Main loop
    Jt = ''
    bkt_dict = ''
    t = 0
    for t in range(K+1,budget):
        
        current_arms = [data[arm_name] for arm_name in data.keys()]
        Jt, bkt_dict = select_arm(current_arms, m, a)

    return get_min_key(bkt_dict, Jt)

def UGapEc(data, e, m, delta, c=0.5):
    '''
    Inputs:
    data: (dict) website name as key and website object as value
    e: (float) accuracy parameter
    m: (Int) number of arms
    delta: (float) confidence level
    c: (float) exploration parameter (0.5 is always a good choice)

    Outputs:
    Set of website objects (i.e. the optimal arms)
    '''
    K = len(data)
    
    ## Initialise arms
    for arm_name in data.keys():
        data[arm_name].pull()

    ## Main loop
    Jt = ''
    Bkt_dict = ''
    t = K + 1
    stopping_criteria = True
    while (stopping_criteria):
        current_arms = [data[arm_name] for arm_name in data.keys()]

        a = c * log((4*K*(t**3))/delta)
        Jt, Bkt_dict = select_arm(current_arms, m, a)

        key = get_max_key(Bkt_dict, Jt)
        t += 1
        if (Bkt_dict[key] >= e):
            stopping_criteria = False
        
    return Jt


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

def calc_beta(arm, a):
    return sqrt(a/arm.num)

def get_max_key(input_dict, keys):
    new_dict = dict()
    for item in keys:
        new_dict[item] = input_dict[item]
    return max(new_dict, key=new_dict.get)

def get_min_key(input_dict, keys):
    new_dict = dict()
    for item in keys:
        new_dict[item] = input_dict[item]
    return min(new_dict, key=new_dict.get)

def select_arm(data, m, a):   
    current_arms = [data[arm_name] for arm_name in data.keys()]

    ukt_dict = dict()
    lkt_dict = dict()
    bkt_dict = dict()
    beta_dict = dict()
    # Compute Uk(t) and Lk(t) for each arm\n",
    for k in current_arms:
        beta_dict[k] = calc_beta(k, a)
        ukt = k.last_average + beta_dict[k]
        lkt = k.last_average - beta_dict[k]
        ukt_dict[k] = ukt
        lkt_dict[k] = lkt
    # Compute Bk(t) for each arm\n",
    for k in current_arms:
        ukt_dict_subset = ukt_dict.copy()
        ukt_dict_subset.pop(k)
        max_ukt = max(ukt_dict_subset, key=ukt_dict_subset.get)
        bkt = ukt_dict[max_ukt] - lkt_dict[k]
        bkt_dict[k] = bkt

    # Identify the set of m arms J(t)\n",
    bkt_dict_sorted = dict(sorted(bkt_dict.items(), key=lambda item: item[1]))
    Jt = set(list(bkt_dict_sorted.keys())[:m])

    # Identify arm with minimum lower bound in J(t)\n",
    lowest = inf
    contenders = []
    for arm in Jt:
        if lkt_dict[arm] <= lowest:
            contenders.append(arm)
    if len(contenders) > 1:
        lower = get_min_key(beta_dict, contenders)
    else:
        lower = contenders[0]
    # Identify arm with maximum upper bound *not* in J(t)\n",
    not_in_jt = list(set(ukt_dict.keys()) - Jt)
    highest = -inf
    contenders = []
    for arm in not_in_jt:
        if ukt_dict[arm] >= highest:
            contenders.append(arm)
    if len(contenders) > 1:
        upper = get_max_key(beta_dict, contenders)
    else:
        upper = contenders[0]
    # Identify and pull arm I(t)\n",
    keyz = [lower, upper]
    It = get_max_key(beta_dict, keyz)
    It.pull()

    return Jt, bkt_dict

