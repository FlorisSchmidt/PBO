from . import algorithms
from . import data_gen

def run_experiment(website_list, budget, accuracy):
    website_data = data_gen.generate_data(budget, website_list, 0.1, 0.7, 0.2)
    return algorithms.succesive_elimination(list(website_data.values()), budget, accuracy)

if __name__ == '__main__':
    pass