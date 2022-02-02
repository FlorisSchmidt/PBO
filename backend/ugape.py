from . import data_gen as gen
from math import sqrt, log, pow, inf

### ALGORTIHM ###

def UGapE(data, budget, accuracy, confidence, m, c):
    K = len(data)

    ## Initialise
    for arm_name in data.keys():
        data[arm_name].pull()

    ## Main loop
    Jt = ''
    Bkt_dict = ''
    reason = ''
    t = K + 1
    budget -= K
    stopping_criteria = True
    while (stopping_criteria):
        budget -= 1
        current_arms = [data[arm_name] for arm_name in data.keys()]
        
        a = c * log((4*K*(t**3))/confidence)
        Jt, Bkt_dict = select_arm(current_arms, m, a)

        key = get_max_key(Bkt_dict, Jt)
        t += 1
        if (Bkt_dict[key] < accuracy):
            stopping_criteria = False
            reason = 'Terminated because specified accuracy has been satisfied'
        elif budget == 0:
            stopping_criteria = False
            reason = 'Terminated because budget is exhausted'
    return Jt
    
def select_arm(data, m, a):   
    current_arms = data

    ukt_dict = dict()
    lkt_dict = dict()
    bkt_dict = dict()
    beta_dict = dict()
    # Compute Uk(t) and Lk(t) for each arm",
    for k in current_arms:
        beta_dict[k] = calc_beta(k, a)
        ukt = k.last_average + beta_dict[k]
        lkt = k.last_average - beta_dict[k]
        ukt_dict[k] = ukt
        lkt_dict[k] = lkt
    # Compute Bk(t) for each arm",
    for k in current_arms:
        ukt_dict_subset = ukt_dict.copy()
        ukt_dict_subset.pop(k)
        # Find max Ukt
        ukt_subset_sorted = dict(
            sorted(ukt_dict_subset.items(), key=lambda item: item[1]))
        max_ukt = list(ukt_subset_sorted.keys())[-m]
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
    # Identify and pull arm I(t)
    keyz = [lower, upper]
    It = get_max_key(beta_dict, keyz)
    It.pull()

    return Jt, bkt_dict

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