import numpy as np
import math
from itertools import product

class Website:
    """Iterator that counts upward forever"""

    def __init__(self, website, p, realisations):
        self.num = 0
        self.p = p
        self.realisations = realisations[website]
        self.average = 0
        self.last_average = 0
        self.totalSum = 0
        self.name = website
        self.fullName = f"Header {website[0]} text {website[1]} picture {website[2]}"

    def __iter__(self):
        return self

    def __next__(self):
        realisation = self.realisations[self.num]
        self.num += 1
        return realisation

    def pull(self):
        self.totalSum+=self.__next__()
        self.last_average = self.average
        self.average = self.totalSum/self.num
        return self.average

    def reset(self):
        self.average = 0
        self.totalSum = 0
        self.num = 0


def generate_data(budget, website_list, effect_A, effect_B, normal_sd):
    '''
    Inputs:
    budget: (Int) number of visitors to the domain
    website_list: (list of tuples of the form ("header_x", text_y", "picture_z") website configurations specified by user
    effect_A: (Int) Lower bound for step one of the data generation
    effect_B: (Int) Upper bound for step one of the data generation
    normal_sd: Int)

    Outputs:
    Dict with N (budget) realisations of generated bernoulli stochastic variable for all combinations in website_list
    '''
    element_effects = _generate_effects_(effect_A, effect_B)
    interaction_probs = _generate_interaction_probs_(element_effects)
    synegestic_probs = dict()
    for prob in interaction_probs.keys():
        synegestic_probs[prob] = _generate_synergestic_effect_(
            interaction_probs[prob], normal_sd)
    realisations = _generate_realisations_(budget, synegestic_probs)
    final_data = _select_data_(website_list, realisations)
    websites = dict()
    for website in final_data:
        p = synegestic_probs[website]
        websites[website] = Website(website, p, realisations)
    return websites


#### HELPER FUNCTIONS ####

def _sigmoid_(x):
    sig = 1 / (1 + math.exp(-x))
    return sig

def _tanh_(x):
    tanh = (math.exp(x) - math.exp(-x)) / (math.exp(-x) + math.exp(x))
    return tanh

def _generate_effects_(A, B, n_texts=3, n_headers=3, n_pictures=3):
    header_effects, text_effects,  picture_effects = dict(), dict(), dict()
    for i in range(n_texts):
        header_effects[f"{i+1}"] = np.random.uniform(A, B)
    for i in range(n_texts):
        text_effects[f"{i+1}"] = np.random.uniform(A, B)
    for i in range(n_texts):
        picture_effects[f"{i+1}"] = np.random.uniform(A, B)
    return {"header_effects": header_effects, "text_effects": text_effects, "picture_effects": picture_effects}


def _generate_interaction_probs_(effect_dict):
    interaction_probs = dict()
    header_effects = effect_dict.get("header_effects")
    text_effects = effect_dict.get("text_effects")
    picture_effects = effect_dict.get("picture_effects")
    combinations = product(header_effects.keys(),
                           text_effects.keys(), picture_effects.keys())
    for combination in combinations:
        comb_string = ''
        for item in combination:
            comb_string += item
        interaction_probs[comb_string] = _tanh_(header_effects.get(
            combination[0]) + text_effects.get(combination[1]) + picture_effects.get(combination[2]))
    return interaction_probs


def _generate_synergestic_effect_(probability, sd):
    return min(np.random.normal(probability, sd), 1)


def _generate_realisations_(budget, probabilities):
    realisations = dict()
    for website in probabilities.keys():
        site_data = []
        for i in range(budget):
            site_data.append(np.random.binomial(1, probabilities[website]))
        realisations[website] = site_data
    return realisations


def _select_data_(website_list, final_data):
    selected_data = dict()
    for website in website_list:
        selected_data[website] = final_data[website]
    return selected_data

