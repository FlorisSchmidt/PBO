import numpy as np
import math
from itertools import product

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
    element_effects = generate_effects(effect_A, effect_B)
    interaction_probs = generate_interaction_probs(element_effects)
    for prob in interaction_probs.keys():
        interaction_probs[prob] = generate_synergestic_effect(
            interaction_probs[prob], normal_sd)
    realisations = generate_realisations(budget, interaction_probs)
    final_data = select_data(website_list, realisations)
    return final_data


#### HELPER FUNCTIONS ####

def sigmoid(x):
    sig = 1 / (1 + math.exp(-x))
    return sig


def generate_effects(A, B, n_texts=3, n_headers=3, n_pictures=3):
    header_effects, text_effects,  picture_effects = dict(), dict(), dict()
    for i in range(n_texts):
        header_effects[f"header_{i+1}"] = np.random.uniform(A, B)
    for i in range(n_texts):
        text_effects[f"text_{i+1}"] = np.random.uniform(A, B)
    for i in range(n_texts):
        picture_effects[f"picture_{i+1}"] = np.random.uniform(A, B)
    return {"header_effects": header_effects, "text_effects": text_effects, "picture_effects": picture_effects}


def generate_interaction_probs(effect_dict):
    interaction_probs = dict()
    header_effects = effect_dict.get("header_effects")
    text_effects = effect_dict.get("text_effects")
    picture_effects = effect_dict.get("picture_effects")
    combinations = product(header_effects.keys(),
                           text_effects.keys(), picture_effects.keys())
    for combination in combinations:
        interaction_probs[combination] = sigmoid(header_effects.get(
            combination[0]) + text_effects.get(combination[1]) + picture_effects.get(combination[2]))
    return interaction_probs


def generate_synergestic_effect(probability, sd):
    return min(np.random.normal(probability, sd), 1)


def generate_realisations(budget, probabilities):
    realisations = dict()
    for website in probabilities.keys():
        site_data = []
        for i in range(budget):
            site_data.append(np.random.binomial(1, probabilities[website]))
        realisations[website] = site_data
    return realisations


def select_data(website_list, final_data):
    selected_data = dict()
    for website in website_list:
        selected_data[website] = final_data[website]
    return selected_data
